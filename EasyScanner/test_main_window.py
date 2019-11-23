import sys
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow,QProgressBar,QPushButton,QCheckBox,QHeaderView,QAbstractScrollArea,QMessageBox,QAction,QTableWidgetItem,QTableWidget, QLineEdit, QMessageBox,QGroupBox,QVBoxLayout,QMenuBar,QTabWidget,QLabel,QHBoxLayout,QFrame,QSplitter,QStyleFactory,QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot,Qt
import time
from proxy_scanner import ProxyScanner
import threading
from subdomain_scanner import SubdomainScanner
from directory_scanner import DirScanner
from multiprocessing import Process
from header_analysis import HeaderAnalysis
from port_scanner import *
from getwhois import Whois
from info import Info
import psutil
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import psutil
import time
from resource_monitor import ResourceMonitor

from test_round import QRoundProgressBar

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Easy Scanner'
        self.setFixedSize(1000  , 700)
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
        self.url = ""
        self.url_without_schema = ""
        self.url_control = False

        self.checkbox_list = []
        self.hbox = QHBoxLayout()
        self.set_frames()
        self.set_tabs()
        self.set_address_and_buttons()
        self.set_checkboxes()
        self.set_checkboxes_true()
        self.set_lists()
        self.set_resource_monitor()
        
        self.resource_monitor = ResourceMonitor(self.get_pid())
        self.resource_monitor.signals.monitor.connect(self.update_resource_monitor)
        


        self.setLayout(self.hbox)
        #QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.threadpool = QThreadPool()
        self.threadpool.start(self.resource_monitor)

        self.info_list = QListWidget(self.info_tab)
        self.info_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.info_list.setMinimumSize(1000, 480)
        #self.info_list.insertItem(0,"test")
        self.show()

    def get_pid(self):
        return os.getpid()



    def set_resource_monitor(self):
        self.label_monitor = QLabel("Easy Scanner Resource Usage ",self.top)
        self.label_monitor.setGeometry(670,7,250,20)
        self.cpu_monitor = QRoundProgressBar(self.top)
        self.cpu_monitor.setFixedSize(110, 110)
        self.cpu_monitor.setName("CPU")
        self.cpu_monitor.setDataPenWidth(3)
        self.cpu_monitor.setOutlinePenWidth(3)
        self.cpu_monitor.setDonutThicknessRatio(0.85)
        self.cpu_monitor.setFormat('%v | %p %')
        self.cpu_monitor.setDecimals(1)
        # self.bar.resetFormat()
        self.cpu_monitor.setNullPosition(90)
        self.cpu_monitor.setBarStyle(QRoundProgressBar.StyleDonut)
        self.cpu_monitor.setDataColors([(0., QtGui.QColor.fromRgb(0,255,0)), (0.5, QtGui.QColor.fromRgb(255,50,0)), (1., QtGui.QColor.fromRgb(255,0,0))])
        self.cpu_monitor.setRange(0, 100)
        self.cpu_monitor.setValue(0)
        self.cpu_monitor.setFormat('%v | %p %')
        self.cpu_monitor.setGeometry(650,30,3,4)    


        self.mem_monitor = QRoundProgressBar(self.top)
        self.mem_monitor.setFixedSize(110, 110)
        self.mem_monitor.setName("Mem")
        self.mem_monitor.setDataPenWidth(3)
        self.mem_monitor.setOutlinePenWidth(3)
        self.mem_monitor.setDonutThicknessRatio(0.85)
        self.mem_monitor.setFormat('%v | %p %')
        self.mem_monitor.setDecimals(1)
        # self.bar.resetFormat()
        self.mem_monitor.setNullPosition(90)
        self.mem_monitor.setBarStyle(QRoundProgressBar.StyleDonut)
        self.mem_monitor.setDataColors([(0., QtGui.QColor.fromRgb(0,255,0)), (0.5, QtGui.QColor.fromRgb(255,50,0)), (1., QtGui.QColor.fromRgb(255,0,0))])
        self.mem_monitor.setRange(0, 100)
        self.mem_monitor.setValue(0)
        self.mem_monitor.setFormat('%v | %p %')
        self.mem_monitor.setGeometry(800,30,3,4)  



    def update_resource_monitor(self,cpu_value,mem_value):
        self.cpu_monitor.setValue(cpu_value)
        self.mem_monitor.setValue(mem_value)

    @pyqtSlot()
    def start_on_click(self):
        self.set_widget_abilities(True)
        #self.set_lists_clear()
        self.get_url_address_text()
        #crawlar eklenecek

        
        self.info_worker = Info(self.url)
        self.info_worker.signals.domain_control.connect(self.check_domain)
        self.info_worker.signals.info_liste.connect(self.update_info_list)
        self.info_worker.signals.control.connect(self.start_threads)

        self.threadpool.start(self.info_worker)



    def start_threads(self,is_okay):
        if is_okay:
            self.port_scanner = PortScanner(self.url_without_schema)
            self.port_scanner.signals.port_list.connect(self.update_list_port)
            self.port_scanner.signals.info_list.connect(self.update_info_list)
            self.threadpool.start(self.port_scanner)
            self.dir_scanner = DirScanner(self.url)
            self.dir_scanner.signals.info_list.connect(self.update_info_list)
            self.dir_scanner.signals.dir_list.connect(self.update_list_dir)
            
            self.threadpool.start(self.dir_scanner)


    @pyqtSlot()
    def stop_on_click(self):
        self.address_text.setDisabled(False)
        self.start_button.setDisabled(False)
        for box in self.checkbox_list:
            box.setDisabled(False)
            
    def check_domain(self,is_valid,url,url_without_schema):
        if is_valid:
            self.info_list.addItem("[✔] URL validated!")
            self.url_control = True
            self.url = url
            self.url_without_schema = url_without_schema
            self.url_control = True
        else:
            self.info_list.addItem("[×] Url is not validated!")
            self.set_widget_abilities(False)
            self.url_control = False


    def get_url_address_text(self):
        self.url = self.address_text.text()


    def set_widget_abilities(self,ability):
        self.address_text.setDisabled(ability)
        self.start_button.setDisabled(ability)
        for box in self.checkbox_list:
            box.setDisabled(ability)

    def set_lists_clear(self):
        self.info_list.clear()

    def update_info_list(self,message):
        self.info_list.addItem(message)




    def set_lists(self):
        self.port_list = QListWidget(self.portscan_tab)
        self.port_list.setMinimumSize(505,430)

        self.sub_list = QListWidget(self.subscan_tab)
        self.sub_list.setMinimumSize(505,430)

        self.dir_list = QListWidget(self.dirscan_tab)
        self.dir_list.setMinimumSize(505,430)

        self.crawler_list = QListWidget(self.crawler_tab)
        self.crawler_list.setMinimumSize(505,430)

        self.header_list = QListWidget(self.headers_tab)
        self.header_list.setMinimumSize(505,430)

        self.xss_list = QListWidget(self.xss_tab)
        self.xss_list.setMinimumSize(505,430)

        self.sqli_list = QListWidget(self.sqli_tab)
        self.sqli_list.setMinimumSize(505,430)

        self.lfi_list = QListWidget(self.lfi_tab)
        self.lfi_list.setMinimumSize(505,430)

        self.fileupload_list = QListWidget(self.fileupload_tab)
        self.fileupload_list.setMinimumSize(505,430)

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

    def update_list_port(self,text):
        self.port_list.addItem(text)

    def update_list_dir(self,text):
        self.dir_list.addItem(text)

    def update_list_sub(self,text,counter):
        self.sub_list.insertItem(counter,text)




    def set_address_and_buttons(self):

            self.address_text = QLineEdit(self.top)
            self.address_text.setPlaceholderText("https://example.com") 
            self.address_text.move(30, 28)
            self.address_text.resize(300,40)

            self.start_button = QPushButton('Start Scan', self.top)
            self.start_button.clicked.connect(self.start_on_click)
            self.start_button.move(340,22)

            self.stop_button = QPushButton('Stop Scan', self.top)
            self.stop_button.clicked.connect(self.stop_on_click)
            self.stop_button.move(340,58)

    def set_frames(self):
        self.top =QFrame(self)
        self.top.setFrameShape(QFrame.StyledPanel)
        #self.top.setStyleSheet("QFrame {background:#2E151B}")

        self.bottom = QFrame(self)
        self.bottom.setFrameShape(QFrame.StyledPanel)

        self.splitter1 = QSplitter(Qt.Vertical,frameShape=QFrame.StyledPanel)
        self.splitter1.addWidget(self.top)
        self.splitter1.addWidget(self.bottom)
        self.splitter1.setSizes([160,550])

        self.hbox.addWidget(self.splitter1)

    def set_tabs(self):
        self.tabs = QTabWidget(self.bottom)
        self.tabs.setMovable(True)
        #self.tabs.setDocumentMode(True)
        self.tabs.setUsesScrollButtons(True)
        self.crawler_tab    = QWidget()
        self.subscan_tab    = QWidget()
        self.dirscan_tab    = QWidget()
        self.portscan_tab   = QWidget()
        self.info_tab       = QWidget()
        self.cms_tab        = QWidget()
        self.headers_tab    = QWidget()
        self.xss_tab        = QWidget()
        self.sqli_tab       = QWidget()
        self.lfi_tab        = QWidget()
        self.fileupload_tab = QWidget()
        self.tabs.resize(1000,600)
        self.tabs.addTab(self.info_tab,"Info")                  #0
        self.tabs.addTab(self.portscan_tab,"Port Scanner")      #1
        self.tabs.addTab(self.subscan_tab,"Subdomain Scanner")  #2
        self.tabs.addTab(self.dirscan_tab,"Directory Scanner")  #3
        self.tabs.addTab(self.crawler_tab,"Crawler")            #4
        self.tabs.addTab(self.headers_tab,"Header Analysis")    #5
        self.tabs.addTab(self.xss_tab,"Xss Vuln")               #6
        self.tabs.addTab(self.sqli_tab,"SQLi Vuln")             #7
        self.tabs.addTab(self.lfi_tab,"LFi/RFi Vuln")           #8
        self.tabs.addTab(self.fileupload_tab,"File Upload")     #9
        #self.righttabs.removeTab(6)

    def change_portscan_tab(self):
        if not self.port_ch.isChecked():
            self.portscan_tab = self.tabs.widget(1)  # save it for later
            self.tabs.removeTab(1)
        else:
            self.tabs.insertTab(1, self.portscan_tab, 'Port Scanner' )

    def change_subscan_tab(self):
        if not self.sub_ch.isChecked():
            self.subscan_tab = self.tabs.widget(2)  # save it for later
            self.tabs.removeTab(2)
        else:
            self.tabs.insertTab(2, self.subscan_tab, 'Subdomain Scanner' )

    def change_dirscan_tab(self):
        if not self.dir_ch.isChecked():
            self.dirscan_tab = self.tabs.widget(3)  # save it for later
            self.tabs.removeTab(3)
        else:
            self.tabs.insertTab(3, self.dirscan_tab, 'Directory Scanner' )

    def change_crawler_tab(self):
        if not self.crawler_ch.isChecked():
            self.crawler_tab = self.tabs.widget(4)  # save it for later
            self.tabs.removeTab(4)
        else:
            self.tabs.insertTab(4, self.crawler_tab, 'Crawler' )       

    def change_header_tab(self):
        if not self.head_ch.isChecked():
            self.headers_tab = self.tabs.widget(5)  # save it for later
            self.tabs.removeTab(5)
        else:
            self.tabs.insertTab(5, self.headers_tab, 'Header Scanner' )

    def change_xss_tab(self):
        if not self.xss_ch.isChecked():
            self.xss_tab = self.tabs.widget(6)  # save it for later
            self.tabs.removeTab(6)
        else:
            self.tabs.insertTab(6, self.xss_tab, 'Xss Vuln' )

    def change_sql_tab(self):
        if not self.sql_ch.isChecked():
            self.sqli_tab = self.tabs.widget(7)  # save it for later
            self.tabs.removeTab(7)
        else:
            self.tabs.insertTab(7, self.sqli_tab, 'SQLi Vuln' )

    def change_lfi_tab(self):
        if not self.Lfi_ch.isChecked():
            self.lfi_tab = self.tabs.widget(8)  # save it for later
            self.tabs.removeTab(8)
        else:
            self.tabs.insertTab(8, self.lfi_tab, 'LFi/RFi Vuln' )

    def change_fileupload_tab(self):
        if not self.fileupload_ch.isChecked():
            self.fileupload_tab = self.tabs.widget(9)  # save it for later
            self.tabs.removeTab(9)
        else:
            self.tabs.insertTab(9, self.fileupload_tab, 'File Upload' )

    def set_checkboxes(self):
        self.port_ch = QCheckBox("Port Scan",self.top)
        self.port_ch.stateChanged.connect(self.change_portscan_tab)
        self.port_ch.move(20,80)
        self.port_ch.resize(320,40)
        self.checkbox_list.append(self.port_ch)

        self.sub_ch = QCheckBox("Sub Scan",self.top)
        self.sub_ch.stateChanged.connect(self.change_subscan_tab)
        self.sub_ch.move(110,80)
        self.sub_ch.resize(320,40)
        self.checkbox_list.append(self.sub_ch)

        self.dir_ch = QCheckBox("Dir Scan",self.top)
        self.dir_ch.stateChanged.connect(self.change_dirscan_tab)
        self.dir_ch.move(200,80)
        self.dir_ch.resize(320,40)
        self.checkbox_list.append(self.dir_ch)

        self.crawler_ch = QCheckBox("Crawler",self.top)
        self.crawler_ch.stateChanged.connect(self.change_crawler_tab)
        self.crawler_ch.move(290,80)
        self.crawler_ch.resize(320,40)
        self.checkbox_list.append(self.crawler_ch)

        self.head_ch = QCheckBox("Header analy",self.top)
        self.head_ch.stateChanged.connect(self.change_header_tab)
        self.head_ch.move(380,80)
        self.head_ch.resize(320,40)
        self.checkbox_list.append(self.head_ch)

        self.xss_ch = QCheckBox("XSS",self.top)
        self.xss_ch.stateChanged.connect(self.change_xss_tab)
        self.xss_ch.move(20,110)
        self.xss_ch.resize(320,40)
        self.checkbox_list.append(self.xss_ch)

        self.sql_ch = QCheckBox("SQLi",self.top)
        self.sql_ch.stateChanged.connect(self.change_sql_tab)
        self.sql_ch.move(110,110)
        self.sql_ch.resize(320,40)
        self.checkbox_list.append(self.sql_ch)

        self.Lfi_ch = QCheckBox("LFi/RFi",self.top)
        self.Lfi_ch.stateChanged.connect(self.change_lfi_tab)
        self.Lfi_ch.move(200,110)
        self.Lfi_ch.resize(320,40)
        self.checkbox_list.append(self.Lfi_ch)

        self.fileupload_ch = QCheckBox("File Upload",self.top)
        self.fileupload_ch.stateChanged.connect(self.change_fileupload_tab)
        self.fileupload_ch.move(290,110)
        self.fileupload_ch.resize(320,40)
        self.checkbox_list.append(self.fileupload_ch)

    def set_checkboxes_true(self):
        for box in self.checkbox_list:
            box.setChecked(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
