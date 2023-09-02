# 主程序：UI实现及功能连接

import sys, time,json,os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QStackedLayout, QComboBox, QCalendarWidget, QApplication, QWidget, QPushButton, QLabel, QLineEdit, QDesktopWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QRadioButton, QGridLayout, QMainWindow
import numpy as np
import pandas as pd
from PyQt5 import sip
import add
import find
import sort
import delete
import file_process
from SMPT_birthday_mails import selectPerson,sendMail
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# 创建存储数据的列表，所有的数据有一个列表, 每个类别也有一个列表
global all_data
all_data = []
global stu_data
stu_data = []
global family_data
family_data = []
global professor_data
professor_data = []
global colleague_data
colleague_data = []
global friend_data
friend_data = []
#存储所有联系人的电话 phone_list
global phone_list
phone_list = []
#存储目前置顶联系人的个数 count
global count
count = 0

global all_df
all_df = pd.DataFrame()
global schoolmate_df
schoolmate_df = pd.DataFrame()
global professor_df
professor_df = pd.DataFrame()
global friend_df
friend_df = pd.DataFrame()
global colleague_df
colleague_df = pd.DataFrame()
global family_df
family_df = pd.DataFrame()
global others_df
others_df = pd.DataFrame()


# 程序开始，读取excel表格内初始化数据
all_df, schoolmate_df, professor_df, friend_df, colleague_df, family_df, others_df = file_process.getData(filepath = 'data.xls')


# ----------------------------------------1 主界面模块---------------------------------------------

