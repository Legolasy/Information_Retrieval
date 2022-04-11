# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

import os
import numpy as np
import math
import re
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

from Lab5.SearchAgent import SearchAgent
from Lab5 import split_word
class Ui_Form(object):
    radionum=3
    def setupUi(self, Form):
        Form.setObjectName("Search")
        Form.resize(1050, 700)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(40, 110, 900, 580))
        self.tableWidget.setObjectName("tableWidget")
        #列数
        self.tableWidget.setColumnCount(2)
        #行数
        self.tableWidget.setRowCount(100)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(40, 70, 401, 31))
        self.lineEdit.setObjectName("lineEdit")
        # self.textEdit = QtWidgets.QTextEdit(Form)
        # self.textEdit.setGeometry(QtCore.QRect(40, 70, 401, 31))
        # self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(460, 70, 93, 28))
        self.pushButton.setObjectName("bt1")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 70, 93, 28))
        self.pushButton_2.setObjectName("bt2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(660, 70, 93, 28))
        self.pushButton_3.setObjectName("bt3")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(450, 10, 311, 51))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(10, 20, 115, 19))
        self.radioButton.setObjectName("rb1")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(110, 20, 115, 19))
        self.radioButton_2.setObjectName("rb2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_3.setGeometry(QtCore.QRect(210, 20, 115, 19))
        self.radioButton_3.setObjectName("rb3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Search"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "DocID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Score"))
        self.pushButton.setText(_translate("Form", "Search"))
        self.pushButton_2.setText(_translate("Form", "Cosine"))
        self.pushButton_3.setText(_translate("Form", "FasterCos"))
        self.radioButton.setText(_translate("Form", "tf"))
        self.radioButton_2.setText(_translate("Form", "wf1"))
        self.radioButton_3.setText(_translate("Form", "wf2"))
        self.pushButton.clicked.connect(lambda: self.func1())
        self.pushButton_2.clicked.connect(lambda :self.func2())
        self.pushButton_3.clicked.connect(lambda: self.func3())
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.HorSectionClicked)  # 表头单击信号
    def func1(self):
        #同lab4效果
        #table改
        self.tableWidget.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        _translate = QtCore.QCoreApplication.translate
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "DocID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "tf-idf"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "wfidf1"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "wfidf2"))
        #获取数据
        # 获取lineEdit查询语句
        # print(self.lineEdit.text())
        query = self.lineEdit.text()
        query=split_word.processChineseSentence(query)
        print(query)
        obj = SearchAgent()
        obj.readFile()
        # 计算查询时间
        start = time.time()
        content = obj.SimpleSeach(query)
        end=time.time()
        print("Search time is ",end="")
        print(end-start)
        if len(content)==0:
            self.tableWidget.setRowCount(1)
            newItem1 = QTableWidgetItem("null")
            newItem2 = QTableWidgetItem("null")
            self.tableWidget.setItem(0, 0, newItem1)
            self.tableWidget.setItem(0, 1, newItem2)
        else:
            #print(len(content))  # 行数
            self.tableWidget.setRowCount(len(content))
            cnt = 0
            for i in content:
                #print(i)
                newItem1 = QTableWidgetItem(str(i.get('docID')))
                newItem2 = QTableWidgetItem(str(i.get('tfidf')))
                newItem3 = QTableWidgetItem(str(i.get('wfidf1')))
                newItem4 = QTableWidgetItem(str(i.get('wfidf2')))
                self.tableWidget.setItem(cnt, 0, newItem1)
                self.tableWidget.setItem(cnt, 1, newItem2)
                self.tableWidget.setItem(cnt, 2, newItem3)
                self.tableWidget.setItem(cnt, 3, newItem4)
                cnt += 1

    def func2(self):
        if self.radioButton.isChecked():
            self.radionum=3
        if self.radioButton_2.isChecked():
            self.radionum=1
        if self.radioButton_3.isChecked():
            self.radionum = 2
        self.tableWidget.setColumnCount(2)
        _translate = QtCore.QCoreApplication.translate
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "DocID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Score"))

        # 获取数据
        # 获取lineEdit查询语句
        # print(self.lineEdit.text())
        query = self.lineEdit.text()
        query = split_word.processChineseSentence(query)
        print(query)
        obj = SearchAgent()
        obj.readFile()
        num=self.radionum
        # 计算查询时间
        start = time.time()
        content = obj.cosine_score(query,num)
        end = time.time()
        print("Search time is ", end="")
        print(end - start)
        if len(content)==0:
            self.tableWidget.setRowCount(1)
            newItem1 = QTableWidgetItem("null")
            newItem2 = QTableWidgetItem("null")
            self.tableWidget.setItem(0, 0, newItem1)
            self.tableWidget.setItem(0, 1, newItem2)
        else:
            # print(content)
            # print(len(content))  # 行数
            self.tableWidget.setRowCount(len(content))
            cnt = 0
            for k,v in content.items():
                newItem1 = QTableWidgetItem(str(k))
                newItem2 = QTableWidgetItem(str(v))
                self.tableWidget.setItem(cnt, 0, newItem1)
                self.tableWidget.setItem(cnt, 1, newItem2)
                cnt += 1
    def func3(self):
        if self.radioButton.isChecked():
            self.radionum=3
        if self.radioButton_2.isChecked():
            self.radionum=1
        if self.radioButton_3.isChecked():
            self.radionum = 2
        self.tableWidget.setColumnCount(2)
        _translate = QtCore.QCoreApplication.translate
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "DocID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Score"))
        # 获取数据
        # 获取lineEdit查询语句
        # print(self.lineEdit.text())
        query = self.lineEdit.text()
        query = split_word.processChineseSentence(query)
        print(query)
        obj = SearchAgent()
        obj.readFile()
        #选择权重计算方式 默认tf
        num=self.radionum
        # 计算查询时间
        start = time.time()
        content = obj.faster_cosine_score(query, num)
        end = time.time()
        print("Search time is ", end="")
        print(end - start)
        if len(content)==0:
            self.tableWidget.setRowCount(1)
            newItem1 = QTableWidgetItem("null")
            newItem2 = QTableWidgetItem("null")
            self.tableWidget.setItem(0, 0, newItem1)
            self.tableWidget.setItem(0, 1, newItem2)
        else:
            # print(content)
            # print(len(content))  # 行数
            self.tableWidget.setRowCount(len(content))
            cnt = 0
            for k, v in content.items():
                newItem1 = QTableWidgetItem(str(k))
                newItem2 = QTableWidgetItem(str(v))
                self.tableWidget.setItem(cnt, 0, newItem1)
                self.tableWidget.setItem(cnt, 1, newItem2)
                cnt += 1
    def HorSectionClicked(self, index):
        print(index)
        # 获取lineEdit查询语句
        # print(self.lineEdit.text())
        query = self.lineEdit.text()
        query = split_word.processChineseSentence(query)
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