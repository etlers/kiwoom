import sys
import time
import pandas as pd

from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtGui import *


class Kiwoom(QMainWindow):
    def __init__(self):
        super().__init__()

        # 로그인
        self.kiwoom = QAxWidget()
        self.kiwoom.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

        # OpenAPI+ Event
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.receive_tr_data)

        # GUI 세팅
        self.setWindowTitle("opt10003")
        self.setGeometry(300, 300, 300, 150)

        label = QLabel('종목코드', self)
        label.move(20, 20)

        self.code_edit = QLineEdit(self)
        self.code_edit.move(80, 20)
        self.code_edit.setText('종목코드를 입력하세요')

        btn1 = QPushButton('조회', self)
        btn1.move(190, 20)
        btn1.clicked.connect(self.btn1_clicked)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 60, 280, 80)
        self.text_edit.setEnabled(False)

    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("로그인 성공")

    def btn1_clicked(self):
        code = self.code_edit.text()
        self.text_edit.append("종목코드:" + code)

        # SetInputValue
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드",  code)
        # CommRqData
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)","opt10003_req", "opt10003", 0, "0101")


    def receive_tr_data(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        print("리시브로 들어옴")
        if rqname == "opt10003_req":
            name = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, recordname, 0, "종목명")
            volume = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, recordname, 0, "거래량")
            numStocks = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, recordname, 0, "상장주식")
            prices = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, recordname, 0, "시가")
            moveRate = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, recordname, 0, "고가")
            self.text_edit.append("종목명:" + name.strip())
            self.text_edit.append("거래량:" + volume.strip())
            self.text_edit.append("상장주식:" + numStocks.strip())
            self.text_edit.append("시가:" + prices.strip())
            self.text_edit.append("고가:" + moveRate.strip())


if __name__=="__main__":
    app = QApplication(sys.argv)
    myWindow = Kiwoom()
    myWindow.show()
    #app.exec_()