class mainWindow(QtWidgets.QWidget):

    def __init__(self,lst):
        super().__init__()

        self.resize(800,800)
        self.hlayout = QtWidgets.QHBoxLayout(self)
        self.lst = lst
        if os.path.exists("data.json"):
            pass
        else:
            self.saveJson({
                "Note":[]
            })
        self.readJson()
        self.allWidget()
        self.tableWidget.clicked.connect(self.panding)
    
    
    # 主界面UI
    def allWidget(self):

        self.container = QVBoxLayout()
        self.upper_box = self.newUpperWidget()
        self.lower_box = self.newTableWidget()
        self.hlayout.addWidget(self.tableWidget)
        self.lower_box.setLayout(self.hlayout)

        self.container.addWidget(self.upper_box)
        self.container.addWidget(self.lower_box)

        self.setLayout(self.container)

        self.resize(800, 400)

        self.setWindowTitle('通讯录主界面')


    # 主界面上侧--下拉框、输入框、按钮UI设计
    def newUpperWidget(self):

        self.upper_box = QGroupBox("")
        self.upper_box_layout = QHBoxLayout()

        self.choose_type_label = QLabel()
        self.choose_type_label.setText('选择搜索联系人的标签')

        self.btn2 = QLabel('')
        self.search_type = QComboBox()
        self.search_type.addItem('全部')
        self.search_type.addItem('同学')
        self.search_type.addItem('家人')
        self.search_type.addItem('老师')
        self.search_type.addItem('同事')
        self.search_type.addItem('朋友')
        self.search_type.addItem('其他')
        self.search_type.currentIndexChanged.connect(self.selectionchange_search)

        
        self.fuzzy_search = QLineEdit()
        self.fuzzy_search.setPlaceholderText("输入搜索信息")
        self.search_btn = QPushButton('搜索', self)
        self.search_btn.clicked.connect(self.refrsh_search)


        self.btn1 = QLabel('')
        self.choose_classification = QComboBox()
        self.choose_classification.addItem('按姓名排序')
        
        self.choose_classification.addItem('按年龄排序')
        self.choose_classification.addItem('同学按专业排序')
        self.choose_classification.addItem('老师按学院、职务排序')
        self.choose_classification.addItem('同事按公司、部门排序')
        self.choose_classification.addItem('亲戚按亲属关系排序')
        self.choose_classification.currentIndexChanged.connect(self.selectionchange)

        self.sort_btn = QPushButton('排序', self)
        self.sort_btn.clicked.connect(self.refrsh)
        


        self.Top_btn = QPushButton('置顶星标联系人',self)
        self.Top_btn.clicked.connect(self.zhiding)


        self.add_new_btn = QPushButton('新建联系人',self)
        self.add_new_btn.clicked.connect(self.show_add_new)
        self.child_window = addNewContacts()


        self.upper_box_layout.addWidget(self.choose_type_label)
        self.upper_box_layout.addWidget(self.search_type)
        self.upper_box_layout.addWidget(self.fuzzy_search)
        self.upper_box_layout.addWidget(self.search_btn)
        self.upper_box_layout.addStretch()
        self.upper_box_layout.addWidget(self.choose_classification)
        self.upper_box_layout.addWidget(self.sort_btn)
        self.upper_box_layout.addStretch()
        self.upper_box_layout.addWidget(self.Top_btn)
        self.upper_box_layout.addWidget(self.add_new_btn)

        self.upper_box.setLayout(self.upper_box_layout)
        return self.upper_box


    # 主页面上侧按钮--置顶星标联系人
    def panding(self):
        name = self.tableWidget.item(self.tableWidget.currentRow(),1).text()
        if str(name) in self.jsonData["Note"] or int(name) in self.jsonData["Note"]:
            self.Top_btn.setText("取消置顶星标联系人")
        else:
            self.Top_btn.setText("置顶星标联系人")


    

    # 表格内控件
    def show_add_new(self):
        self.child_window.show()
    

    # 表格内按钮--查看详细信息按钮
    def buttonForRow(self,i):

        widget = QtWidgets.QWidget()

        self.detailBtn = QtWidgets.QPushButton('查看详细信息')
        self.detailBtn.setStyleSheet(''' text-align : center;
                                    background-color : LightCyan;
                                    height : 30px;
                                    border-style: outset;
                                    font : 13px; ''')

        self.detailBtn.clicked.connect(lambda :self.show_datail(i))

        
        self.deleteBtn = QtWidgets.QPushButton('删除')
        self.deleteBtn.setStyleSheet(''' text-align : center;
                                    background-color : Mistyrose;
                                    height : 30px;
                                    border-style: outset;
                                    font : 13px; ''')

        self.deleteBtn.clicked.connect(self.delete_clicked)

        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(self.detailBtn)
        hLayout.addWidget(self.deleteBtn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    # 刷新表格显示内容
    def refrsh(self):
        try:
            sip.delete(self.tableWidget)
        except:
            pass
        self.newTableWidget()
        self.hlayout.addWidget(self.tableWidget)
    
    



    # 显示详细信息--功能实现：判断联系人类型
    def show_datail(self,i):

        ids = int(self.tableWidget.item(i,1).text())
        #查找分类
        if list(schoolmate_df[schoolmate_df["phone"]==ids].index) != []:
            dpTemp = schoolmate_df[schoolmate_df["phone"]==ids]
        elif list(professor_df[professor_df["phone"]==ids].index) != []:
            dpTemp = professor_df[professor_df["phone"]==ids]
        elif list(friend_df[friend_df["phone"]==ids].index) != []:
            dpTemp = friend_df[friend_df["phone"]==ids]
        elif list(colleague_df[colleague_df["phone"]==ids].index) != []:
            dpTemp = colleague_df[colleague_df["phone"]==ids]
        elif list(family_df[family_df["phone"]==ids].index) != []:
            dpTemp = family_df[family_df["phone"]==ids]
        elif list(others_df[others_df["phone"]==ids].index) != []:
            dpTemp = others_df[others_df["phone"]==ids]
        try:
            if dpTemp:
                pass
        except:
            ids = self.tableWidget.item(i, 1).text()
            # 查找分类
            if list(schoolmate_df[schoolmate_df["phone"] == ids].index) != []:
                dpTemp = schoolmate_df[schoolmate_df["phone"] == ids]
            elif list(professor_df[professor_df["phone"] == ids].index) != []:
                dpTemp = professor_df[professor_df["phone"] == ids]
            elif list(friend_df[friend_df["phone"] == ids].index) != []:
                dpTemp = friend_df[friend_df["phone"] == ids]
            elif list(colleague_df[colleague_df["phone"] == ids].index) != []:
                dpTemp = colleague_df[colleague_df["phone"] == ids]
            elif list(family_df[family_df["phone"] == ids].index) != []:
                dpTemp = family_df[family_df["phone"] == ids]
            elif list(others_df[others_df["phone"] == ids].index) != []:
                dpTemp = others_df[others_df["phone"] == ids]
        self.child_window_detail = showDetailInfo(dpTemp)
        self.child_window_detail.show()




    # 删除联系人--功能实现
    def delete_clicked(self):
        global all_df

        global schoolmate_df

        global professor_df

        global friend_df

        global colleague_df

        global family_df

        global others_df

        button = self.sender()

        if button:
            row = self.tableWidget.indexAt(button.parent().pos()).row()
            column = self.tableWidget.indexAt(button.parent().pos()).column()
            delete_phone = self.tableWidget.item(row, 1).text()
            if delete_phone in self.jsonData["Note"]:
                self.jsonData["Note"].remove(delete_phone)
                self.saveJson(self.jsonData)
            print(delete_phone)
            self.tableWidget.removeRow(row)
            all_df, schoolmate_df, professor_df, friend_df, colleague_df, family_df, others_df = delete.delete(delete_phone, all_df, schoolmate_df, professor_df, friend_df, colleague_df, family_df, others_df, phone_list)
            print(friend_df)
            type = self.selectionchange()
            self.excel2list(type)

            input_list = self.excel2list(type)

            self.lower_box = QGroupBox("")

            self.tableWidget = QtWidgets.QTableWidget()
            self.tableWidget.setRowCount(len(input_list))
            self.tableWidget.setColumnCount(len(self.lst))
            self.tableWidget.setHorizontalHeaderLabels(self.lst)
        
            # 使列表自适应宽度
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  
            # 设置tablewidget不可编辑
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            # 设置tablewidget不可选中
            self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

            dsp = self.jsonData["Note"]
            specialList = []
            for i in input_list:
                if str(i[1]) in dsp or int(i[1]) in dsp:
                    specialList.append(i)
            for i in specialList:
                input_list.remove(i)
            input_list = specialList + input_list


            for i in range(len(input_list)):
                if str(input_list[i][1]) in dsp:
                    for j in range(len(input_list[0])):
                        self.tableWidget.item(i, j).setBackground(QBrush(QColor(255, 153, 153)))
                for j in range(len(input_list[0])):
                    newItem = QTableWidgetItem(str(input_list[i][j]))
                    self.tableWidget.setItem(i, j, newItem)
                self.tableWidget.setCellWidget(i, len(self.lst) - 1, self.buttonForRow(i))
            # 在最后一个单元格中加入修改、删除按钮

            return self.lower_box



    # 排序--下拉框功能实现
    def selectionchange(self):
        #排序
        #标签用来显示选中的文本
        #currentText()：返回选中选项的文本
        self.btn1.setText(self.choose_classification.currentText())

        self.index = self.choose_classification.currentIndex()
        self.current_lable_for_sort = self.choose_classification.itemText(self.index)

        return self.current_lable_for_sort
    
    # 搜索--下拉框功能实现
    def selectionchange_search(self):
        #搜索
        #标签用来显示选中的文本
        #currentText()：返回选中选项的文本
        self.btn1.setText(self.search_type.currentText())

        self.index_two = self.search_type.currentIndex()
        self.current_lable_for_search = self.search_type.itemText(self.index_two)

        return self.current_lable_for_search

 


    # 置顶星标联系人--功能实现
    def zhiding(self):
        global all_df

        global schoolmate_df

        global professor_df

        global friend_df

        global colleague_df

        global family_df

        global others_df
        phone = self.tableWidget.item(self.tableWidget.currentRow(), 1).text()
        if self.Top_btn.text() == "置顶星标联系人":
            colName = list(all_df.columns)
            try:
                row = all_df[all_df["phone"] == phone].index.values[0]
                temp = all_df.loc[row]
                all_df = all_df.drop(axis=0, index=row)
                all_df = pd.DataFrame(np.insert(all_df.values, 0, values=list(temp), axis=0))
            except:
                phone = int(phone)
                row = all_df[all_df["phone"] == phone].index.values[0]
                temp = all_df.loc[row]
                all_df = all_df.drop(axis=0, index=row)
                all_df = pd.DataFrame(np.insert(all_df.values, 0, values=list(temp), axis=0))
            all_df.columns = colName
            if list(schoolmate_df[schoolmate_df["phone"] == phone].index) != []:
                colName = list(schoolmate_df.columns)
                row = schoolmate_df[schoolmate_df["phone"] == phone].index.values[0]
                temp = schoolmate_df.loc[row]
                schoolmate_df = schoolmate_df.drop(axis=0, index=row)
                schoolmate_df = pd.DataFrame(np.insert(schoolmate_df.values, 0, values=list(temp), axis=0))
                schoolmate_df.columns = colName
            elif list(professor_df[professor_df["phone"] == phone].index) != []:
                colName = list(professor_df.columns)
                row = professor_df[professor_df["phone"] == phone].index.values[0]
                temp = professor_df.loc[row]
                professor_df = professor_df.drop(axis=0, index=row)
                professor_df = pd.DataFrame(np.insert(professor_df.values, 0, values=list(temp), axis=0))
                professor_df.columns = colName
            elif list(friend_df[friend_df["phone"] == phone].index) != []:
                colName = list(friend_df.columns)
                row = friend_df[friend_df["phone"] == phone].index.values[0]
                temp = friend_df.loc[row]
                friend_df = friend_df.drop(axis=0, index=row)
                friend_df = pd.DataFrame(np.insert(friend_df.values, 0, values=list(temp), axis=0))
                friend_df.columns = colName
            elif list(colleague_df[colleague_df["phone"] == phone].index) != []:
                row = colleague_df[colleague_df["phone"] == phone].index.values[0]
                colName = list(colleague_df.columns)
                temp = colleague_df.loc[row]
                colleague_df = colleague_df.drop(axis=0, index=row)
                colleague_df = pd.DataFrame(np.insert(colleague_df.values, 0, values=list(temp), axis=0))
                colleague_df.columns = colName
            elif list(family_df[family_df["phone"] == phone].index) != []:
                row = family_df[family_df["phone"] == phone].index.values[0]
                colName = list(family_df.columns)
                temp = family_df.loc[row]
                family_df = family_df.drop(axis=0, index=row)
                family_df = pd.DataFrame(np.insert(family_df.values, 0, values=list(temp), axis=0))
                family_df.columns = colName
            elif list(others_df[others_df["phone"] == phone].index) != []:
                row = others_df[others_df["phone"] == phone].index.values[0]
                temp = others_df.loc[row]
                colName = list(others_df.columns)
                others_df = others_df.drop(axis=0, index=row)
                others_df = pd.DataFrame(np.insert(others_df.values, 0, values=list(temp), axis=0))
                others_df.columns = colName
            self.jsonData["Note"].append(phone)
            self.saveJson(self.jsonData)
            self.Top_btn.setText("取消置顶星标联系人")
            file_process.saveData(all_df, schoolmate_df, professor_df, friend_df, colleague_df, family_df, others_df, filepath = 'data.xls' )

        else:
            try:
                row = all_df[all_df["phone"] == phone].index.values[0]
                temp = all_df.loc[row]
                colName = list(all_df.columns)
                all_df = all_df.drop(axis=0, index=row)
                all_df = pd.DataFrame(np.insert(all_df.values, -1, values=list(temp), axis=0))

            except:
                phone = int(phone)
                row = all_df[all_df["phone"] == phone].index.values[0]
                temp = all_df.loc[row]
                colName = list(all_df.columns)
                all_df = all_df.drop(axis=0, index=row)
                all_df = pd.DataFrame(np.insert(all_df.values, -1, values=list(temp), axis=0))
            all_df.columns = colName
            if list(schoolmate_df[schoolmate_df["phone"] == phone].index) != []:
                colName = list(schoolmate_df.columns)
                row = schoolmate_df[schoolmate_df["phone"] == phone].index.values[0]
                temp = schoolmate_df.loc[row]
                schoolmate_df = schoolmate_df.drop(axis=0, index=row)
                schoolmate_df = pd.DataFrame(np.insert(schoolmate_df.values, -1, values=list(temp), axis=0))
                schoolmate_df.columns = colName
            elif list(professor_df[professor_df["phone"] == phone].index) != []:
                colName = list(professor_df.columns)
                row = professor_df[professor_df["phone"] == phone].index.values[0]
                temp = professor_df.loc[row]
                professor_df = professor_df.drop(axis=0, index=row)
                professor_df = pd.DataFrame(np.insert(professor_df.values, -1, values=list(temp), axis=0))
                professor_df.columns = colName
            elif list(friend_df[friend_df["phone"] == phone].index) != []:
                colName = list(friend_df.columns)
                row = friend_df[friend_df["phone"] == phone].index.values[0]
                temp = friend_df.loc[row]
                friend_df = friend_df.drop(axis=0, index=row)
                friend_df = pd.DataFrame(np.insert(friend_df.values, -1, values=list(temp), axis=0))
                friend_df.columns = colName
            elif list(colleague_df[colleague_df["phone"] == phone].index) != []:
                row = colleague_df[colleague_df["phone"] == phone].index.values[0]
                colName = list(colleague_df.columns)
                temp = colleague_df.loc[row]
                colleague_df = colleague_df.drop(axis=0, index=row)
                colleague_df = pd.DataFrame(np.insert(colleague_df.values, -1, values=list(temp), axis=0))
                colleague_df.columns = colName
            elif list(family_df[family_df["phone"] == phone].index) != []:
                row = family_df[family_df["phone"] == phone].index.values[0]
                colName = list(family_df.columns)
                temp = family_df.loc[row]
                family_df = family_df.drop(axis=0, index=row)
                family_df = pd.DataFrame(np.insert(family_df.values, -1, values=list(temp), axis=0))
                family_df.columns = colName
            elif list(others_df[others_df["phone"] == phone].index) != []:
                row = others_df[others_df["phone"] == phone].index.values[0]
                temp = others_df.loc[row]
                colName = list(others_df.columns)
                others_df = others_df.drop(axis=0, index=row)
                others_df = pd.DataFrame(np.insert(others_df.values, -1, values=list(temp), axis=0))
                others_df.columns = colName

            self.Top_btn.setText("置顶星标联系人")
            self.jsonData["Note"].remove(phone)
            self.saveJson(self.jsonData)

        win.refrsh()
    
    # 置顶联系人--读取json数据
    def readJson(self):
        with open("data.json", encoding="utf-8") as f:
            self.jsonData = json.load(f)

    # 置顶联系人--更新json数据
    def saveJson(self,data):
        with open("data.json", "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写为多行

  


        
    # 搜索--将需要显示的数据转为list格式
    def excel2list_search(self, type_search):
        global all_df

        global schoolmate_df

        global professor_df

        global friend_df

        global colleague_df

        global family_df

        global others_df

        type_search = self.selectionchange_search()
        content = self.fuzzy_search.text()


        if type_search == '全部':
            self.data = find.find_single_vague(all_df, 'all', content).iloc[ : ,0:2]
            self.data_list = self.data.values.tolist()

        if type_search == '同学':
            self.data = find.find_single_vague(schoolmate_df, 'student', content).iloc[ : ,0:2]
            self.data_list = self.data.values.tolist()

        if type_search == '家人':
            self.data = find.find_single_vague(family_df, 'family', content).iloc[ : ,0:2]
            self.data_list = self.data.values.tolist()

        if type_search == '老师':
            self.data = find.find_single_vague(professor_df, 'professor', content).iloc[ : ,0:2]
            self.data_list = self.data.values.tolist()

        if type_search == '同事':
            self.data = find.find_single_vague(colleague_df, 'colleague', content).iloc[ : ,0:2]
            self.data_list = self.data.values.tolist()

        if type_search == '朋友':
            self.data = find.find_single_vague(friend_df, 'friend', content).iloc[ : ,0:2]
            self.data_list = self.data.values.tolist()
        
        if type_search == '其他':
            self.data = find.find_single_vague(others_df, 'others', content).iloc[ : ,0:2]
            self.data_list = self.data.values.tolist()
        

        return self.data_list

    # 搜索--更新搜索后表格内容
    def refrsh_search(self):
        try:
            sip.delete(self.tableWidget)
        except:
            pass
        self.newTableWidget_search()
        self.hlayout.addWidget(self.tableWidget)
    
    # 主界面表格--显示搜索后表格内容
    def newTableWidget_search(self):

        type_search = self.selectionchange_search()
        
        input_list_search = self.excel2list_search(type_search)
        

        self.lower_box = QGroupBox("")

        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setRowCount(len(input_list_search))
        self.tableWidget.setColumnCount(len(self.lst))
        self.tableWidget.setHorizontalHeaderLabels(self.lst)
        

        # 使列表自适应宽度
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  
        # 设置tablewidget不可编辑
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置tablewidget不可选中
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        dsp = self.jsonData["Note"]
        specialList = []
        for i in input_list_search:
            if str(i[1]) in dsp or int(i[1]) in dsp:
                specialList.append(i)
        for i in specialList:
            input_list_search.remove(i)
        input_list_search = specialList + input_list_search
        
        for i in range(len(input_list_search)):
            if str(input_list_search[i][1]) in dsp:
                for j in range(len(input_list_search[0])):
                    self.tableWidget.item(i, j).setBackground(QBrush(QColor(255, 153, 153)))
            for j in range(len(input_list_search[0])):
                newItem = QTableWidgetItem(str(input_list_search[i][j]))
                self.tableWidget.setItem(i, j, newItem)
            self.tableWidget.setCellWidget(i, len(self.lst) - 1, self.buttonForRow(i))
            # 在最后一个单元格中加入修改、删除按钮

        return self.lower_box



    
    # 排序--将需要显示的数据转为list格式
    def excel2list(self, type):
        global all_df

        global schoolmate_df

        global professor_df

        global friend_df

        global colleague_df

        global family_df

        global others_df

        type = self.selectionchange()

        if type == '按姓名排序':
            self.data = sort.name_sort(all_df, phone_list).iloc[ : ,0:2]
            self.data_list = self.data.values.tolist()

        if type == '按年龄排序':
            self.data = sort.birthday_sort(all_df, phone_list).iloc[ : ,0:2]
            self.data_list = self.data.values.tolist()

        if type == '同学按专业排序':
            self.data = sort.student_major_sort(schoolmate_df).iloc[ : ,0:2]
            self.data_list = self.data.values.tolist()

        if type == '老师按学院、职务排序':
            self.data = sort.professor_college_sort(professor_df).iloc[ : ,0:2]
            self.data_list = self.data.values.tolist()

        if type == '同事按公司、部门排序':
            self.data = sort.colleague_company_sort(colleague_df).iloc[ : ,0:2]
            self.data_list = self.data.values.tolist()

        if type == '亲戚按亲属关系排序':
            self.data = sort.name_sort(family_df, phone_list).iloc[ : ,0:2]
            self.data_list = self.data.values.tolist()

        return self.data_list

    # 主界面表格--显示排序后表格内容
    def newTableWidget(self):

        ###### 下方表格
        type = self.selectionchange()
        input_list = self.excel2list(type)

        self.lower_box = QGroupBox("")

        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setRowCount(len(input_list))
        self.tableWidget.setColumnCount(len(self.lst))
        self.tableWidget.setHorizontalHeaderLabels(self.lst)
        
        #self.tableWidget.verticalHeader()->setDefaultSectionSize(20)
        # 使列表自适应宽度
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  
        # 设置tablewidget不可编辑
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置tablewidget不可选中
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        dsp = self.jsonData["Note"]
        specialList = []
        for i in input_list:
            if str(i[1]) in dsp or int(i[1]) in dsp:
                specialList.append(i)
        for i in specialList:
            input_list.remove(i)
        input_list = specialList + input_list


        for i in range(len(input_list)):
            for j in range(len(input_list[0])):
                newItem = QTableWidgetItem(str(input_list[i][j]))
                self.tableWidget.setItem(i, j, newItem)
            self.tableWidget.setCellWidget(i, len(self.lst) - 1, self.buttonForRow(i))
            if str(input_list[i][1]) in dsp or int(input_list[i][1]) in dsp:
                for j in range(len(input_list[0])):
                    self.tableWidget.item(i, j).setBackground(QBrush(QColor(255, 153, 153)))

            # 在最后一个单元格中加入修改、删除按钮


        return self.lower_box
   

# ---------------------------------------1 主界面模块结束--------------------------------------------



# ---------------------------------------2 新增联系人模块---------------------------------------------

# 新增联系人--子窗口UI及功能实现
class addNewContacts(QWidget):
    global all_data
    all_data = []
    global stu_data
    stu_data = []
    global family_data
    family_data = []
    global professor_data
    professor_data = []
    global colleague_data
    colleague_data = []
    global friend_data
    friend_data = []

    global all_df

    global schoolmate_df

    global professor_df

    global friend_df

    global colleague_df

    global family_df

    global others_df

    
    def __init__(self):
        super().__init__()
        self.remarks_ui()
        self.add_new_ui()
        self.attach_label = ''
        #self.table = table
    
    # 输入框UI实现
    def remarks_ui(self):
        self.stacked_layout = QStackedLayout()

        self.remarks_box1 = QGroupBox("添加同学备注信息")
        self.remarks_layout1 = QVBoxLayout()
        self.school1 = QLineEdit()
        self.college1 = QLineEdit()
        self.major1 = QLineEdit()
        self.grade1 = QLineEdit()

        self.school1.setPlaceholderText("学校")
        self.college1.setPlaceholderText("学院")
        self.major1.setPlaceholderText("专业")
        self.grade1.setPlaceholderText("年级")

        self.remarks_layout1.addWidget(self.school1)
        self.remarks_layout1.addWidget(self.college1)
        self.remarks_layout1.addWidget(self.major1)
        self.remarks_layout1.addWidget(self.grade1)

        self.remarks_box1.setLayout(self.remarks_layout1)

        self.remarks_box2 = QGroupBox("添加家人备注信息")
        self.remarks_layout2 = QVBoxLayout()
        self.address = QLineEdit()
        self.relationship = QLineEdit()
        self.relationship.setPlaceholderText("关系")
        self.address.setPlaceholderText("家庭住址")

        self.remarks_layout2.addWidget(self.relationship)
        self.remarks_layout2.addWidget(self.address)

        self.remarks_box2.setLayout(self.remarks_layout2)

        self.remarks_box3 = QGroupBox("添加老师备注信息")
        self.remarks_layout3 = QVBoxLayout()
        self.school2 = QLineEdit()
        self.college2 = QLineEdit()
        self.post2 = QLineEdit()

        self.school2.setPlaceholderText("学校")
        self.college2.setPlaceholderText("学院")
        self.post2.setPlaceholderText("职务")

        self.remarks_layout3.addWidget(self.school2)
        self.remarks_layout3.addWidget(self.college2)
        self.remarks_layout3.addWidget(self.post2)

        self.remarks_box3.setLayout(self.remarks_layout3)

        self.remarks_box4 = QGroupBox("添加同事备注信息")
        self.remarks_layout4 = QVBoxLayout()
        self.company = QLineEdit()
        self.department = QLineEdit()
        self.job = QLineEdit()

        self.company.setPlaceholderText("公司")
        self.department.setPlaceholderText("部门")
        self.job.setPlaceholderText("职务")

        self.remarks_layout4.addWidget(self.company)
        self.remarks_layout4.addWidget(self.department)
        self.remarks_layout4.addWidget(self.job)

        self.remarks_box4.setLayout(self.remarks_layout4)

        self.remarks_box5 = QGroupBox("添加朋友备注信息")
        self.remarks_layout5 = QVBoxLayout()
        self.meet_time = QLineEdit()
        self.how_we_met = QLineEdit()

        self.meet_time.setPlaceholderText("认识时间")
        self.how_we_met.setPlaceholderText("认识方式")

        self.remarks_layout5.addWidget(self.meet_time)
        self.remarks_layout5.addWidget(self.how_we_met)

        self.remarks_box5.setLayout(self.remarks_layout5)

        self.remarks_box6 = QGroupBox("添加其他备注信息")
        self.remarks_layout6 = QVBoxLayout()
        self.other_remark = QLineEdit()

        self.other_remark.setPlaceholderText("填写备注信息")
        self.remarks_layout6.addWidget(self.other_remark)
        self.remarks_box6.setLayout(self.remarks_layout6)

        self.stacked_layout.addWidget(self.remarks_box1)
        self.stacked_layout.addWidget(self.remarks_box2)
        self.stacked_layout.addWidget(self.remarks_box3)
        self.stacked_layout.addWidget(self.remarks_box4)
        self.stacked_layout.addWidget(self.remarks_box5)
        self.stacked_layout.addWidget(self.remarks_box6)

    # 总UI实现
    def add_new_ui(self):

        # 创建一个大的垂直布局器
        self.container = QVBoxLayout()

        # 创建基本信息模块,4个基本信息姓氏、名字、电话、性别
        # 其中，姓氏，名字，电话使用垂直布局，性别使用水平布局。两部分总体上采用垂直布局

        # basic_info_box是用于获取姓氏，名字，电话的第一个垂直布局的模块
        self.basic_info_box = QGroupBox("基本信息")
        self.basic_info_layout = QVBoxLayout()
        self.name = QLineEdit()
        self.phone_number = QLineEdit()
        self.email = QLineEdit()
        self.birthday = QLineEdit()

        self.name.setPlaceholderText("姓名")
        self.phone_number.setPlaceholderText("电话")
        self.email.setPlaceholderText("邮箱")
        self.birthday.setPlaceholderText("生日")


        self.basic_info_layout.addWidget(self.name)
        self.basic_info_layout.addWidget(self.phone_number)
        self.basic_info_layout.addWidget(self.email)
        self.basic_info_layout.addWidget(self.birthday)

        self.basic_info_box.setLayout(self.basic_info_layout)


        self.gender_info_box = QGroupBox("性别")
        self.gender_layout = QHBoxLayout()
        self.button_male = QRadioButton("男")
        self.button_female = QRadioButton("女")
        self.button_else = QRadioButton("其他")

        self.gender_layout.addWidget(self.button_male)
        self.gender_layout.addWidget(self.button_female)
        self.gender_layout.addWidget(self.button_else)

        self.gender_info_box.setLayout(self.gender_layout)

        self.container.addWidget(self.basic_info_box)

        self.container.addWidget(self.gender_info_box)
        self.container.addStretch()

        self.widget = QWidget()
        self.widget.setLayout(self.stacked_layout)
        self.widget.setStyleSheet("background-color:white;")

        self.btn_horizontal_layout = QHBoxLayout()
        self.btn_student = QPushButton("同学备注", self)
        self.btn_family = QPushButton("家人备注", self)
        self.btn_professor = QPushButton("老师备注", self)
        self.btn_colleague = QPushButton("同事备注", self)
        self.btn_friend = QPushButton("朋友备注", self)
        self.btn_other = QPushButton("其他类别备注", self)
        self.btn_horizontal_layout.addStretch(1)
        self.btn_horizontal_layout.addWidget(self.btn_student)
        self.btn_horizontal_layout.addWidget(self.btn_family)
        self.btn_horizontal_layout.addWidget(self.btn_professor)
        self.btn_horizontal_layout.addWidget(self.btn_colleague)
        self.btn_horizontal_layout.addWidget(self.btn_friend)
        self.btn_horizontal_layout.addWidget(self.btn_other)
        self.btn_horizontal_layout.addStretch(1)

        self.btn_student.clicked.connect(self.btn_student_clicked)
        self.btn_family.clicked.connect(self.btn_family_clicked)
        self.btn_professor.clicked.connect(self.btn_professor_clicked)
        self.btn_colleague.clicked.connect(self.btn_colleague_clicked)
        self.btn_friend.clicked.connect(self.btn_friend_clicked)
        self.btn_other.clicked.connect(self.btn_other_clicked)

        self.container.addLayout(self.btn_horizontal_layout)


        self.container.addWidget(self.widget)

        self.save_horizontal_layout = QHBoxLayout()
        self.save_button = QPushButton("保存", self)
        self.save_horizontal_layout.addStretch(1)
        self.save_horizontal_layout.addWidget(self.save_button)
        self.save_horizontal_layout.addStretch(1)
        self.container.addLayout(self.save_horizontal_layout)

        self.save_button.clicked.connect(self.save_Info_clicked)
        self.setLayout(self.container)

        self.resize(400, 400)

        self.setWindowTitle('新建联系人')

    # 联系人类别选择按钮UI实现
    def btn_student_clicked(self):
        self.stacked_layout.setCurrentIndex(0)
        self.attach_label = 'student'
    def btn_family_clicked(self):
        self.stacked_layout.setCurrentIndex(1)
        self.attach_label = 'family'
    def btn_professor_clicked(self):
        self.stacked_layout.setCurrentIndex(2)
        self.attach_label = 'professor'
    def btn_colleague_clicked(self):
        self.stacked_layout.setCurrentIndex(3)
        self.attach_label = 'colleague'
    def btn_friend_clicked(self):
        self.stacked_layout.setCurrentIndex(4)
        self.attach_label = 'friend'
    def btn_other_clicked(self):
        self.stacked_layout.setCurrentIndex(5)
        self.attach_label = 'other'
    

    # 保存新增信息按钮--功能实现
    def save_Info_clicked(self):

        global win

        global all_df

        global schoolmate_df

        global professor_df

        global friend_df

        global colleague_df

        global family_df

        global others_df

        global phone_list

        global count

        self._name = self.name.text()
        self._phone_number = self.phone_number.text()
        self._email = self.email.text()
        self._birthday = self.birthday.text()
        self._gender = self.button_male.text()

        if self.attach_label == 'student':
            self.school_s = self.school1.text()
            self.college_s = self.college1.text()
            self.major = self.major1.text()
            self.grade = self.grade1.text()

            stu = add.add_student(self._name, self._gender, self._birthday, self._phone_number, self._email, self.school_s, self.college_s, self.grade, self.major)

            all_df, schoolmate_df = add.update_df(stu, all_df, schoolmate_df, phone_list)

            file_process.saveData(all_df, schoolmate_df, professor_df, friend_df, colleague_df, family_df, others_df, filepath = 'data.xls' )


        if self.attach_label == 'family':
            self.relation = self.relationship.text()
            self.home_address = self.address.text()
            family = add.add_family (self._name, self._gender, self._birthday, self._phone_number, self._email, self.relation, self.home_address)
            all_df, family_df = add.update_df(family, all_df, family_df, phone_list)
            file_process.saveData(all_df, schoolmate_df, professor_df, friend_df, colleague_df, family_df, others_df, filepath = 'data.xls' )

        if self.attach_label == 'professor':
            self.school_t = self.school2.text()
            self.college_t = self.college2.text()
            self.post = self.post2.text()
            professor = add.add_professor(self._name, self._gender, self._birthday, self._phone_number, self._email, self.school_t, self.college_t, self.post)
            all_df, professor_df = add.update_df(professor, all_df, professor_df, phone_list)
            file_process.saveData(all_df, schoolmate_df, professor_df, friend_df, colleague_df, family_df, others_df, filepath = 'data.xls' )

        if self.attach_label == 'colleague':
            self._company = self.company.text()
            self._department = self.department.text()
            self._job = self.job.text()
            colleague = add.add_colleague(self._name, self._gender, self._birthday, self._phone_number, self._email, self._company, self._department, self._job)
            all_df, colleague_df = add.update_df(colleague, all_df, colleague_df, phone_list)
            file_process.saveData(all_df, schoolmate_df, professor_df, friend_df, colleague_df, family_df, others_df, filepath = 'data.xls' )

        if self.attach_label == 'friend':
            self.place = self.meet_time.text()
            self.time = self.how_we_met.text()
            friend = add.add_friend(self._name, self._gender, self._birthday, self._phone_number, self._email, self.place, self.time)
            all_df, friend_df = add.update_df(friend, all_df, friend_df, phone_list)
            file_process.saveData(all_df, schoolmate_df, professor_df, friend_df, colleague_df, family_df, others_df, filepath = 'data.xls' )

        if self.attach_label == 'other':
            self.note = self.other_remark.text()
            others = add.add_others(self._name, self._gender, self._birthday, self._phone_number, self._email, self.note)
            all_df, others_df = add.update_df(others, all_df, others_df,phone_list)
            file_process.saveData(all_df, schoolmate_df, professor_df, friend_df, colleague_df, family_df, others_df, filepath = 'data.xls' )
        
        
        win.refrsh()
        self.close()

# ---------------------------------------2 新增联系人模块结束-----------------------------------------



# ---------------------------------------3 显示详细信息模块---------------------------------------------

# 显示详细信息子窗口
class showDetailInfo(QWidget):
    def __init__(self,dpNew):
        super().__init__()
        self.setWindowTitle('显示详细信息')
        self.resize(350, 400)
        self.dpNew = dpNew
        self.allWidget()

    # 子窗口--UI实现
    def allWidget(self):
        self.dataP = {
            "name":"姓氏",
            "gender":"性别",
            "phone":"电话",
            "birthday":"生日",
            "email":"邮箱",
            "school":"学校",
            "college":"学院",
            "major":"专业",
            "post":"职称",
            "place":"位置",
            "job":"工作",
            "relation":"关系",
            "home_address":"家庭住宅",
            "note":"备注",
            "time":"时间",
            "company":"公司",
            'department':'部门',
            'grade':'年级',
        }

        self.container = QVBoxLayout()

        self.upper_box = self.special_info()

        self.lower_box = self.detail_ui_student()
        self.saveButton = QPushButton("修改")
        self.saveButton.clicked.connect(self.saveDf)
        self.container.addWidget(self.upper_box)
        self.container.addWidget(self.lower_box)
        self.container.addWidget(self.saveButton)

        self.setLayout(self.container)

        self.resize(400, 400)

        self.setWindowTitle('详细信息')


    # 子窗口--显示基本信息功能实现
    def saveDf(self):
        global win

        # table = mainWindow()

        global all_df

        global schoolmate_df

        global professor_df

        global friend_df

        global colleague_df

        global family_df

        global others_df

        global phone_list

        global count

        ids = int(list(self.dpNew["phone"])[0])
        state = 0
        phone = self.lineUp[1].text()

        if phone == str(ids):
            pass
        else:
            if list(all_df[all_df["phone"] == phone].index) != []:
                QMessageBox.warning(self,"警告","存在重复电话号码,请重新输入",QMessageBox.Yes)
                return
            if list(all_df[all_df["phone"] == int(phone)].index) != []:
                QMessageBox.warning(self,"警告","存在重复电话号码,请重新输入",QMessageBox.Yes)
                return

        # 查找分类
        if list(schoolmate_df[schoolmate_df["phone"] == ids].index) != []:

            name  = self.lineUp[0].text()
            phone = self.lineUp[1].text()
            birthday = self.lineUp[2].text()
            gender = self.lineUp[3].text()

            email = self.lineDown[0].text()
            school = self.lineDown[1].text()
            college = self.lineDown[2].text()
            grade = self.lineDown[3].text()
            major = self.lineDown[4].text()
            row = schoolmate_df[schoolmate_df["phone"] == ids].index.values[0]

            schoolmate_df.iloc[row,0] = name
            schoolmate_df.iloc[row,1] = phone
            schoolmate_df.iloc[row,2] = birthday
            schoolmate_df.iloc[row,3] = gender
            schoolmate_df.iloc[row,4] = email
            schoolmate_df.iloc[row,5] = school
            schoolmate_df.iloc[row,6] = college
            schoolmate_df.iloc[row,7] = grade
            schoolmate_df.iloc[row,8] = major

            row = all_df[all_df["phone"] == ids].index.values[0]

            all_df.iloc[row, 0] = name
            all_df.iloc[row, 1] = phone
            all_df.iloc[row, 2] = birthday
            all_df.iloc[row, 3] = gender
            all_df.iloc[row, 4] = email

            state = 1
        elif list(professor_df[professor_df["phone"] == ids].index) != []:
            name = self.lineUp[0].text()
            phone = self.lineUp[1].text()
            birthday = self.lineUp[2].text()
            gender = self.lineUp[3].text()

            email = self.lineDown[0].text()
            school = self.lineDown[1].text()
            college = self.lineDown[2].text()
            post = self.lineDown[3].text()

            row = professor_df[professor_df["phone"] == ids].index.values[0]

            professor_df.iloc[row, 0] = name
            professor_df.iloc[row, 1] = phone
            professor_df.iloc[row, 2] = birthday
            professor_df.iloc[row, 3] = gender
            professor_df.iloc[row, 4] = email
            professor_df.iloc[row, 5] = school
            professor_df.iloc[row, 6] = college
            professor_df.iloc[row, 7] = post


            row = all_df[all_df["phone"] == ids].index.values[0]

            all_df.iloc[row, 0] = name
            all_df.iloc[row, 1] = phone
            all_df.iloc[row, 2] = birthday
            all_df.iloc[row, 3] = gender
            all_df.iloc[row, 4] = email
            state = 1
        elif list(friend_df[friend_df["phone"] == ids].index) != []:
            name = self.lineUp[0].text()
            phone = self.lineUp[1].text()
            birthday = self.lineUp[2].text()
            gender = self.lineUp[3].text()

            email = self.lineDown[0].text()
            place = self.lineDown[1].text()
            time = self.lineDown[2].text()

            row = friend_df[friend_df["phone"] == ids].index.values[0]

            friend_df.iloc[row, 0] = name
            friend_df.iloc[row, 1] = phone
            friend_df.iloc[row, 2] = birthday
            friend_df.iloc[row, 3] = gender
            friend_df.iloc[row, 4] = email
            friend_df.iloc[row, 5] = place
            friend_df.iloc[row, 6] = time

            row = all_df[all_df["phone"] == ids].index.values[0]

            all_df.iloc[row, 0] = name
            all_df.iloc[row, 1] = phone
            all_df.iloc[row, 2] = birthday
            all_df.iloc[row, 3] = gender
            all_df.iloc[row, 4] = email
            state = 1
        elif list(colleague_df[colleague_df["phone"] == ids].index) != []:
            name = self.lineUp[0].text()
            phone = self.lineUp[1].text()
            birthday = self.lineUp[2].text()
            gender = self.lineUp[3].text()

            email = self.lineDown[0].text()
            company = self.lineDown[1].text()
            department = self.lineDown[2].text()
            job = self.lineDown[3].text()
            row = colleague_df[colleague_df["phone"] == ids].index.values[0]

            colleague_df.iloc[row, 0] = name
            colleague_df.iloc[row, 1] = phone
            colleague_df.iloc[row, 2] = birthday
            colleague_df.iloc[row, 3] = gender
            colleague_df.iloc[row, 4] = email
            colleague_df.iloc[row, 5] = company
            colleague_df.iloc[row, 6] = department
            colleague_df.iloc[row, 7] = job

            row = all_df[all_df["phone"] == ids].index.values[0]

            all_df.iloc[row, 0] = name
            all_df.iloc[row, 1] = phone
            all_df.iloc[row, 2] = birthday
            all_df.iloc[row, 3] = gender
            all_df.iloc[row, 4] = email
            state = 1
        elif list(family_df[family_df["phone"] == ids].index) != []:
            name = self.lineUp[0].text()
            phone = self.lineUp[1].text()
            birthday = self.lineUp[2].text()
            gender = self.lineUp[3].text()

            email = self.lineDown[0].text()
            relation = self.lineDown[1].text()
            home_address = self.lineDown[2].text()

            row = family_df[family_df["phone"] == ids].index.values[0]

            family_df.iloc[row, 0] = name
            family_df.iloc[row, 1] = phone
            family_df.iloc[row, 2] = birthday
            family_df.iloc[row, 3] = gender
            family_df.iloc[row, 4] = email
            family_df.iloc[row, 5] = relation
            family_df.iloc[row, 6] = home_address


            row = all_df[all_df["phone"] == ids].index.values[0]

            all_df.iloc[row, 0] = name
            all_df.iloc[row, 1] = phone
            all_df.iloc[row, 2] = birthday
            all_df.iloc[row, 3] = gender
            all_df.iloc[row, 4] = email
            state = 1
        elif list(others_df[others_df["phone"] == ids].index) != []:
            name = self.lineUp[0].text()
            phone = self.lineUp[1].text()
            birthday = self.lineUp[2].text()
            gender = self.lineUp[3].text()

            email = self.lineDown[0].text()
            note = self.lineDown[1].text()

            row = others_df[others_df["phone"] == ids].index.values[0]

            others_df.iloc[row, 0] = name
            others_df.iloc[row, 1] = phone
            others_df.iloc[row, 2] = birthday
            others_df.iloc[row, 3] = gender
            others_df.iloc[row, 4] = email
            others_df.iloc[row, 5] = note

            row = all_df[all_df["phone"] == ids].index.values[0]

            all_df.iloc[row, 0] = name
            all_df.iloc[row, 1] = phone
            all_df.iloc[row, 2] = birthday
            all_df.iloc[row, 3] = gender
            all_df.iloc[row, 4] = email
            state = 1
        if state == 1:
            pass
        else:
            ids = str(list(self.dpNew["phone"])[0])
            phone = self.lineUp[1].text()

            if phone == str(ids):
                pass
            else:
                if list(all_df[all_df["phone"] == phone].index) != []:
                    QMessageBox.warning(self, "警告", "存在重复电话号码,请重新输入", QMessageBox.Yes)
                    return

                    # 查找分类
            if list(schoolmate_df[schoolmate_df["phone"] == ids].index) != []:

                name = self.lineUp[0].text()
                phone = self.lineUp[1].text()
                birthday = self.lineUp[2].text()
                gender = self.lineUp[3].text()

                email = self.lineDown[0].text()
                school = self.lineDown[1].text()
                college = self.lineDown[2].text()
                grade = self.lineDown[3].text()
                major = self.lineDown[4].text()
                row = schoolmate_df[schoolmate_df["phone"] == ids].index.values[0]

                schoolmate_df.iloc[row, 0] = name
                schoolmate_df.iloc[row, 1] = phone
                schoolmate_df.iloc[row, 2] = birthday
                schoolmate_df.iloc[row, 3] = gender
                schoolmate_df.iloc[row, 4] = email
                schoolmate_df.iloc[row, 5] = school
                schoolmate_df.iloc[row, 6] = college
                schoolmate_df.iloc[row, 7] = grade
                schoolmate_df.iloc[row, 8] = major

                row = all_df[all_df["phone"] == ids].index.values[0]

                all_df.iloc[row, 0] = name
                all_df.iloc[row, 1] = phone
                all_df.iloc[row, 2] = birthday
                all_df.iloc[row, 3] = gender
                all_df.iloc[row, 4] = email

                state = 1
            elif list(professor_df[professor_df["phone"] == ids].index) != []:
                name = self.lineUp[0].text()
                phone = self.lineUp[1].text()
                birthday = self.lineUp[2].text()
                gender = self.lineUp[3].text()

                email = self.lineDown[0].text()
                school = self.lineDown[1].text()
                college = self.lineDown[2].text()
                post = self.lineDown[3].text()

                row = professor_df[professor_df["phone"] == ids].index.values[0]

                professor_df.iloc[row, 0] = name
                professor_df.iloc[row, 1] = phone
                professor_df.iloc[row, 2] = birthday
                professor_df.iloc[row, 3] = gender
                professor_df.iloc[row, 4] = email
                professor_df.iloc[row, 5] = school
                professor_df.iloc[row, 6] = college
                professor_df.iloc[row, 7] = post

                row = all_df[all_df["phone"] == ids].index.values[0]

                all_df.iloc[row, 0] = name
                all_df.iloc[row, 1] = phone
                all_df.iloc[row, 2] = birthday
                all_df.iloc[row, 3] = gender
                all_df.iloc[row, 4] = email
                state = 1
            elif list(friend_df[friend_df["phone"] == ids].index) != []:
                name = self.lineUp[0].text()
                phone = self.lineUp[1].text()
                birthday = self.lineUp[2].text()
                gender = self.lineUp[3].text()

                email = self.lineDown[0].text()
                place = self.lineDown[1].text()
                time = self.lineDown[2].text()

                row = friend_df[friend_df["phone"] == ids].index.values[0]

                friend_df.iloc[row, 0] = name
                friend_df.iloc[row, 1] = phone
                friend_df.iloc[row, 2] = birthday
                friend_df.iloc[row, 3] = gender
                friend_df.iloc[row, 4] = email
                friend_df.iloc[row, 5] = place
                friend_df.iloc[row, 6] = time

                row = all_df[all_df["phone"] == ids].index.values[0]

                all_df.iloc[row, 0] = name
                all_df.iloc[row, 1] = phone
                all_df.iloc[row, 2] = birthday
                all_df.iloc[row, 3] = gender
                all_df.iloc[row, 4] = email
                state = 1
            elif list(colleague_df[colleague_df["phone"] == ids].index) != []:
                name = self.lineUp[0].text()
                phone = self.lineUp[1].text()
                birthday = self.lineUp[2].text()
                gender = self.lineUp[3].text()

                email = self.lineDown[0].text()
                company = self.lineDown[1].text()
                department = self.lineDown[2].text()
                job = self.lineDown[3].text()
                row = colleague_df[colleague_df["phone"] == ids].index.values[0]

                colleague_df.iloc[row, 0] = name
                colleague_df.iloc[row, 1] = phone
                colleague_df.iloc[row, 2] = birthday
                colleague_df.iloc[row, 3] = gender
                colleague_df.iloc[row, 4] = email
                colleague_df.iloc[row, 5] = company
                colleague_df.iloc[row, 6] = department
                colleague_df.iloc[row, 7] = job

                row = all_df[all_df["phone"] == ids].index.values[0]

                all_df.iloc[row, 0] = name
                all_df.iloc[row, 1] = phone
                all_df.iloc[row, 2] = birthday
                all_df.iloc[row, 3] = gender
                all_df.iloc[row, 4] = email
                state = 1
            elif list(family_df[family_df["phone"] == ids].index) != []:
                name = self.lineUp[0].text()
                phone = self.lineUp[1].text()
                birthday = self.lineUp[2].text()
                gender = self.lineUp[3].text()

                email = self.lineDown[0].text()
                relation = self.lineDown[1].text()
                home_address = self.lineDown[2].text()

                row = family_df[family_df["phone"] == ids].index.values[0]

                family_df.iloc[row, 0] = name
                family_df.iloc[row, 1] = phone
                family_df.iloc[row, 2] = birthday
                family_df.iloc[row, 3] = gender
                family_df.iloc[row, 4] = email
                family_df.iloc[row, 5] = relation
                family_df.iloc[row, 6] = home_address

                row = all_df[all_df["phone"] == ids].index.values[0]

                all_df.iloc[row, 0] = name
                all_df.iloc[row, 1] = phone
                all_df.iloc[row, 2] = birthday
                all_df.iloc[row, 3] = gender
                all_df.iloc[row, 4] = email
                state = 1
            elif list(others_df[others_df["phone"] == ids].index) != []:
                name = self.lineUp[0].text()
                phone = self.lineUp[1].text()
                birthday = self.lineUp[2].text()
                gender = self.lineUp[3].text()

                email = self.lineDown[0].text()
                note = self.lineDown[1].text()

                row = others_df[others_df["phone"] == ids].index.values[0]

                others_df.iloc[row, 0] = name
                others_df.iloc[row, 1] = phone
                others_df.iloc[row, 2] = birthday
                others_df.iloc[row, 3] = gender
                others_df.iloc[row, 4] = email
                others_df.iloc[row, 5] = note

                row = all_df[all_df["phone"] == ids].index.values[0]

                all_df.iloc[row, 0] = name
                all_df.iloc[row, 1] = phone
                all_df.iloc[row, 2] = birthday
                all_df.iloc[row, 3] = gender
                all_df.iloc[row, 4] = email
                state = 1

        file_process.saveData(all_df, schoolmate_df, professor_df, friend_df, colleague_df, family_df, others_df,
                              filepath='data.xls')

        win.refrsh()
        QtWidgets.QMessageBox.information(self,"提示","修改成功",QtWidgets.QMessageBox.Yes)
        self.close()


    # 子窗口--显示类别备注信息功能实现
    def special_info(self):
        
        # 创建基本信息模块,4个基本信息姓氏、名字、电话、性别
        # 其中，姓氏，名字，电话使用垂直布局，性别使用水平布局。两部分总体上采用垂直布局

        # basic_info_box是用于获取姓氏，名字，电话的第一个垂直布局的模块
        self.special_info_box = QGroupBox("基本信息")

        self.special_info_layout = QVBoxLayout()

        fundationInfo = ['name',  'phone', 'birthday' ,'gender']
        cols = list(self.dpNew.columns)
        self.lineUp = []
        print(self.dpNew)
        for name in cols:
            if name in fundationInfo:
                self.name = QLineEdit(str(list(self.dpNew[name])[0]))
                self.name.setPlaceholderText(self.dataP[name])
                self.special_info_layout.addWidget(self.name)
                self.lineUp.append(self.name)


        self.special_info_box.setLayout(self.special_info_layout)

        return self.special_info_box

        
    # 子窗口--根据类别的UI针对设计
    def detail_ui_student(self):

        self.basic_info_box = QGroupBox("备注信息")
        #self.container = QVBoxLayout()

        self.basic_info_layout = QVBoxLayout()

        self.school = QLineEdit()
        self.college = QLineEdit()
        self.major = QLineEdit()
        self.grade = QLineEdit()

        fundationInfo = ['name', 'phone', 'birthday', 'gender']
        cols = list(self.dpNew.columns)
        self.lineDown = []
        for name in cols:
            if name not in fundationInfo:
                self.school = QLineEdit(str(list(self.dpNew[name])[0]))
                self.school.setPlaceholderText(self.dataP[name])
                self.basic_info_layout.addWidget(self.school)
                self.lineDown.append(self.school)
        self.basic_info_box.setLayout(self.basic_info_layout)

        return self.basic_info_box
    

    def detail_ui_friend(self):

        self.basic_info_box = QGroupBox("备注信息")
        #self.container = QVBoxLayout()

        self.basic_info_layout = QVBoxLayout()

        self.place = QLineEdit()
        self.time = QLineEdit()

        self.place.setPlaceholderText("地点")
        self.time.setPlaceholderText("时间")

        self.basic_info_layout.addWidget(self.place)
        self.basic_info_layout.addWidget(self.time)

        self.basic_info_box.setLayout(self.basic_info_layout)

        return self.basic_info_box
    

    def detail_ui_colleague(self):

        self.basic_info_box = QGroupBox("备注信息")
        #self.container = QVBoxLayout()

        self.basic_info_layout = QVBoxLayout()

        self.company = QLineEdit()
        self.department = QLineEdit()
        self.job = QLineEdit()

        self.company.setPlaceholderText("公司")
        self.department.setPlaceholderText("部门")
        self.job.setPlaceholderText("工作")

        self.basic_info_layout.addWidget(self.company)
        self.basic_info_layout.addWidget(self.department)
        self.basic_info_layout.addWidget(self.job)

        self.basic_info_box.setLayout(self.basic_info_layout)

        return self.basic_info_box
    

    def detail_ui_family(self):

        self.basic_info_box = QGroupBox("备注信息")
        #self.container = QVBoxLayout()

        self.basic_info_layout = QVBoxLayout()

        self.relation = QLineEdit()
        self.home_address = QLineEdit()

        self.relation.setPlaceholderText("公司")
        self.home_address.setPlaceholderText("部门")

        self.basic_info_layout.addWidget(self.relation)
        self.basic_info_layout.addWidget(self.home_address)

        self.basic_info_box.setLayout(self.basic_info_layout)

        return self.basic_info_box
    

    def detail_ui_others(self):

        self.basic_info_box = QGroupBox("备注信息")
        #self.container = QVBoxLayout()

        self.basic_info_layout = QVBoxLayout()

        self.note = QLineEdit()

        self.note.setPlaceholderText("备注")

        self.basic_info_layout.addWidget(self.note)

        return self.basic_info_box

# ------------------------------------3 显示详细信息模块结束--------------------------------------------

# 运行主程序
if __name__ == '__main__':
    
    # 创建类QApplication的一个对象app
    app = QApplication(sys.argv)
    # 创建了一个界面的对象
    global win

    # 向当天生日联系人群发生日邮件
    all_df = pd.read_excel('data.xls', sheet_name='all')
    receivers = selectPerson(all_df)
    sendMail(receivers)

    lst = ['姓名','电话','更多操作',]
    win = mainWindow(lst)
    palette = QPalette()
    palette.setColor(QPalette.Background, Qt.white)
    win.setPalette(palette)

    app.setWindowIcon(QtGui.QIcon('img/system.png'))
    win.show()
    sys.exit(app.exec_())