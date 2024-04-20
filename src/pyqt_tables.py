from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout

def setBusinessTableStyle(tableWidget):
    """
    Given a PyQT application's tableWidget, set the styles of the table.
    """

    headerStyle = "::section { background-color: rgb(200,200,200); }"
    tableWidget.horizontalHeader().setStyleSheet(headerStyle)
    tableWidget.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'User Rating', 'User Reviews', 'Total Checkins'])
    tableWidget.resizeColumnsToContents()
    tableWidget.setColumnWidth(0,200)
    tableWidget.setColumnWidth(1,100)
    tableWidget.setColumnWidth(2,50)
    tableWidget.setColumnWidth(3,80)

def setZipcodeCategoriesStyle(tableWidget):
    """
    Sets the Top Categories table's style.
    """

    headerStyle = "::section { background-color: rgb(200,200,200); }"
    tableWidget.horizontalHeader().setStyleSheet(headerStyle)
    tableWidget.setHorizontalHeaderLabels(['Businesses', 'Category'])
    tableWidget.resizeColumnsToContents()