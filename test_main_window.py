# import sys
# from PyQt5 import QtWidgets

# class Example(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         # create widgets
#         graph = QtWidgets.QFrame()
#         graph.setFixedHeight(40)
#         graph.setFrameShape(QtWidgets.QFrame.Box)
#         graph.setStyleSheet("QWidget { background-color: red }" )

#         qlist = QtWidgets.QListWidget()
#         qlist.setFrameStyle(QtWidgets.QFrame.Raised)
#         qlist.addItems(map(str, range(31)))

#         # create QHBoxLayout and add QListWidget
#         hlay = QtWidgets.QHBoxLayout()
#         hlay.addWidget(qlist)
#         hlay.addStretch(1)

#         # create QVBoxLayout and add QFrame and QHBoxLayout
#         vlay = QtWidgets.QVBoxLayout(self)
#         vlay.addWidget(graph)
#         vlay.addLayout(hlay) 

#         self.setStyleSheet("font: 20pt Cambria")
#         self.showMaximized()

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 

        # Show widget
        self.show()

    def createTable(self):
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setRowCount(6)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setItem(0,0, QTableWidgetItem("Cell (1,1)"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Cell (1,2)"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Cell (2,1)"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("Cell (2,2)"))
        self.tableWidget.setItem(2,0, QTableWidgetItem("Cell (3,1)"))
        self.tableWidget.setItem(2,1, QTableWidgetItem("Cell (3,2)"))
        self.tableWidget.setItem(3,0, QTableWidgetItem("Cell (4,1)"))
        self.tableWidget.setItem(3,1, QTableWidgetItem("Cell (4,2)"))
        self.tableWidget.move(0,0)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())  
