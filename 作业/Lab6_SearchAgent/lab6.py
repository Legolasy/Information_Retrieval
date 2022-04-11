# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lab6.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
from datetime import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
import split_word
from  SearchAgent import SearchAgent
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1200, 720)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(30, 70, 541, 31))
        self.lineEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(590, 70, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(30, 120, 900, 540))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(100)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Search"))
        self.pushButton.setText(_translate("Form", "Search"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "docID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Score1"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Score2"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Score3"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Score4"))
        self.pushButton.clicked.connect(lambda: self.func1())
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.HorSectionClicked)  # 表头单击信号
    def func1(self):
        # 同lab4效果
        # 获取数据
        # 获取lineEdit查询语句
        # print(self.lineEdit.text())
        query = self.lineEdit.text()
        #输入为空
        if(len(query)==0):
            self.tableWidget.setRowCount(1)
            newItem1 = QTableWidgetItem("null")
            newItem2 = QTableWidgetItem("null")
            newItem3 = QTableWidgetItem("null")
            newItem4 = QTableWidgetItem("null")
            newItem5 = QTableWidgetItem("null")
            self.tableWidget.setItem(0, 0, newItem1)
            self.tableWidget.setItem(0, 1, newItem2)
            self.tableWidget.setItem(0, 2, newItem3)
            self.tableWidget.setItem(0, 3, newItem4)
            self.tableWidget.setItem(0, 4, newItem5)
            return
        # query = split_word.processChineseSentence(query)
        #print(query)
        obj = SearchAgent()
        obj.load_corpus()
        #obj.readFile()
        # 计算查询时间
        content1 = obj.search_languageModel(query)
        content2=obj.search_improved1(query)
        content3=obj.search_improved2(query)
        content4=obj.search_improved3(query)
        if len(content1) == 0:
            self.tableWidget.setRowCount(1)
            newItem1 = QTableWidgetItem("null")
            newItem2 = QTableWidgetItem("null")
            newItem3 = QTableWidgetItem("null")
            newItem4 = QTableWidgetItem("null")
            newItem5 = QTableWidgetItem("null")
            self.tableWidget.setItem(0, 0, newItem1)
            self.tableWidget.setItem(0, 1, newItem2)
            self.tableWidget.setItem(0, 2, newItem3)
            self.tableWidget.setItem(0, 3, newItem4)
            self.tableWidget.setItem(0, 4, newItem5)
        else:
            # print(len(content))  # 行数
            self.tableWidget.setRowCount(len(content1))
            cnt = 0
            for i in content1:
                print(i.get('docID'))
                #print(content1[i])
                #print(content1[i].get('docID'))
                newItem1 = QTableWidgetItem(str(i.get('docID')))
                newItem2 = QTableWidgetItem(str(i.get('score')))
                self.tableWidget.setItem(cnt, 0, newItem1)
                self.tableWidget.setItem(cnt, 1, newItem2)
                cnt += 1
            cnt=0
            for i in content2:
                print(i)
                newItem = QTableWidgetItem(str(i.get('score')))
                self.tableWidget.setItem(cnt, 2, newItem)
                cnt+=1
            cnt = 0
            for i in content3:
                print(i)
                newItem = QTableWidgetItem(str(i.get('score')))
                self.tableWidget.setItem(cnt, 3, newItem)
                cnt += 1
            cnt = 0
            for i in content4:
                print(i)
                newItem = QTableWidgetItem(str(i.get('score')))
                self.tableWidget.setItem(cnt, 4, newItem)
                cnt += 1

    def HorSectionClicked(self, index):
        print(index)
        # 获取lineEdit查询语句
        # print(self.lineEdit.text())
        query = self.lineEdit.text()
        #query = split_word.processChineseSentence(query)
        obj = SearchAgent()
        #obj.readFile()
        obj.load_corpus()
        content1 = obj.search_languageModel(query)
        content2 = obj.search_improved1(query)
        content3 = obj.search_improved2(query)
        content4 = obj.search_improved3(query)


        # print(len(content))  # 行数
        self.tableWidget.setRowCount(len(content1))
        # print(content)
        #排序
        if(index==1):
            content1.sort(key=lambda k: k['score'], reverse=True)
            cnt = 0
            for i in content1:
                print(i.get('docID'))
                id=i.get('docID')
                for j in content2:
                    if j.get('docID')==id:
                        score2=j.get('score')
                for j in content3:
                    if j.get('docID')==id:
                        score3=j.get('score')
                for j in content4:
                    if j.get('docID')==id:
                        score4=j.get('score')
                newItem1 = QTableWidgetItem(str(i.get('docID')))
                newItem2 = QTableWidgetItem(str(i.get('score')))
                newItem3 = QTableWidgetItem(str(score2))
                newItem4 = QTableWidgetItem(str(score3))
                newItem5 = QTableWidgetItem(str(score4))
                self.tableWidget.setItem(cnt, 0, newItem1)
                self.tableWidget.setItem(cnt, 1, newItem2)
                self.tableWidget.setItem(cnt, 2, newItem3)
                self.tableWidget.setItem(cnt, 3, newItem4)
                self.tableWidget.setItem(cnt, 4, newItem5)
                cnt += 1
        elif index==2:
            content2.sort(key=lambda k: k['score'], reverse=True)
            cnt = 0
            for i in content2:
                print(i.get('docID'))
                id=i.get('docID')
                for j in content1:
                    if j.get('docID')==id:
                        score1=j.get('score')
                for j in content3:
                    if j.get('docID')==id:
                        score3=j.get('score')
                for j in content4:
                    if j.get('docID')==id:
                        score4=j.get('score')
                newItem1 = QTableWidgetItem(str(i.get('docID')))
                newItem3 = QTableWidgetItem(str(i.get('score')))
                newItem2 = QTableWidgetItem(str(score1))
                newItem4 = QTableWidgetItem(str(score3))
                newItem5 = QTableWidgetItem(str(score4))
                self.tableWidget.setItem(cnt, 0, newItem1)
                self.tableWidget.setItem(cnt, 1, newItem2)
                self.tableWidget.setItem(cnt, 2, newItem3)
                self.tableWidget.setItem(cnt, 3, newItem4)
                self.tableWidget.setItem(cnt, 4, newItem5)
                cnt += 1
        elif index==3:
            content3.sort(key=lambda k: k['score'], reverse=True)
            cnt = 0
            for i in content3:
                print(i.get('docID'))
                id = i.get('docID')
                for j in content1:
                    if j.get('docID') == id:
                        score1 = j.get('score')
                for j in content2:
                    if j.get('docID') == id:
                        score2 = j.get('score')
                for j in content4:
                    if j.get('docID') == id:
                        score4 = j.get('score')
                newItem1 = QTableWidgetItem(str(i.get('docID')))
                newItem4 = QTableWidgetItem(str(i.get('score')))
                newItem2 = QTableWidgetItem(str(score1))
                newItem3 = QTableWidgetItem(str(score2))
                newItem5 = QTableWidgetItem(str(score4))
                self.tableWidget.setItem(cnt, 0, newItem1)
                self.tableWidget.setItem(cnt, 1, newItem2)
                self.tableWidget.setItem(cnt, 2, newItem3)
                self.tableWidget.setItem(cnt, 3, newItem4)
                self.tableWidget.setItem(cnt, 4, newItem5)
                cnt += 1
        elif index == 4:
            content4.sort(key=lambda k: k['score'], reverse=True)
            cnt = 0
            for i in content4:
                print(i.get('docID'))
                id = i.get('docID')
                for j in content1:
                    if j.get('docID') == id:
                        score1 = j.get('score')
                for j in content2:
                    if j.get('docID') == id:
                        score2 = j.get('score')
                for j in content3:
                    if j.get('docID') == id:
                        score3 = j.get('score')
                newItem1 = QTableWidgetItem(str(i.get('docID')))
                newItem5 = QTableWidgetItem(str(i.get('score')))
                newItem2 = QTableWidgetItem(str(score1))
                newItem3 = QTableWidgetItem(str(score2))
                newItem4 = QTableWidgetItem(str(score3))
                self.tableWidget.setItem(cnt, 0, newItem1)
                self.tableWidget.setItem(cnt, 1, newItem2)
                self.tableWidget.setItem(cnt, 2, newItem3)
                self.tableWidget.setItem(cnt, 3, newItem4)
                self.tableWidget.setItem(cnt, 4, newItem5)
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