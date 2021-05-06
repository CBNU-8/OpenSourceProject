import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pymysql #따로 설치해주어야한다.

connect = pymysql.connect(host='localhost', user='mySQL이름', password='mySQL비밀번호', db='스케마이름',charset='utf8mb4')
cur = connect.cursor()

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("untitled.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.addcityitem()
        self.city.currentIndexChanged.connect(self.citychoose)
        self.sisul.currentIndexChanged.connect(self.listp)
     
    def addcityitem(self):
        query="SELECT DISTINCT 분류 FROM 스케마이름.테이블이름" 
        cur.execute(query)
        connect.commit()
        
        self.city.addItem('')
        datas = cur.fetchall()
        for data in datas:
            cityname=data[0]
            self.city.addItem(cityname)
                              
    def citychoose(self):
        self.sisul.clear()
        self.sisul.addItem('')
        query="SELECT DISTINCT 개방시설유형구분 FROM 스케마이름.테이블이름 WHERE 분류 like '%s'"%self.city.currentText()
        cur.execute(query)
        connect.commit()
       
        datas = cur.fetchall()
        for data in datas:
            sisulname=data[0]
            self.sisul.addItem(sisulname)
      
    def listp(self):
        self.listWidget.clear()
        if not self.sisul.currentText():
              query="SELECT 개방시설명 FROM 스케마이름.테이블이름 WHERE 분류 like '%s' "%(self.city.currentText())
        else:
              query="SELECT 개방시설명 FROM 스케마이름.테이블이름 WHERE 분류 like '%s' and 개방시설유형구분 like '%s'"%(self.city.currentText(),self.sisul.currentText())
        cur.execute(query)
        connect.commit()         
        
        datas = cur.fetchall()
        for data in datas:
            listname=data[0]
            self.listWidget.addItem(listname)
        
if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
