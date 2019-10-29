import sys
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow,QPushButton,QMessageBox,QAction, QLineEdit, QMessageBox,QGroupBox,QVBoxLayout,QMenuBar,QTabWidget,QLabel,QHBoxLayout,QFrame,QSplitter,QStyleFactory
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot,Qt
import time

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Easy Scanner'
        self.setFixedSize(1200  , 650)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.statusBar().showMessage("Application waiting.")

        self.window = Window()
        self.setCentralWidget(self.window)
        self.show()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.hbox = QHBoxLayout()

        topleft =QFrame(self)
        topleft.setFrameShape(QFrame.StyledPanel)


        bottomleft = QFrame(self)
        bottomleft.setFrameShape(QFrame.StyledPanel)


        right = QFrame(self)
        right.setFrameShape(QFrame.StyledPanel)



        splitter1 = QSplitter(Qt.Vertical,frameShape=QFrame.StyledPanel)
        splitter1.addWidget(topleft)
        splitter1.addWidget(bottomleft)
        splitter1.setSizes([100,400])


        splitter2 = QSplitter(Qt.Horizontal,frameShape=QFrame.StyledPanel)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(right)
        splitter2.setSizes([550,650])

        righttabs = QTabWidget(right)

        righttabs.setMovable(True)
        righttabs.setDocumentMode(True)
        righttabs.setUsesScrollButtons(True)
        righttabs.setElideMode(Qt.ElideRight)
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()
        tab5 = QWidget()
        righttabs.resize(600,610)
        righttabs.addTab(tab1,"Tab 1")
        righttabs.addTab(tab2,"Tab 2")
        righttabs.addTab(tab3,"Tab 3")
        righttabs.addTab(tab4,"Tab 4")
        righttabs.addTab(tab5,"Tab 5")

        #self.righttabs.layout = QHBoxLayout(self)

        leftabs = QTabWidget(bottomleft)
        tab_1 = QWidget()
        tab_2 = QWidget()
        tab_3 = QWidget()
        tab_4 = QWidget()
        tab_5 = QWidget()
        leftabs.resize(600,500)
        leftabs.addTab(tab_1,"Tab 1")
        leftabs.addTab(tab_2,"Tab 2")
        leftabs.addTab(tab_3,"Tab 3")
        leftabs.addTab(tab_4,"Tab 4")
        leftabs.addTab(tab_5,"Tab 5")


        self.address_text = QLineEdit(topleft)
        self.address_text.setPlaceholderText("https://example.com") 
        self.address_text.move(20, 35)
        self.address_text.resize(300,40)

        self.start_button = QPushButton('Start Scan', topleft)
        self.start_button.clicked.connect(self.start_on_click)
        self.start_button.move(340,40)

        self.stop_button = QPushButton('Stop Scan', topleft)
        self.stop_button.clicked.connect(self.start_on_click)
        self.stop_button.move(435,40)


        hbox.addWidget(splitter1)
        hbox.addWidget(splitter2)


        self.setLayout(hbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.show()

    @pyqtSlot()
    def start_on_click(self):
        self.address_text.setDisabled(True)
        self.start_button.setDisabled(True)

    def set_frames(self):
        self.topleft =QFrame(self)
        self.topleft.setFrameShape(QFrame.StyledPanel)

        self.bottomleft = QFrame(self)
        self.bottomleft.setFrameShape(QFrame.StyledPanel)

        self.right = QFrame(self)
        self.right.setFrameShape(QFrame.StyledPanel)

        self.splitter1 = QSplitter(Qt.Vertical,frameShape=QFrame.StyledPanel)
        self.splitter1.addWidget(topleft)
        self.splitter1.addWidget(bottomleft)
        self.splitter1.setSizes([100,400])

        self.splitter2 = QSplitter(Qt.Horizontal,frameShape=QFrame.StyledPanel)
        self.splitter2.addWidget(splitter1)
        self.splitter2.addWidget(right)
        self.splitter2.setSizes([550,650])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
