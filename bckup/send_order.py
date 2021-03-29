""" 주식 주문을 서버로 전송한다.

# 원형
    LONG SendOrder(
        BSTR sRQName,
        BSTR sScreenNo,
        BSTR sAccNo,
        LONG nOrderType,
        BSTR sCode,
        LONG nQty,
        LONG nPrice,
        BSTR sHogaGb,
        BSTR sOrgOrderNo
    )

# 입력 값
    sRQName - 사용자 구분 요청 명
    sScreenNo - 화면번호[4]
    sAccNo - 계좌번호[10]
    nOrderType - 주문유형 (1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정)
    sCode, - 주식종목코드
    nQty – 주문수량
    nPrice – 주문단가
    sHogaGb - 거래구분
    sOrgOrderNo – 원주문번호

# 비고
    sHogaGb
        00:지정가, 03:시장가, 05:조건부지정가, 06:최유리지정가, 07:최우선지정가, 
        10:지정가IOC, 13:시장가IOC, 16:최유리IOC, 
        20:지정가FOK, 23:시장가FOK, 26:최유리FOK, 
        61:장전시간외종가, 62:시간외단일가, 81:장후시간외종가
    "시장가, 최유리지정가, 최우선지정가, 시장가IOC, 최유리IOC, 시장가FOK, 최유리FOK, 장전시간외, 장후시간외 주문"시 주문가격을 입력하지 않습니다    

# 함수 호출
    지정가 매수 - openApi.SendOrder("RQ_1", "0101", "5015123410", 1, "000660", 10, 48500, "00", "");
    시장가 매수 - openApi.SendOrder("RQ_1", "0101", "5015123410", 1, "000660", 10,     0, "03", "");
    매수 정정   - openApi.SendOrder("RQ_1", "0101", "5015123410", 5, "000660", 10, 49500, "00", "1");
    매수 취소   - openApi.SendOrder("RQ_1", "0101", "5015123410", 3, "000660", 10,     0, "00", "2");

# 조회 정보 요청 - openApi.GetCommData("OPT00001", RQName, 0, "현재가");
# 실시간정보 요청 - openApi.GetCommRealData("000660", 10);
# 체결정보 요청 - openApi.GetChejanData(9203);

"""

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
        #self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호",  code)
        # CommRqData
        #self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)","opw00001_req", "opw00001", 0, "0101")
        # 시장가 매수
        self.kiwoom.dynamicCall("SendOrder", "RQ_1", "0101", "8162124111", 1, "221610", 1, 0, "03", "")

    def receive_tr_data(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        print("리시브로 들어옴")
        if rqname == "opw00001_req":
            name = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, recordname, 0, "예수금")
            self.text_edit.append("예수금:" + name.strip())


if __name__=="__main__":
    app = QApplication(sys.argv)
    myWindow = Kiwoom()
    myWindow.show()
    app.exec_()
