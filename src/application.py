import sys
import psycopg2
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap

qtCreatorFile = "ui/yelp-pyqt-app.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

try:
    infile = open("bin/password.txt", "r")
    password_string = infile.read()
    infile.close()
except:
    print("Create a file named 'password.txt' in the bin folder and type your pSQL password into it!")


class myApp(QMainWindow):
    def __init__(self):
        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()

        # Event handler
        self.ui.comboBox_State.currentTextChanged.connect(self.stateValueChanged)
        self.ui.listWidget_City.itemSelectionChanged.connect(self.cityValueChanged)

    def executeSQLQuery(self,sql_str):
        try:
            pysql_string = "dbname='milestone1db' user='postgres' host='localhost' password='" + password_string + "'"
            conn = psycopg2.connect(pysql_string)
        except RuntimeError as error:
            print(error)
            print("Unable to connect to database!")
        cur = conn.cursor()
        cur.execute(query=sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()

        return result

    def loadStateList(self):
        # Clear combo box items just in case
        self.ui.comboBox_State.clear()

        # Add items from database into state combo box
        sql_str = "SELECT distinct state FROM business ORDER BY state;"
        try:
            result = self.executeSQLQuery(sql_str)
            for row in result:
                self.ui.comboBox_State.addItem(row[0])
        except RuntimeError as error:
            print(error)
            print("State query failed!")

        # To clear default selected values in the combo box
        self.ui.comboBox_State.setCurrentIndex(-1)
        self.ui.comboBox_State.clearEditText()

    def stateValueChanged(self):
        # Clear list
        self.ui.listWidget_City.clear()

        # Catch non-existent state
        if(self.ui.comboBox_State.currentIndex() < 0):
            raise Exception("Invalid item in list is selected!")

        # Add items from database into city list
        state = self.ui.comboBox_State.currentText()
        sql_str = "SELECT distinct city FROM business WHERE state = '" + state + "' ORDER BY city;"
        try:
            result = self.executeSQLQuery(sql_str)
            for row in result:
                self.ui.listWidget_City.addItem(row[0])
        except:
            print("City query has failed!")

        # Fill table with items
        sql_str = "SELECT name, city, state FROM business WHERE state = '" + state + "' ORDER BY name;"
        try:
            result = self.executeSQLQuery(sql_str)
            self.ui.tableWidget_Business.setColumnCount(len(result[0]))
            self.ui.tableWidget_Business.setRowCount(len(result))

            # Clear table
            for i in reversed(range(self.ui.tableWidget_Business.rowCount())):
                self.ui.tableWidget_Business.removeRow(i)

            # Style table
            headerStyle = "::section { background-color: rgb(200,200,200); }"
            self.ui.tableWidget_Business.horizontalHeader().setStyleSheet(headerStyle)
            self.ui.tableWidget_Business.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
            self.ui.tableWidget_Business.resizeColumnsToContents()
            self.ui.tableWidget_Business.setColumnWidth(0,300)
            self.ui.tableWidget_Business.setColumnWidth(1,100)
            self.ui.tableWidget_Business.setColumnWidth(2,50)

            # Fill table with the items
            rowCount = 0
            for row in result:
                for colCount in range(0,len(result[0])):
                    self.ui.tableWidget_Business.setItem(rowCount,colCount,QTableWidgetItem(row[colCount]))
                rowCount += 1
        except:
            print("Business query has failed!")

    def cityValueChanged(self):
        if (self.ui.comboBox_State.currentIndex() >= 0 and len(self.ui.listWidget_City.selectedItems()) > 0):
            state = self.ui.comboBox_State.currentText()
            city = self.ui.listWidget_City.selectedItems()[0].text()

            sql_str = "SELECT name, city, state FROM business WHERE state = '" + state + "' AND city = '" + city + "' ORDER BY name;"
            try:
                result = self.executeSQLQuery(sql_str)
                self.ui.tableWidget_Business.setColumnCount(len(result[0]))
                self.ui.tableWidget_Business.setRowCount(len(result))

                # Style table
                headerStyle = "::section { background-color: rgb(200,200,200); }"
                self.ui.tableWidget_Business.horizontalHeader().setStyleSheet(headerStyle)
                self.ui.tableWidget_Business.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
                self.ui.tableWidget_Business.resizeColumnsToContents()
                self.ui.tableWidget_Business.setColumnWidth(0,300)
                self.ui.tableWidget_Business.setColumnWidth(1,100)
                self.ui.tableWidget_Business.setColumnWidth(2,50)

                # Fill table with the items
                rowCount = 0
                for row in result:
                    for colCount in range(0,len(result[0])):
                        self.ui.tableWidget_Business.setItem(rowCount,colCount,QTableWidgetItem(row[colCount]))
                    rowCount += 1
            except:
                print("City filter has failed!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = myApp()
    window.show()
    sys.exit(app.exec_())