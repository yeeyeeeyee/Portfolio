import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,QPlainTextEdit
import yolo_img
import threading
        

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 設置窗口標題和大小
        self.setWindowTitle('PyQt6 Example')
        self.setGeometry(100, 100, 600, 400)

        # 創建標籤和按鈕
        label1 = QLabel('向聽數')
        self.result1 = QLabel('')
        label2 = QLabel('策略')
        self.result2 = QPlainTextEdit("")
        self.result2.setReadOnly(True)
        button = QPushButton('按鈕')

        # 設置標籤和按鈕的文字
        label1.setText('向聽數')
        label2.setText('策略')
        button.setText('偵測')

        # 創建佈局並添加小部件
        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(self.result1)
        layout.addWidget(label2)
        layout.addWidget(self.result2)
        layout.addWidget(button)

        # 設置窗口佈局
        self.setLayout(layout)

        # 連接按鈕的點擊事件到槽函數
        button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        thread = threading.Thread(target=self.run_yolo)
        thread.start()
        

    def run_yolo(self):
        print("偵測開始")
        self.hide()
        yolo = yolo_img.yolo_img()
        tile,win = yolo.main()
        self.result1.setText(win)
        self.result2.setPlainText(tile)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
