import sys
import psycopg2
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import pyqt_tables as tables

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
        self.ui.comboBox_State3.currentTextChanged.connect(self.stateValueChanged)
        self.ui.listWidget_City3.itemSelectionChanged.connect(self.cityValueChanged)
        self.ui.listWidget_Zipcode2.itemSelectionChanged.connect(self.zipCodeValueChanged)
        self.ui.lineEdit_BusinessName2.textChanged.connect(self.businessNameSearchChanged)
        self.ui.pushButton_Search.clicked.connect(self.searchBusinesses)
        self.ui.pushButton_Clear.clicked.connect(self.clearCategorySelection)
        self.ui.pushButton_Refresh.clicked.connect(self.filterNotableBusinesses)

    def executeSQLQuery(self,sql_str):
        try:
            pysql_string = "dbname='yelpdb' user='postgres' host='localhost' password='" + password_string + "'"
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
        """
        Loads the list of states in `Selection: comboBox_State`.
        """
        # Clear combo box items just in case
        self.ui.comboBox_State3.clear()

        # Add items from database into state combo box
        sql_str = "SELECT distinct state FROM business ORDER BY state;"
        try:
            result = self.executeSQLQuery(sql_str)
            for row in result:
                self.ui.comboBox_State3.addItem(row[0])
        except RuntimeError as error:
            print(error)
            print("State query failed!")

        # To clear default selected values in the combo box
        self.ui.comboBox_State3.setCurrentIndex(-1)
        self.ui.comboBox_State3.clearEditText()

    def stateValueChanged(self):
        """
        Refreshes the values displayed on `Selection: listWidget_City and listWidget_Zipcode`.  
        """
        # Clear list
        self.ui.listWidget_City3.clear()
        self.ui.listWidget_Zipcode2.clear()

        # Catch non-existent state
        if(self.ui.comboBox_State3.currentIndex() < 0):
            raise Exception("Invalid item in list is selected!")

        # Add items from database into city list
        state = self.ui.comboBox_State3.currentText()
        sql_str = "SELECT distinct city FROM business WHERE state = '" + state + "' ORDER BY city;"
        try:
            result = self.executeSQLQuery(sql_str)
            for row in result:
                self.ui.listWidget_City3.addItem(row[0])
        except:
            print("City query has failed!")

        # Add items to zipcode list
        sql_str = "SELECT distinct zipcode from business WHERE state = '" + state + "' ORDER BY zipcode;"
        try:
            result = self.executeSQLQuery(sql_str)
            for row in result:
                self.ui.listWidget_Zipcode2.addItem(row[0])
        except:
            print("Zipcode query has failed!")

        # Fill table with items
        try:
            sql_str = "SELECT name, address, city, stars, business_rating, num_review, total_checkin " + \
                "FROM business WHERE state = '" + state + "' ORDER BY name;"

            # Clear table
            for i in reversed(range(self.ui.tableWidget_Business3.rowCount())):
                self.ui.tableWidget_Business3.removeRow(i)

            result = self.executeSQLQuery(sql_str)
            self.ui.tableWidget_Business3.setColumnCount(len(result[0]))
            self.ui.tableWidget_Business3.setRowCount(len(result))

            # Style table
            tables.setBusinessTableStyle(self.ui.tableWidget_Business3)

            # Fill table with the items
            rowCount = 0
            for row in result:
                for colCount in range(0,len(result[0])):
                    self.ui.tableWidget_Business3.setItem(rowCount,colCount,QTableWidgetItem(str(row[colCount])))
                rowCount += 1
        except:
            print("State: Business query has failed!")

    def cityValueChanged(self):
        state = ""
        city = ""
        if (len(self.ui.listWidget_City3.selectedItems()) > 0):
            state = self.ui.comboBox_State3.currentText()
            city = self.ui.listWidget_City3.selectedItems()[0].text()
        else:
            return

        # Add items from database into zipcode list
        self.ui.listWidget_Zipcode2.clear()
        sql_str = "SELECT distinct zipcode FROM business WHERE city = '" + city + "' ORDER BY zipcode;"
        try:
            result = self.executeSQLQuery(sql_str)
            for row in result:
                self.ui.listWidget_Zipcode2.addItem(row[0])
        except:
            print("Zipcode query has failed!")

        # Fill in business table
        sql_str = "SELECT name, address, city, stars, business_rating, num_review, total_checkin" + \
            " FROM business WHERE state = '" + state + "' AND city = '" + city + "' ORDER BY name;"

        try:
            # Clear table
            for i in reversed(range(self.ui.tableWidget_Business3.rowCount())):
                self.ui.tableWidget_Business3.removeRow(i)

            result = self.executeSQLQuery(sql_str)
            self.ui.tableWidget_Business3.setColumnCount(len(result[0]))
            self.ui.tableWidget_Business3.setRowCount(len(result))

            # Style table
            tables.setBusinessTableStyle(self.ui.tableWidget_Business3)

            # Fill table with the items
            rowCount = 0
            for row in result:
                for colCount in range(0,len(result[0])):
                    self.ui.tableWidget_Business3.setItem(rowCount,colCount,QTableWidgetItem(str(row[colCount])))
                rowCount += 1
        except Exception as e:
            print("City filter has failed!")
            print(e)
    
    def zipCodeValueChanged(self):
        state = ""
        city = ""
        zipcode = ""

        if (len(self.ui.listWidget_Zipcode2.selectedItems()) > 0):
            zipcode = self.ui.listWidget_Zipcode2.selectedItems()[0].text()
        else:
            return
        
        if (self.ui.comboBox_State3.currentIndex() >= 0 and len(self.ui.listWidget_City3.selectedItems()) > 0):
            state = self.ui.comboBox_State3.currentText()
            city = self.ui.listWidget_City3.selectedItems()[0].text()
            
        # Fill the zipcode statistics
        try:
            # Set business count
            sql_str = "SELECT count(*) FROM business WHERE zipcode = '" + zipcode + "'"
            result = self.executeSQLQuery(sql_str)
            self.ui.lineEdit_ZipcodeNumBusinesses.setText(str(result[0][0]))

            # Set population
            sql_str = "SELECT population FROM zipcodeData WHERE zipcode = '" + zipcode + "'"
            result = self.executeSQLQuery(sql_str)
            self.ui.lineEdit_ZipcodePopulation.setText(str(result[0][0]))

            # Set average income
            sql_str = "SELECT meanIncome FROM zipcodeData WHERE zipcode = '" + zipcode + "'"
            result = self.executeSQLQuery(sql_str)
            self.ui.lineEdit_ZipcodeAvgIncome.setText(str(result[0][0]))

            # Table top categories in current zipcode
            sql_str = "SELECT COUNT(business.business_id), categories.category_name FROM business, categories" + \
                    " WHERE business.business_id = categories.business_id AND business.zipcode = '" + zipcode + \
                    "'GROUP BY categories.category_name ORDER BY count(business.business_id) DESC"
            result = self.executeSQLQuery(sql_str)
            self.ui.tableWidget_ZipcodeCategories.setColumnCount(len(result[0]))
            self.ui.tableWidget_ZipcodeCategories.setRowCount(len(result))
            tables.setZipcodeCategoriesStyle(self.ui.tableWidget_ZipcodeCategories)
            
            # Fill table with the items
            rowCount = 0
            for row in result:
                for colCount in range(0,len(result[0])):
                    self.ui.tableWidget_ZipcodeCategories.setItem(rowCount,colCount,QTableWidgetItem(str(row[colCount])))
                rowCount += 1
        except Exception as e:
            print("Failed to retrieve zipcode statistics!")
            print(e)

        # Filter the categories list
        try:
            # Clear the list
            self.ui.listWidget_Categories2.clear()

            sql_str = "SELECT distinct categories.category_name FROM business, categories" + \
                        " WHERE business.business_id = categories.business_id AND business.zipcode = '" + \
                        zipcode + "'"
            result = self.executeSQLQuery(sql_str)

            # Populate list
            for row in result:
                self.ui.listWidget_Categories2.addItem(row[0])
        except Exception as e:
            print("Failed to filter categories.")
            print(e)

        # Fill the business table
        if (state and city):
            sql_str = "SELECT name, address, city, stars, business_rating, num_review, total_checkin" + \
                    " FROM business WHERE state = '" + state + "' AND city = '" + city + "' AND zipcode = '" + \
                    zipcode + "' ORDER BY name;"
        else:
            sql_str = "SELECT name, address, city, stars, business_rating, num_review, total_checkin" + \
                    " FROM business WHERE zipcode = '" + zipcode + "' ORDER BY name;"

        try:
            result = self.executeSQLQuery(sql_str)
            self.ui.tableWidget_Business3.setColumnCount(len(result[0]))
            self.ui.tableWidget_Business3.setRowCount(len(result))

            # Style table
            tables.setBusinessTableStyle(self.ui.tableWidget_Business3)

            # Fill table with the items
            rowCount = 0
            for row in result:
                for colCount in range(0,len(result[0])):
                    self.ui.tableWidget_Business3.setItem(rowCount,colCount,QTableWidgetItem(str(row[colCount])))
                rowCount += 1
        except:
            print("Zipcode filter has failed!")
        
    def businessNameSearchChanged(self):
        zipcode = ""
        category = ""
        if (len(self.ui.listWidget_Zipcode2.selectedItems()) > 0):
            zipcode = self.ui.listWidget_Zipcode2.selectedItems()[0].text()
        if (len(self.ui.listWidget_Categories2.selectedItems()) > 0):
            category = self.ui.listWidget_Categories2.selectedItems()[0].text()

        businessName = self.ui.lineEdit_BusinessName2.text()

        if (not category):
            sql_str = "SELECT distinct name, address, city, stars, business_rating, num_review, total_checkin" + \
                    " FROM business WHERE zipcode = '" + zipcode + "' AND name like '" + businessName + "%' ORDER BY name;"
        else:
            sql_str = "SELECT name, address, city, stars, business_rating, num_review, total_checkin" + \
                    " FROM business, categories WHERE zipcode = '" + zipcode + \
                    "' AND category_name = '" + category + \
                    "' AND business.business_id = categories.business_id" + \
                    " AND name like '" + businessName + "%' ORDER BY name;"

        try:
            # Clear table
            for i in reversed(range(self.ui.tableWidget_Business3.rowCount())):
                self.ui.tableWidget_Business3.removeRow(i)

            result = self.executeSQLQuery(sql_str)
            self.ui.tableWidget_Business3.setColumnCount(len(result[0]))
            self.ui.tableWidget_Business3.setRowCount(len(result))

            # Style table
            tables.setBusinessTableStyle(self.ui.tableWidget_Business3)

            # Fill table with the items
            rowCount = 0
            for row in result:
                for colCount in range(0,len(result[0])):
                    self.ui.tableWidget_Business3.setItem(rowCount,colCount,QTableWidgetItem(str(row[colCount])))
                rowCount += 1
        except Exception as e:
            print("Zipcode filter has failed!")
            print(e)

        return
    
    def searchBusinesses(self):
        """
        Searches businesses based on given information.
        """
        zipcode = ""
        category = ""

        if (len(self.ui.listWidget_Zipcode2.selectedItems()) > 0):
            zipcode = self.ui.listWidget_Zipcode2.selectedItems()[0].text()
        if (len(self.ui.listWidget_Categories2.selectedItems()) > 0):
            category = self.ui.listWidget_Categories2.selectedItems()[0].text()

        businessName = self.ui.lineEdit_BusinessName2.text()
        
        if (zipcode and category):
            sql_str = "SELECT name, address, city, stars, business_rating, num_review, total_checkin" + \
                        " FROM business, categories WHERE zipcode = '" + zipcode + \
                        "' AND category_name = '" + category + \
                        "' AND business.business_id = categories.business_id AND name like '" + \
                        businessName + "%' ORDER BY name;"
        elif (not category):
            sql_str = "SELECT name, address, city, stars, business_rating, num_review, total_checkin" + \
                        " FROM business WHERE zipcode = '" + zipcode + \
                        "' AND name like '" + businessName + "%' ORDER BY name;"

        try:
            # Clear table
            for i in reversed(range(self.ui.tableWidget_Business3.rowCount())):
                self.ui.tableWidget_Business3.removeRow(i)

            result = self.executeSQLQuery(sql_str)
            self.ui.tableWidget_Business3.setColumnCount(len(result[0]))
            self.ui.tableWidget_Business3.setRowCount(len(result))

            # Style table
            tables.setBusinessTableStyle(self.ui.tableWidget_Business3)

            # Fill table with the items
            rowCount = 0
            for row in result:
                for colCount in range(0,len(result[0])):
                    self.ui.tableWidget_Business3.setItem(rowCount,colCount,QTableWidgetItem(str(row[colCount])))
                rowCount += 1
        except Exception as e:
            print("Business search has failed!")
            print(e)

    def clearCategorySelection(self):
        """
        Clears category selection.
        """

        self.ui.listWidget_Categories2.clearSelection()
        

    def filterNotableBusinesses(self):
        """
        Filters the notable businesses table further by searching for select categories.
        """
        if (len(self.ui.listWidget_Zipcode2.selectedItems()) > 0 and \
                len(self.ui.listWidget_Categories2.selectedItems()) > 0):
            zipcode = self.ui.listWidget_Zipcode2.selectedItems()[0].text()
            category = self.ui.listWidget_Categories2.selectedItems()[0].text()

        # Fill in the popular businesses
        try:
            sql_str = "SELECT Name, Business.Total_checkin, Num_review, Business_rating, " + \
                    "(Business_rating + (Total_checkin * 0.3) + (Num_review * 0.2)) AS Popularity_Score " + \
                    "FROM Business,categories WHERE Total_checkin IS NOT NULL AND zipcode = '" + \
                    zipcode + "' And category_name = '" + category + "' AND stars >= 4.5 " + \
                    "AND business_rating >= 4.6 AND Business.business_id = Categories.business_id " + \
                    "ORDER BY popularity_score DESC, Num_review DESC;"

            # Clear table
            for i in reversed(range(self.ui.tableWidget_PopularBusinesses.rowCount())):
                self.ui.tableWidget_PopularBusinesses.removeRow(i)

            result = self.executeSQLQuery(sql_str)
            self.ui.tableWidget_PopularBusinesses.setColumnCount(len(result[0]))
            self.ui.tableWidget_PopularBusinesses.setRowCount(len(result))

            # Style table
            tables.setBusinessTableStyle(self.ui.tableWidget_PopularBusinesses)

            # Fill table with the items
            rowCount = 0
            for row in result:
                for colCount in range(0,len(result[0])):
                    self.ui.tableWidget_PopularBusinesses.setItem(rowCount,colCount,QTableWidgetItem(str(row[colCount])))
                rowCount += 1
        except Exception as e:
            print("Popular business refresh has failed!")
            print(e)
        
        # Fill in the successful businesses
        try:
            sql_str = "SELECT distinct Name, Business.Total_checkin, Num_review, Business_rating, " + \
                    "(Business_rating + (Total_checkin * 0.3) + (Num_review * 0.2)) AS Popularity_Score " + \
                    "FROM Business,categories WHERE Total_checkin IS NOT NULL AND zipcode = '" + \
                    zipcode + "' AND stars >= 4.5 " + \
                    "AND business_rating >= 4.6 AND Business.business_id = Categories.business_id " + \
                    "ORDER BY popularity_score DESC, Num_review DESC;"

            # Clear table
            for i in reversed(range(self.ui.tableWidget_SuccessfulBusinesses.rowCount())):
                self.ui.tableWidget_SuccessfulBusinesses.removeRow(i)

            result = self.executeSQLQuery(sql_str)
            self.ui.tableWidget_SuccessfulBusinesses.setColumnCount(len(result[0]))
            self.ui.tableWidget_SuccessfulBusinesses.setRowCount(len(result))

            # Style table
            tables.setBusinessTableStyle(self.ui.tableWidget_SuccessfulBusinesses)

            # Fill table with the items
            rowCount = 0
            for row in result:
                for colCount in range(0,len(result[0])):
                    self.ui.tableWidget_SuccessfulBusinesses.setItem(rowCount,colCount,QTableWidgetItem(str(row[colCount])))
                rowCount += 1
        except Exception as e:
            print("Popular business refresh has failed!")
            print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = myApp()
    window.show()
    sys.exit(app.exec_())