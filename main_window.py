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
from header_analysis import HeaderAnalysis
from port_scanner import PortScanner
from tech_scanner import TechScanner
from getwhois import Whois
import psutil
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

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
        self.set_address_and_buttons()



        self.sub_list = QListWidget(self.subscan_tab)
        self.sub_list.setMinimumSize(740, 550)

        self.dir_list = QListWidget(self.dirscan_tab)
        self.dir_list.setMinimumSize(740, 550)

        self.port_list = QListWidget(self.ports_tab)
        self.port_list.setMinimumSize(505,430)

        self.header_list = QListWidget(self.headers_tab)
        self.header_list.setMinimumSize(740, 550)

        self.whois_list = QListWidget(self.whois_tab)
        self.whois_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.whois_list.setMinimumSize(505, 430)
        #self.whois_list.setMaximumSize(505,400)


        self.tech_list = QListWidget(self.tech_tab)
        self.tech_list.setMinimumSize(505, 430)

        self.port_bar = QProgressBar(self.ports_tab)
        self.port_bar.setGeometry(150, 400, 250, 20)
        self.port_bar.setValue(0)
        self.port_bar.setTextVisible(True);

        self.dirscan_bar = QProgressBar(self.dirscan_tab)
        self.dirscan_bar.setGeometry(220, 550, 250, 20)
        self.dirscan_bar.setValue(0)
        self.dirscan_bar.setTextVisible(True);

        self.subscan_bar = QProgressBar(self.subscan_tab)
        self.subscan_bar.setGeometry(220, 550, 250, 20)
        self.subscan_bar.setValue(0)
        self.subscan_bar.setTextVisible(True);




        self.setLayout(self.hbox)
        #QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.show()



    #     pid  = self.get_pid()
    #     process = psutil.Process(pid)


    # def test(self,process):
    #     while True:
            
    #         print(process.status())
    #         print(process.cpu_percent(interval=1.0))
    #         print(process.cpu_num())
    #         print(process.num_threads())
    #         time.sleep(2)

    # def get_pid(self):
    #     for i in psutil.pids():
    #         if "test.py" in psutil.Process(i).cmdline():
    #             return psutil.Process(i).pid
    @pyqtSlot()
    def start_on_click(self):
        self.address_text.setDisabled(True)
        self.start_button.setDisabled(True)
        for box in self.checkbox_list:
            box.setDisabled(True)

        
        # self.t1 = threading.Thread(target=self.start_sub_scanner)
        # self.t2 = threading.Thread(target=self.start_dir_scanner)
        # self.t3 = threading.Thread(target=self.start_header_analysis)
        # self.t4 = threading.Thread(target=self.start_port_scanner)


        # self.t1.daemon = True
        # self.t2.daemon = True
        # self.t3.daemon = True
        # self.t4.daemon = True

        # self.t1.start()
        # self.t2.start()
        # self.t3.start()
        # self.t4.start()

        port_scanner = PortScanner("176.53.35.152") # Any other args, kwargs are passed to the run function
        port_scanner.signals.progress.connect(self.update_progress_bar_port)
        port_scanner.signals.list.connect(self.update_list_port)

        sub_scanner = SubdomainScanner("instra.com")
        sub_scanner.signals.progress.connect(self.update_progress_bar_sub)
        sub_scanner.signals.list.connect(self.update_list_sub)

        dir_scanner = DirScanner("https://bekchy.com")
        dir_scanner.signals.progress.connect(self.update_progress_bar_dir)
        dir_scanner.signals.list.connect(self.update_list_dir)

        header_analysis = HeaderAnalysis("https://bekchy.com")
        header_analysis.signals.list.connect(self.update_header_analysis_list)

        tech_scanner = TechScanner("https://wpmavi.com")
        tech_scanner.signals.list.connect(self.update_tech_list)

        whois = Whois("ahmetcankaraagacli.com")
        whois.signals.list.connect(self.update_whois_list)

        #dir_scanner = DirScanner("https://bekchy.com",self.dir_list)
        #dir_scanner.signals.progress.connect(self.update_progress_bar_dir)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        #self.port_scanner.progressbar_changer.connect(self.update_progress_bar)
        self.threadpool.start(port_scanner)
        self.threadpool.start(sub_scanner)
        self.threadpool.start(dir_scanner)
        self.threadpool.start(header_analysis)
        self.threadpool.start(tech_scanner)
        self.threadpool.start(whois)
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        #self.threadpool.start(dir_scanner)



    def update_whois_list(self,counter,text):
        self.whois_list.insertItem(counter,text)

    def update_tech_list(self,counter,text):
        self.tech_list.insertItem(counter,text)



    def update_header_analysis_list(self,counter,text,check):
        self.header_list.insertItem(counter,text)
        if check:
            self.header_list.item(counter).setForeground(QBrush(QtCore.Qt.blue))
        else:
            self.header_list.item(counter).setForeground(QBrush(QtCore.Qt.red))



    def update_progress_bar_port(self,value,text):
        self.port_bar.setFormat(text);
        self.port_bar.setValue(value)

    def update_progress_bar_sub(self,value,text):
        self.subscan_bar.setFormat(text)
        self.subscan_bar.setValue(value)
        #print("test")

    def update_progress_bar_dir(self,value,text):
        self.dirscan_bar.setFormat(text)
        self.dirscan_bar.setValue(value)

    def update_list_port(self,text,counter):
        self.port_list.insertItem(counter,text)

    def update_list_dir(self,text,counter):
        self.dir_list.insertItem(counter,text)

    def update_list_sub(self,text,counter):
        self.sub_list.insertItem(counter,text)


    @pyqtSlot()
    def stop_on_click(self):
        self.address_text.setDisabled(False)
        self.start_button.setDisabled(False)
        for box in self.checkbox_list:
            box.setDisabled(False)
        self.t.kill()

    def set_address_and_buttons(self):

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

    def set_frames(self):
        self.topleft =QFrame(self)
        self.topleft.setFrameShape(QFrame.StyledPanel)
        #self.topleft.setStyleSheet("QFrame {background:#2E151B}")

        self.bottomleft = QFrame(self)
        self.bottomleft.setFrameShape(QFrame.StyledPanel)
        #self.bottomleft.setObjectName("myObject")
        #self.bottomleft.setStyleSheet("#myObject { border: 2px solid black; }")
        #self.bottomleft.setStyleSheet("QFrame{background: #2F4454}")

        #self.test_button = QPushButton('test', self.bottomleft)
        #self.start_button.clicked.connect(self.start_on_click)
        #self.test_button.move(600,200)

        self.cpu_bar = QProgressBar(self.bottomleft)
        self.cpu_bar.setGeometry(150, 400, 170, 20)
        self.cpu_bar.setValue(40)
        self.cpu_bar.setTextVisible(True);
        self.cpu_bar.move(530,50)
        template_css = """QProgressBar {font-weight: bold;}"""
        self.cpu_bar.setStyleSheet(template_css)
        self.cpu_bar.setFormat("CPU [%40]")


        self.memory_bar = QProgressBar(self.bottomleft)
        self.memory_bar.setGeometry(150, 400, 170, 20)
        self.memory_bar.setValue(60)
        template_css = """QProgressBar {font-weight: bold;}"""
        self.memory_bar.setStyleSheet(template_css)
        self.memory_bar.setTextVisible(True);
        self.memory_bar.move(530,90)
        self.memory_bar.setFormat("Mem [%60]")





        self.right = QFrame(self)
        self.right.setFrameShape(QFrame.StyledPanel)
        #self.right.setObjectName("myObject")
        #self.right.setStyleSheet("QFrame { background:#2E151B;}")

        self.splitter1 = QSplitter(Qt.Vertical,frameShape=QFrame.StyledPanel)
        self.splitter1.addWidget(self.topleft)
        self.splitter1.addWidget(self.bottomleft)
        self.splitter1.setSizes([150,550])

        self.splitter2 = QSplitter(Qt.Horizontal,frameShape=QFrame.StyledPanel)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.addWidget(self.right)
        self.splitter2.setSizes([100,600])

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
        self.righttabs.resize(740,600)
        self.righttabs.addTab(self.subscan_tab,"Subdomain Scanner")
        self.righttabs.addTab(self.dirscan_tab,"Directory Scanner")
        self.righttabs.addTab(self.cms_tab,"CMS Scanner")
        self.righttabs.addTab(self.headers_tab,"Header Analysis")
        self.righttabs.addTab(self.xss_tab,"Xss Vuln")
        self.righttabs.addTab(self.sqli_tab,"SQLi Vuln")
        self.righttabs.addTab(self.lfi_tab,"LFi/RFi Vuln")
        #self.righttabs.removeTab(6)

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

    def change_cms_tab(self):
        if not self.cms_ch.isChecked():
            self.cms_tab = self.righttabs.widget(2)  # save it for later
            self.righttabs.removeTab(2)
        else:
            self.righttabs.insertTab(2, self.cms_tab, 'CMS Scanner' )

    def change_header_tab(self):
        if not self.head_ch.isChecked():
            self.headers_tab = self.righttabs.widget(3)  # save it for later
            self.righttabs.removeTab(3)
        else:
            self.righttabs.insertTab(3, self.headers_tab, 'Header Scanner' )

    def change_xss_tab(self):
        if not self.xss_ch.isChecked():
            self.xss_tab = self.righttabs.widget(4)  # save it for later
            self.righttabs.removeTab(4)
        else:
            self.righttabs.insertTab(4, self.xss_tab, 'Xss Vuln' )

    def change_sql_tab(self):
        if not self.sql_ch.isChecked():
            self.sqli_tab = self.righttabs.widget(5)  # save it for later
            self.righttabs.removeTab(5)
        else:
            self.righttabs.insertTab(5, self.sqli_tab, 'SQLi Vuln' )

    def change_lfi_tab(self):
        if not self.Lfi_ch.isChecked():
            self.lfi_tab = self.righttabs.widget(6)  # save it for later
            self.righttabs.removeTab(6)
        else:
            self.righttabs.insertTab(6, self.lfi_tab, 'LFi/RFi Vuln' )

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
        self.leftabs.resize(480,500)
        #self.leftabs.setStyleSheet("QTabWidget{background-color: blue}")

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
        self.cms_ch.stateChanged.connect(self.change_cms_tab)
        self.cms_ch.move(50,90)
        self.cms_ch.resize(320,40)
        self.checkbox_list.append(self.cms_ch)

        self.head_ch = QCheckBox("Head Analy",self.topleft)
        self.head_ch.stateChanged.connect(self.change_header_tab)
        self.head_ch.move(170,90)
        self.head_ch.resize(320,40)
        self.checkbox_list.append(self.head_ch)

        self.Lfi_ch = QCheckBox("LFi/RFi",self.topleft)
        self.Lfi_ch.stateChanged.connect(self.change_lfi_tab)
        self.Lfi_ch.move(290,90)
        self.Lfi_ch.resize(320,40)
        self.checkbox_list.append(self.Lfi_ch)

        self.xss_ch = QCheckBox("XSS",self.topleft)
        self.xss_ch.stateChanged.connect(self.change_xss_tab)
        self.xss_ch.move(410,90)
        self.xss_ch.resize(320,40)
        self.checkbox_list.append(self.xss_ch)

        self.sql_ch = QCheckBox("SQLi",self.topleft)
        self.sql_ch.stateChanged.connect(self.change_sql_tab)
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
