from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import cv2
import os

model = YOLO("best.pt")
names = model.names

cap = cv2.VideoCapture("mv.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

idx = 0
while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    im0 = cv2.resize(im0, (640,400))

    results = model.predict(im0, show=False)
    boxes = results[0].boxes.xyxy.cpu().tolist()
    clss = results[0].boxes.cls.cpu().tolist()
    annotator = Annotator(im0, line_width=2, example=names)
    #畫面有物件
    if boxes is not None:
        for box, cls in zip(boxes, clss):
            idx += 1
            annotator.box_label(box, color=colors(int(cls), True), label=names[int(cls)])

            crop_obj = im0[int(box[1]):int(box[3]), int(box[0]):int(box[2])]

            print(box)


    cv2.imshow("ultralytics", im0)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()