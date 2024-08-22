from ultralytics import YOLO
import cut_img as cut_img
import web_get
import sys
class yolo_img:
    def __init__(self):
        self.model=self.load_model()
        

    def load_model(self)-> tuple[YOLO, YOLO]:
        """回傳yolo模型 ,前面是一般台麻,後面是補充紅寶牌跟白板的資料"""
        return YOLO("麻將助理\\base.pt"),YOLO("麻將助理\\extra.pt")

    def predict(self,model)->tuple[dict,list,dict,list]:
        """
            input:
            model:YOLO模型
            img_path:圖片路徑
            回傳yolo的預測結果

            output:
            name_extra:回傳額外的名稱字典
            detect_extra:回傳額外的預測結果
            name_base:回傳一般的名稱字典
            detect_base:回傳一般的預測結果

        """
        img_path=cut_img.get_screen()
        base,extra = model
        detect_extra = []
        detect_base = []

        def detect(results:YOLO,detect:list=[])-> tuple[list,dict]:
            detect = []
            for i in results[0].boxes.data.tolist():
                _,_,_,_,confidence,classid = i
                detect.append(classid)
                #print(f"{results[0].names[classid]}: {confidence}")
            return detect , results[0].names
        
        results_extra=extra(img_path)
        detect_extra,name_extra = detect(results_extra,detect_extra)    
        results_base=base(img_path)
        detect_base,name_base = detect(results_base,detect_base)

        name_base = {key: value[::-1] for key, value in name_base.items()} #原本是s1 變成 1s
        return name_extra,detect_extra,name_base,detect_base
    
    def marge(self,name_extra:dict,detect_extra:list,name_base:dict,detect_base:list)->str:
        """
            處理yolo的預測結果,將預測到的麻將對照字典後變成合併成字串。
            回傳預測結果的字串->"7m8m1p6p4s9s2z6m"
        """
        output = ""
        for detect in detect_extra:
            classid = detect
            name = name_extra[classid]
            output += f"{name}"
        for detect in detect_base:
            classid = detect
            name = name_base[classid]
            output += f"{name}"
        return output
        
        
    def main(self):
        try:
            name_extra,detect_extra,name_base,detect_base = self.predict(self.model)
            output = self.marge(name_extra,detect_extra,name_base,detect_base)
            print(output)
            if output == "":
                print("沒檢測到")
                return "" , "沒檢測到"
            else:
                tile, win = web_get.get_solution(output)
                print(tile)
                print(win)
            
            return tile, win
        except Exception as e :
            print(e)
            sys.exit(0)
    
    
if __name__ == "__main__":
    yolo_img().main()
