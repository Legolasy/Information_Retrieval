# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

from Lab4_tfidf.SearchAgent import SearchAgent


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 618)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 441, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(470, 40, 131, 31))
        self.pushButton.setObjectName("pushButton")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(20, 90, 880, 480))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)

        #动态读取行数
        self.tableWidget.setRowCount(100)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Search"))
        self.pushButton.setText(_translate("Form", "Search"))
        self.pushButton.clicked.connect(lambda :self.func())

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "docID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "tfidf"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "wfidf1"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "wfidf2"))

        self.tableWidget.horizontalHeader().sectionClicked.connect(self.HorSectionClicked)  # 表头单击信号

    def func(self):
        #获取lineEdit查询语句
        #print(self.lineEdit.text())
        query=self.lineEdit.text()
        obj = SearchAgent()
        obj.readFile()
        content = obj.SimpleSeach(query)
        print(len(content))#行数
        self.tableWidget.setRowCount(len(content))
        cnt=0
        for i in content:
            print(i)
            newItem1 = QTableWidgetItem(str(i.get('docID')))
            newItem2 = QTableWidgetItem(str(i.get('tfidf')))
            newItem3 = QTableWidgetItem(str(i.get('wfidf1')))
            newItem4 = QTableWidgetItem(str(i.get('wfidf2')))

            self.tableWidget.setItem(cnt, 0, newItem1)
            self.tableWidget.setItem(cnt, 1, newItem2)
            self.tableWidget.setItem(cnt, 2, newItem3)
            self.tableWidget.setItem(cnt, 3, newItem4)
            cnt+=1

    def HorSectionClicked(self, index):
        print(index)
        # 获取lineEdit查询语句
        # print(self.lineEdit.text())
        query = self.lineEdit.text()
        obj = SearchAgent()
        obj.readFile()
        content = obj.SimpleSeach(query)
        # print(len(content))  # 行数
        self.tableWidget.setRowCount(len(content))
        # print(content)
        #tf-idf排序
        if(index==1):
            content=sorted(content,key=lambda x:x["tfidf"],reverse=True)
        elif index==2:
            content = sorted(content, key=lambda x: x["wfidf1"], reverse=True)
        elif index==3:
            content = sorted(content, key=lambda x: x["wfidf2"], reverse=True)
        cnt=0
        for i in content:
            print(i)
            newItem1 = QTableWidgetItem(str(i.get('docID')))
            newItem2 = QTableWidgetItem(str(i.get('tfidf')))
            newItem3 = QTableWidgetItem(str(i.get('wfidf1')))
            newItem4 = QTableWidgetItem(str(i.get('wfidf2')))

            self.tableWidget.setItem(cnt, 0, newItem1)
            self.tableWidget.setItem(cnt, 1, newItem2)
            self.tableWidget.setItem(cnt, 2, newItem3)
            self.tableWidget.setItem(cnt, 3, newItem4)
            cnt += 1






if __name__=="__main__":
    import sys
    #输入查询
    #返回结果
    #结果排序


    app=QtWidgets.QApplication(sys.argv)
    widget=QtWidgets.QWidget()
    ui=Ui_Form()
    ui.setupUi(widget)
    widget.show()

    sys.exit(app.exec_())
