import sys
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow,QProgressBar,QPushButton,QCheckBox,QHeaderView,QAbstractScrollArea,QMessageBox,QAction,QTableWidgetItem,QTableWidget, QLineEdit, QMessageBox,QGroupBox,QVBoxLayout,QMenuBar,QTabWidget,QLabel,QHBoxLayout,QFrame,QSplitter,QStyleFactory,QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot,Qt
import time
from proxy_scanner import ProxyScanner
import threading
from subdomain_scanner import SubdomainScanner
from dirscanner import DirScanner
from multiprocessing import Process

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Easy Scanner'
        self.setFixedSize(1480  , 650)
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
        self.checkbox_list = []

        self.hbox = QHBoxLayout()
        self.set_frames()
        self.set_right_tabs()
        self.set_left_tabs()
        self.set_checkboxes()
        self.set_checkboxes_true()


        self.address_text = QLineEdit(self.topleft)
        self.address_text.setPlaceholderText("https://example.com") 
        self.address_text.move(70, 20)
        self.address_text.resize(300,40)

        self.start_button = QPushButton('Start Scan', self.topleft)
        self.start_button.clicked.connect(self.start_on_click)
        self.start_button.move(390,25)

        self.stop_button = QPushButton('Stop Scan', self.topleft)
        self.stop_button.clicked.connect(self.stop_on_click)
        self.stop_button.move(490,25)

        self.subscan_bar = QProgressBar(self.subscan_tab)
        self.subscan_bar.setGeometry(220, 550, 250, 20)
        self.subscan_bar.setValue(0)
        self.subscan_bar.setTextVisible(True);
        # text = "test"
        # self.subscan_bar.setFormat( text );

        self.dirscan_bar = QProgressBar(self.dirscan_tab)
        self.dirscan_bar.setGeometry(220, 550, 250, 20)
        self.dirscan_bar.setValue(0)
        self.dirscan_bar.setTextVisible(True);




        self.sub_list = QListWidget(self.subscan_tab)
        self.sub_list.setMinimumSize(740, 550)

        self.dir_list = QListWidget(self.dirscan_tab)
        self.dir_list.setMinimumSize(740, 550)


        self.setLayout(self.hbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.show()

    @pyqtSlot()
    def start_on_click(self):
        self.address_text.setDisabled(True)
        self.start_button.setDisabled(True)
        for box in self.checkbox_list:
            box.setDisabled(True)
        self.t1 = threading.Thread(target=self.start_sub_scanner)
        self.t2 = threading.Thread(target=self.start_dir_scanner)
        self.t1.daemon = True
        self.t2.daemon = True
        self.t1.start()
        self.t2.start()


    def start_sub_scanner(self):
        proxy_scanner = SubdomainScanner("instra.com",self.sub_list,self.subscan_bar)

    def start_dir_scanner(self):
        dir_scanner = DirScanner("https://bekchy.com",self.dir_list,self.dirscan_bar)


    @pyqtSlot()
    def stop_on_click(self):
        self.address_text.setDisabled(False)
        self.start_button.setDisabled(False)
        for box in self.checkbox_list:
            box.setDisabled(False)
        self.t.kill()

    def set_frames(self):
        self.topleft =QFrame(self)
        self.topleft.setFrameShape(QFrame.StyledPanel)

        self.bottomleft = QFrame(self)
        self.bottomleft.setFrameShape(QFrame.StyledPanel)

        self.right = QFrame(self)
        self.right.setFrameShape(QFrame.StyledPanel)

        self.splitter1 = QSplitter(Qt.Vertical,frameShape=QFrame.StyledPanel)
        self.splitter1.addWidget(self.topleft)
        self.splitter1.addWidget(self.bottomleft)
        self.splitter1.setSizes([125,400])

        self.splitter2 = QSplitter(Qt.Horizontal,frameShape=QFrame.StyledPanel)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.addWidget(self.right)
        self.splitter2.setSizes([100,650])

        self.hbox.addWidget(self.splitter1)
        self.hbox.addWidget(self.splitter2)

    def set_right_tabs(self):
        self.righttabs = QTabWidget(self.right)

        self.righttabs.setMovable(True)
        self.righttabs.setDocumentMode(True)
        self.righttabs.setUsesScrollButtons(True)
        self.subscan_tab = QWidget()

        self.dirscan_tab = QWidget()
        self.cms_tab = QWidget()
        self.headers_tab = QWidget()
        self.xss_tab = QWidget()
        self.sqli_tab = QWidget()
        self.lfi_tab = QWidget()
        self.righttabs.resize(740,610)
        self.righttabs.addTab(self.subscan_tab,"Subdomain Scanner")
        self.righttabs.addTab(self.dirscan_tab,"Directory Scanner")
        self.righttabs.addTab(self.cms_tab,"CMS Scanner")
        self.righttabs.addTab(self.headers_tab,"Header Analysis")
        self.righttabs.addTab(self.xss_tab,"Xss Vuln")
        self.righttabs.addTab(self.sqli_tab,"SQLi Vuln")
        self.righttabs.addTab(self.lfi_tab,"LFi/RFi Vuln")
        self.righttabs.removeTab(6)

    def change_subscan_tab(self):
        if not self.sub_ch.isChecked():
            self.subscan_tab = self.righttabs.widget(0)  # save it for later
            self.righttabs.removeTab(0)
        else:
            self.righttabs.insertTab(0, self.subscan_tab, 'Subdomain Scanner' )

    def change_dirscan_tab(self):
        if not self.dir_ch.isChecked():
            self.dirscan_tab = self.righttabs.widget(1)  # save it for later
            self.righttabs.removeTab(1)
        else:
            self.righttabs.insertTab(1, self.dirscan_tab, 'Directory Scanner' )

    def set_left_tabs(self):
        self.leftabs = QTabWidget(self.bottomleft)

        self.leftabs.setMovable(True)
        self.leftabs.setDocumentMode(True)
        self.leftabs.setUsesScrollButtons(True)
        self.leftabs.setElideMode(Qt.ElideRight)

        self.info_tab = QWidget()
        self.ports_tab = QWidget()
        self.whois_tab = QWidget()
        self.tech_tab = QWidget()
        self.tab_5 = QWidget()
        self.leftabs.resize(600,500)
        self.leftabs.addTab(self.info_tab,"Info")
        self.leftabs.addTab(self.ports_tab,"Port Scanner")
        self.leftabs.addTab(self.whois_tab,"Whois Info")
        self.leftabs.addTab(self.tech_tab,"Web Technologies")
        self.leftabs.addTab(self.tab_5,"Tool Information")

    def set_checkboxes(self):
        self.port_ch = QCheckBox("Port Scan",self.topleft)
        #self.port_ch.stateChanged.connect(self.clickBox)
        self.port_ch.move(50,60)
        self.port_ch.resize(320,40)
        self.checkbox_list.append(self.port_ch)

        self.whois_ch = QCheckBox("Whois",self.topleft)
        #self.b.stateChanged.connect(self.clickBox)
        self.whois_ch.move(170,60)
        self.whois_ch.resize(320,40)
        self.checkbox_list.append(self.whois_ch)

        self.tech_ch = QCheckBox("Web Tech",self.topleft)
        #self.b.stateChanged.connect(self.clickBox)
        self.tech_ch.move(290,60)
        self.tech_ch.resize(320,40)
        self.checkbox_list.append(self.tech_ch)

        self.sub_ch = QCheckBox("Sub Scan",self.topleft)
        self.sub_ch.stateChanged.connect(self.change_subscan_tab)
        self.sub_ch.move(410,60)
        self.sub_ch.resize(320,40)
        self.checkbox_list.append(self.sub_ch)

        self.dir_ch = QCheckBox("Dir Scan",self.topleft)
        self.dir_ch.stateChanged.connect(self.change_dirscan_tab)
        self.dir_ch.move(530,60)
        self.dir_ch.resize(320,40)
        self.checkbox_list.append(self.dir_ch)

        self.cms_ch = QCheckBox("CMS Scan",self.topleft)
        #self.b.stateChanged.connect(self.clickBox)
        self.cms_ch.move(50,90)
        self.cms_ch.resize(320,40)
        self.checkbox_list.append(self.cms_ch)

        self.head_ch = QCheckBox("Head Analy",self.topleft)
        #self.b.stateChanged.connect(self.clickBox)
        self.head_ch.move(170,90)
        self.head_ch.resize(320,40)
        self.checkbox_list.append(self.head_ch)

        self.Lfi_ch = QCheckBox("LFi/RFi",self.topleft)
        #self.b.stateChanged.connect(self.clickBox)
        self.Lfi_ch.move(290,90)
        self.Lfi_ch.resize(320,40)
        self.checkbox_list.append(self.Lfi_ch)

        self.xss_ch = QCheckBox("XSS",self.topleft)
        #self.b.stateChanged.connect(self.clickBox)
        self.xss_ch.move(410,90)
        self.xss_ch.resize(320,40)
        self.checkbox_list.append(self.xss_ch)

        self.sql_ch = QCheckBox("SQLi",self.topleft)
        #self.b.stateChanged.connect(self.clickBox)
        self.sql_ch.move(530,90)
        self.sql_ch.resize(320,40)
        self.checkbox_list.append(self.sql_ch)

    def set_checkboxes_true(self):
        for box in self.checkbox_list:
            box.setChecked(True)
    # def insert_item_to_tab(self,listwidget,information):
    #     # listwidget.insertItem(0,information)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
