from PyQt6 import QtWidgets, QtGui, QtCore
import sys

class MainWindow(QtWidgets.QWidget):
    def __init__(self, card_list):
       super().__init__()
       self.setWindowTitle('麻將助理')
       self.resize(320,240)
       self.set_ui(card_list)

    def set_ui(self, card_list):
       self.h_layout = QtWidgets.QHBoxLayout() # 建立水平 Layout
       for card in card_list:
           img_label = self.create_card_label(card)
           self.h_layout.addWidget(img_label)
       self.setLayout(self.h_layout)  # 設定主佈局

    def create_card_label(self, card):
       label = QtWidgets.QLabel(self)
       label.setGeometry(20,20,60,90)
       img_path = self.get_card_image_path(card)
       img = QtGui.QPixmap(img_path)
       label.setPixmap(img)  
       return label

    def get_card_image_path(self, card):
       suit = card[-1]  # 牌的花色
       number = card[:-1]  # 牌的數字
       return f'麻將助理/img/{number}{suit}.png'  
       
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    card_list = ['2s','5s','8s','2m','5m','8m','2p','5p','8p','1z','2z','2z']
    window = MainWindow(card_list)
    window.show()
    sys.exit(app.exec())
