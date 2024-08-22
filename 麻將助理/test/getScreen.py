from ultralytics import YOLO
import cv2

#load model
mahjongModel = YOLO("best.pt")

#load video
VIDEO = "mv.mp4"
cap = cv2.VideoCapture(VIDEO)
#影片中有其他雜項,要讀特定幾個才做這件事
#vehicles=[0,1,2,3,4,5,6,7,8,9,10]

#read frames
ret = True
while ret:
    ret , frame = cap.read()
    if ret  :
        # detection vehicles 
        frame=cv2.resize(frame,(800,600))
        #crop_frame
        # 取得影像的高度和寬度
        height, width = frame.shape[:2]

        # 計算要截取的高度範圍
        top = height-(height // 5)  # 只取五分之一的高度
        bottom = height  # 原始影像的底部

        # 截取影像
        cropped_image = frame[top:bottom, :]
        #載入模型
        detections = mahjongModel(cropped_image)[0]

        detections_=[]
        #print(detections) => img2
        for detection in detections.boxes.data.tolist():
            #print(detection) => img1
            x1,y1,x2,y2,score,class_id = detection
            detections_.append([x1,y1,x2,y2,score,class_id])
            #if int(class_id) in vehicles:
            #   detections_.append([x1,y1,x2,y2,score,class_id])
        
        
        for detection in detections_:
            x1,y1,x2,y2,score,class_id = detection
            
            #畫框
            cropped_image=cv2.rectangle(cropped_image,(int(x1),int(y1)),(int(x2),int(y2)),(255,0,0),2)
            cv2.putText(cropped_image,f"{detections.names[class_id]}",(int(x1),int(y1)-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)

            #print(f"class_id:{detections.names[class_id]}")

        #crop
        """ crop=frame[int(y1):int(y2),int(x1):int(x2)]
        crop= cv2.resize(crop,(500,500))
        cv2.imshow("crop",crop) """

        cv2.imshow("frame2",cropped_image)
        cv2.imshow("frame",frame)
        
        
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    else:
        print("cap is error")
        break
        
cap.release()
