# -*- coding: utf-8 -*-
# Author: 万锦
# Email : wanjinhhu@gmail.com
# Time : 2023/9/13 16:05
# File: budyko弹性系数计算.py
# Software: PyCharm

from PyQt5.QtGui import *
from qfluentwidgets import MessageBox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import sys
import os
import time
import pandas as pd
from ui.budyko import Ui_MainWindow
from qfluentwidgets import Dialog
from scipy.optimize import fsolve




class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setObjectName("reason_analysis")
        self.ininitialize()
        self.handlebutton()
        #初始化站名、权重
        self.station = 0
        self.w = 0
        #初始化径流信息
        self.runoff = 0
        #初始化降雨信息
        self.pre = 0
        #初始化气温信息
        self.wendu = 0
        self.et = 0
        #初始化计算年限
        self.year_index = 0
        #初始化计算表信息
        self.use_table = 0
        #初始化全序列平均降水、径流、潜在蒸发
        self.p = 0
        self.r = 0
        self.et0 = 0
        #初始化全序列下垫面参数
        self.n = 0



        self.initialize_combox()

    #初始化下拉框
    def initialize_combox(self):
        # 从列表中添加下拉选项
        self.ComboBox.addItems([str(_) for _ in range(1,11)])
        # 设置显示项目
        self.ComboBox.setCurrentIndex(4)




    def ininitialize(self):
        self.LineEdit.setPlaceholderText("1705383")
        # self.PushButton_3.setEnabled(False)
        # self.PushButton.setEnabled(False)
        # self.PushButton_2.setEnabled(False)
        # self.PushButton_5.setEnabled(False)
        # self.PushButton_10.setEnabled(False)

    def handlebutton(self):
        self.PushButton_6.clicked.connect(self.call_author)
        self.PushButton_7.clicked.connect(self.load_w)
        self.PushButton_3.clicked.connect(self.load_runoff)
        self.PushButton.clicked.connect(self.load_pre)
        self.PushButton_2.clicked.connect(self.load_t)
        self.PushButton_5.clicked.connect(self.caculate_et)
        self.PushButton_10.clicked.connect(self.calculate_dataframe)
        self.PushButton_9.clicked.connect(self.caculate_avg)
        self.PushButton_4.clicked.connect(self.caculate_budyko)
        self.PushButton_8.clicked.connect(self.caculate_gongxinalv)

    #显示对话框信息
    def showDialog(self,name=""):
        title = '数据导入'
        content = f"""{name}数据已经成功导入，点击OK进行下一步"""
        w = Dialog(title, content, self)
        w.setTitleBarVisible(False)
        if w.exec():
            pass
        else:
            pass

    #警示对话框信息
    def warning_w(self,name=""):
        title = '计算错误'
        content = f"""{name}信息未载入"""
        w = Dialog(title, content, self)
        w.setTitleBarVisible(False)
        if w.exec():
            pass
        else:
            pass

    # 联系作者
    def call_author(self):
        title = '联系作者'
        content = """wanjinhhu@gmail.com"""
        # w = MessageDialog(title, content, self)   # Win10 style message box
        w = MessageBox(title, content, self)
        if w.exec():
            pass
        else:
            pass

    #载入权重信息
    def load_w(self):
        fname, _ = QFileDialog.getOpenFileName(self, "打开文件", '.', '数据文件(*.xlsx)')
        if fname:
            df = pd.read_excel(fname, index_col=0)
            self.station = df["站点名"].values
            self.w = df["权重"].values
            self.showDialog(name="权重")
            self.PushButton_3.setEnabled(True)

    #载入径流信息
    def load_runoff(self):
        fname, _ = QFileDialog.getOpenFileName(self, "打开文件", '.', '数据文件(*.xlsx)')
        if fname:
            df = pd.read_excel(fname, index_col=0)
            self.runoff = df.stack().values
            self.showDialog(name="径流")
            self.PushButton.setEnabled(True)

    #载入降雨信息
    def load_pre(self):
        fname, _ = QFileDialog.getOpenFileName(self, "打开文件", '.', '数据文件(*.xlsx)')
        if fname:
            # self.statusBar().showMessage("数据加载中......")
            df = pd.read_excel(fname, index_col=0)
            # self.year_index = df.index.values
            data = df.values
            # 表格加载数据
            # 设置行列，设置表头
            tmp = [str(_) for _ in df.columns.tolist()]
            tmp2 = [str(_) for _ in df.index.tolist()]
            self.TableWidget.setRowCount(len(data))
            self.TableWidget.setColumnCount(len(data[0]))
            self.TableWidget.setHorizontalHeaderLabels(tmp)
            self.TableWidget.setVerticalHeaderLabels(tmp2)
            # 设置单元格对齐方式为中心
            cell_alignment = Qt.AlignCenter
            # 表格加载内容
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    use_item = QTableWidgetItem(str(round(item,2)))
                    use_item.setTextAlignment(cell_alignment)
                    self.TableWidget.setItem(row, column, use_item)
            if self.w is 0:
                self.warning_w(name="权重")
            else:
                df_pre_w = df * self.w
                df_pre_w["total"] = df_pre_w.sum(axis=1)
                self.pre = df_pre_w["total"].values
                self.PushButton_2.setEnabled(True)
                self.showDialog(name="月平均雨量")
                # print(self.pre)

    #载入气温数据
    def load_t(self):
        fname, _ = QFileDialog.getOpenFileName(self, "打开文件", '.', '数据文件(*.xlsx)')
        if fname:
            # self.statusBar().showMessage("数据加载中......")
            df = pd.read_excel(fname, index_col=0)
            self.year_index = df.index.values
            self.wendu = df
            data = df.values
            # 表格加载数据
            # 设置行列，设置表头
            tmp = [str(_) for _ in df.columns.tolist()]
            tmp2 = [str(_) for _ in df.index.tolist()]
            self.TableWidget.setRowCount(len(data))
            self.TableWidget.setColumnCount(len(data[0]))
            self.TableWidget.setHorizontalHeaderLabels(tmp)
            self.TableWidget.setVerticalHeaderLabels(tmp2)
            # 设置单元格对齐方式为中心
            cell_alignment = Qt.AlignCenter
            # 表格加载内容
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    use_item = QTableWidgetItem(str(round(item,2)))
                    use_item.setTextAlignment(cell_alignment)
                    self.TableWidget.setItem(row, column, use_item)
            self.PushButton_2.setEnabled(True)
            self.showDialog(name="月平均气温")

    #计算潜在蒸散发
    def caculate_et(self):
        def et0(lst_yue):
            pet_values = []
            tmp = 0
            for t in lst_yue:
                tmp = tmp + (t / 5) ** 1.514
            I = tmp
            a = 6.75 * 10 ** -7 * I ** 3 - 7.71 * 10 ** -5 * I ** 2 + 1.792 * 10 ** -2 * I + 0.49239
            for t in lst_yue:
                pet = 16 * ((10 * t / I) ** a)  # Thornthwaite公式
                pet_values.append(pet)
            return pet_values
        if self.wendu is not 0:
            for _ in range(len(self.wendu.columns)):
                tmp_lst = []
                for i in range(660 // 12):
                    tmp_lst.append(et0(self.wendu.iloc[:, _].values[12 * i:i * 12 + 12]))
                self.wendu[str(_)] = list(np.concatenate(tmp_lst))
            if self.station is not 0:
                df = self.wendu.iloc[:, -(len(self.wendu.columns)//2):]
                df.columns = self.station
                data = df.values
                # 表格加载数据
                # 设置行列，设置表头
                tmp = [str(_) for _ in df.columns.tolist()]
                tmp2 = [str(_) for _ in df.index.tolist()]
                self.TableWidget.setRowCount(len(data))
                self.TableWidget.setColumnCount(len(data[0]))
                self.TableWidget.setHorizontalHeaderLabels(tmp)
                self.TableWidget.setVerticalHeaderLabels(tmp2)
                # 设置单元格对齐方式为中心
                cell_alignment = Qt.AlignCenter
                # 表格加载内容
                for row, form in enumerate(data):
                    for column, item in enumerate(form):
                        use_item = QTableWidgetItem(str(round(item, 2)))
                        use_item.setTextAlignment(cell_alignment)
                        self.TableWidget.setItem(row, column, use_item)
                self.PushButton_2.setEnabled(True)
                self.showDialog(name="潜在蒸散发")
                df = df * self.w
                df["total"] = df.sum(axis=1)
                self.et = df["total"].values
                # print(self.et)
            else:
                self.warning_w(name="权重")
        else:
            self.warning_w(name="气温")

    #构建计算表
    def calculate_dataframe(self):
        if self.runoff is not 0:
            if self.pre is not 0:
                if self.et is not 0:
                    # print(len(self.et))
                    # print(len(self.pre))
                    # print(len(self.runoff))
                    # 构建计算表
                    df = pd.DataFrame([self.runoff, self.et,self.pre])
                    df = df.T
                    df.columns = ["流量", "潜在蒸发", "降水"]
                    df.index = self.year_index
                    self.use_table = df
                    data = df.values
                    # 表格加载数据
                    # 设置行列，设置表头
                    tmp = ["流量", "潜在蒸发", "降水"]
                    tmp2 = self.year_index
                    self.TableWidget_2.setRowCount(len(data))
                    self.TableWidget_2.setColumnCount(len(data[0]))
                    self.TableWidget_2.setHorizontalHeaderLabels(tmp)
                    self.TableWidget_2.setVerticalHeaderLabels(tmp2)
                    # 设置单元格对齐方式为中心
                    cell_alignment = Qt.AlignCenter
                    # 表格加载内容
                    for row, form in enumerate(data):
                        for column, item in enumerate(form):
                            use_item = QTableWidgetItem(str(round(item, 2)))
                            use_item.setTextAlignment(cell_alignment)
                            self.TableWidget_2.setItem(row, column, use_item)
                else:
                    self.warning_w(name="潜在蒸发")
            else:
                self.warning_w(name="降雨")
        else:
            self.warning_w(name="径流")

    #计算年均气象要素
    def caculate_avg(self):

        if self.use_table is not 0:
            tmp = self.LineEdit.text()
            if tmp:
                # 长江流域面积
                eara = float(tmp) * 1000 * 1000
                df = self.use_table
                df["径流深"] = df["流量"] * 30 * 24 * 3600 / eara * 1000
                # 变化期年份
                change_year = int(self.ComboBox.currentText())
                # 构建基准期和变化期，后八年为变化前，前面为基准期
                df_std = df.iloc[:-12 * change_year, :]
                df_change = df.iloc[-12 * change_year:, :]

                # 获取基准期降水、径流、潜在蒸发
                p1 = df_std.sum().降水 / (df.shape[0] / 12 - change_year)
                r1 = df_std.sum().径流深 / (df.shape[0] / 12 - change_year)
                et01 = df_std.sum().潜在蒸发 / (df.shape[0] / 12 - change_year)

                # 获取变化期降水、径流、潜在蒸发
                p2 = df_change.sum().降水 / change_year
                r2 = df_change.sum().径流深 / change_year
                et02 = df_change.sum().潜在蒸发 / change_year

                # 获取全过程降水、径流、潜在蒸发
                self.p = df.sum().降水 / (df.shape[0] / 12)
                self.r = df.sum().径流深 / (df.shape[0] / 12)
                self.et0 = df.sum().潜在蒸发 / (df.shape[0] / 12)

                #设置基准期年均气象要素显示
                self.LineEdit_28.setText(str(p1))
                self.LineEdit_27.setText(str(et01))
                self.LineEdit_17.setText(str(r1))

                #设置变化期气象要素显示
                self.LineEdit_42.setText(str(p2))
                self.LineEdit_41.setText(str(et02))
                self.LineEdit_43.setText(str(r2))
            else:
                self.warning_w(name="研究区域面积")
        else:
            self.warning_w(name="区域气象要素")

    #计算弹性系数
    def caculate_budyko(self):

        # 定义方程
        def equation(n):
            return P - R - P * ET0 / (P ** n + ET0 ** n) ** (1 / n)

        # 计算基准期弹性系数
        if self.LineEdit_28.text():
            # 给定常数
            P = float(self.LineEdit_28.text())
            R = float(self.LineEdit_27.text())
            ET0 = float(self.LineEdit_17.text())
            if P:
                if R:
                    if ET0:
                        # 使用fsolve数值求解
                        n_solution = fsolve(equation, 1.0)  # 从初始值1.0开始求解

                        # 计算dP
                        dP = ((1 + (ET0 / P) ** n_solution[0]) ** ((1 / n_solution[0]) + 1) - (ET0 / P) ** (n_solution[0] + 1)) / \
                             ((1 + (ET0 / P) ** n_solution[0]) * ((1 + (ET0 / P) ** n_solution[0]) ** (1 / n_solution[0]) - ET0 / P))

                        # 计算dET0
                        dET0 = 1 / ((1 + (ET0 / P) ** n_solution[0]) * (1 - (1 + (ET0 / P) ** (-n_solution[0])) ** (1 / n_solution[0])))

                        # 计算dn
                        dn = (np.log(1 + (ET0 / P) ** n_solution[0]) + (ET0 / P) ** n_solution[0] * np.log(
                            1 + (ET0 / P) ** (-n_solution[0]))) / \
                             (n_solution[0] * (1 + (ET0 / P) ** n_solution[0]) * (
                                         1 - ((1 + (ET0 / P) ** (-n_solution[0])) ** (1 / n_solution[0]))))
                        #基准期弹性系数
                        self.LineEdit_47.setText(str(round(dP,4)))
                        self.LineEdit_49.setText(str(round(dET0,4)))
                        self.LineEdit_48.setText(str(round(dn,4)))
                        self.LineEdit_58.setText(str(round(n_solution[0],4)))
                    else:
                        self.warning_w(name='基准期蒸散发')
                else:
                    self.warning_w(name="基准期径流")
            else:
                self.warning_w(name="基准期降雨")

            #变化期弹性系数
            P = float(self.LineEdit_42.text())
            R = float(self.LineEdit_41.text())
            ET0 = float(self.LineEdit_43.text())
            if P:
                if R:
                    if ET0:
                        # 使用fsolve数值求解
                        n_solution = fsolve(equation, 1.0)  # 从初始值1.0开始求解

                        # 计算dP
                        dP = ((1 + (ET0 / P) ** n_solution[0]) ** ((1 / n_solution[0]) + 1) - (ET0 / P) ** (
                                    n_solution[0] + 1)) / \
                             ((1 + (ET0 / P) ** n_solution[0]) * (
                                         (1 + (ET0 / P) ** n_solution[0]) ** (1 / n_solution[0]) - ET0 / P))

                        # 计算dET0
                        dET0 = 1 / ((1 + (ET0 / P) ** n_solution[0]) * (
                                    1 - (1 + (ET0 / P) ** (-n_solution[0])) ** (1 / n_solution[0])))

                        # 计算dn
                        dn = (np.log(1 + (ET0 / P) ** n_solution[0]) + (ET0 / P) ** n_solution[0] * np.log(
                            1 + (ET0 / P) ** (-n_solution[0]))) / \
                             (n_solution[0] * (1 + (ET0 / P) ** n_solution[0]) * (
                                     1 - ((1 + (ET0 / P) ** (-n_solution[0])) ** (1 / n_solution[0]))))
                        #变化期弹性系数
                        self.LineEdit_26.setText(str(round(dP, 4)))
                        self.LineEdit_25.setText(str(round(dET0, 4)))
                        self.LineEdit_16.setText(str(round(dn, 4)))
                        self.LineEdit_56.setText(str(round(n_solution[0], 4)))
                    else:
                        self.warning_w(name='基准期蒸散发')
                else:
                    self.warning_w(name="基准期径流")
            else:
                self.warning_w(name="基准期降雨")

            # 全序列弹性系数
            P = self.p
            R = self.r
            ET0 = self.et0
            if P:
                if R:
                    if ET0:
                        # 使用fsolve数值求解
                        n_solution = fsolve(equation, 1.0)  # 从初始值1.0开始求解

                        # 计算dP
                        dP = ((1 + (ET0 / P) ** n_solution[0]) ** ((1 / n_solution[0]) + 1) - (ET0 / P) ** (
                                n_solution[0] + 1)) / \
                             ((1 + (ET0 / P) ** n_solution[0]) * (
                                     (1 + (ET0 / P) ** n_solution[0]) ** (1 / n_solution[0]) - ET0 / P))

                        # 计算dET0
                        dET0 = 1 / ((1 + (ET0 / P) ** n_solution[0]) * (
                                1 - (1 + (ET0 / P) ** (-n_solution[0])) ** (1 / n_solution[0])))

                        # 计算dn
                        dn = (np.log(1 + (ET0 / P) ** n_solution[0]) + (ET0 / P) ** n_solution[0] * np.log(
                            1 + (ET0 / P) ** (-n_solution[0]))) / \
                             (n_solution[0] * (1 + (ET0 / P) ** n_solution[0]) * (
                                     1 - ((1 + (ET0 / P) ** (-n_solution[0])) ** (1 / n_solution[0]))))
                        # 全序列下垫面参数
                        self.n = n_solution[0]

                    else:
                        self.warning_w(name='基准期蒸散发')
                else:
                    self.warning_w(name="基准期径流")
            else:
                self.warning_w(name="基准期降雨")
        else:
            self.warning_w(name="平均气象要素")

    #计算贡献率
    def caculate_gongxinalv(self):

        if self.LineEdit_28.text():
            if self.LineEdit_47.text():
                #获取基准期平均降水、径流、潜在蒸发及弹性系数
                p1 = float(self.LineEdit_28.text())
                r1 = float(self.LineEdit_27.text())
                et01 = float(self.LineEdit_17.text())
                dp1 = float(self.LineEdit_47.text())
                det01 = float(self.LineEdit_49.text())
                dn1 = float(self.LineEdit_48.text())
                n1 = float(self.LineEdit_58.text())

                # 获取变化期平均降水、径流、潜在蒸发及弹性系数
                p2 = float(self.LineEdit_42.text())
                r2 = float(self.LineEdit_41.text())
                et02 = float(self.LineEdit_43.text())
                dp2 = float(self.LineEdit_26.text())
                det02 = float(self.LineEdit_25.text())
                dn2 = float(self.LineEdit_16.text())
                n2 = float(self.LineEdit_56.text())
                if p1:
                    if dp1:
                        #贡献率计算
                        r_change = r2 - r1
                        p_lv = (dp1 * (p2-p1) / self.p * self.r)/r_change * 100
                        et_lv = det01 * (et02-et01)/r_change * 100
                        n_lv = (dn1 * (n2-n1) / self.n * self.r)/r_change*100

                        self.LineEdit_6.setText(str(round(p_lv,4)))
                        self.LineEdit_8.setText(str(round(et_lv,4)))
                        self.LineEdit_7.setText(str(round(n_lv,4)))
                    else:
                        self.warning_w(name="弹性系数")
                else:
                    self.warning_w(name="平均气象要素")
            else:
                self.warning_w(name="弹性系数")
        else:
            self.warning_w(name="平均气象要素")




def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.setWindowTitle("径流变化归因分析系统")
    mainwindow.setWindowIcon(QIcon("three.ico"))
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()