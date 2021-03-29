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
        self.setWindowTitle("opt10001")
        self.setGeometry(300, 300, 300, 150)

        label = QLabel('계좌번호', self)
        label.move(20, 20)

        self.code_edit = QLineEdit(self)
        self.code_edit.move(80, 20)
        self.code_edit.setText('계좌번호를 입력하세요')

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
        self.text_edit.append("계좌번호:" + code)
        # SetInputValue
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호",  code)
        # CommRqData
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)","opw00001_req", "opw00001", 0, "0101")

    def receive_tr_data(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        print("리시브로 들어옴")
        if rqname == "opw00001_req":
            avail_amount = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, recordname, 0, "예수금")
            # 앞에 존재하는 '0' 제거 및 ','로 분리
            avail_amount = f'{int(avail_amount):,}'
            self.text_edit.append("예수금:" + avail_amount.strip())


if __name__=="__main__":
    app = QApplication(sys.argv)
    myWindow = Kiwoom()
    myWindow.show()
    app.exec_()