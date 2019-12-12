import sys
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow,QProgressBar,QPushButton,QCheckBox,QHeaderView,QAbstractScrollArea,QMessageBox,QAction,QTableWidgetItem,QTableWidget, QLineEdit, QMessageBox,QGroupBox,QVBoxLayout,QMenuBar,QTabWidget,QLabel,QHBoxLayout,QFrame,QSplitter,QStyleFactory,QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot,Qt
import time
#from proxy_scanner import ProxyScanner
import threading
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
import validators
from test_round import QRoundProgressBar
from urllib.parse import urlparse,urljoin
from subdomain_with_async import *
#from subdomain_scanner import SubdomainScanner
import threading
import os


# infodan veya herhangi bir clastan classmethod kullanarak eğer kullanıcı ayar verdiyse vs ona göre oluşturmak


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Easy Scanner'
        self.setFixedSize(600  , 550)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Application waiting.")
        mainMenu = self.menuBar()


        self.window = Window(self.statusBar,mainMenu)
        self.setCentralWidget(self.window)
        self.show()


class Window(QWidget):
    def __init__(self,statusBar,mainMenu):
        super().__init__()
        self.statusbar = statusBar
        self.menu = mainMenu
        self.url_without_schema =""
        self.url = ""
        self.threadpool = QThreadPool()

        self.init_ui()
        

        
    def init_ui(self):
        self.hbox = QHBoxLayout(self)
        self.set_frames()
        self.set_input_and_buttons()
        self.set_combobox()
        self.start_resource_monitor()
        self.set_menu()
        self.show()



    def start_on_click(self):
        if self.is_url_valid:
            self.clear_result_list()
            self.clear_infobox()
            self.disable_enable_options(True)
            self.start_action()
            pass
        else:
            self.print_error("[×] URL format is not correct")

    def stop_on_click(self):
        self.disable_enable_options(False)

    def print_error(self,message):
        self.information_list.addItem(message)

    def print_info(self,message):
        self.information_list.addItem(message)

    def print_result(self,message):
        self.result_list.addItem(message)

    def clear_infobox(self):
        self.information_list.clear()

    def clear_result_list(self):
        self.result_list.clear()

    def finish_control(self):
        self.disable_enable_options(False)


    def start_action(self):
        option_value = self.options_combobox.currentText()
        option_list = {

            'Information Gather':self.start_information_gathering,
            'Port Scanner':self.start_port_scanner,
            'Directory Scanner':self.start_directory_scanner,
            'Subdomain Scanner':self.start_subdomain_scanner,
            'Header Analysis':self.start_header_scanner,
            'Xss Scanner':self.start_xss_scanner,
            'SQLi Scanner':self.start_sqli_scanner,
            'LFi/RFi Scanner':self.start_lfi_scanner,
            'File Upload Scanner':self.start_fileupload_scanner,
        }
        option_list[option_value]()


    def start_information_gathering(self):
        self.print_info("[✔] Information Gathering started!")
        self.information_scanner = Info(self.url)
        self.information_scanner.signals.result_list.connect(self.print_result)
        self.information_scanner.signals.finish_control.connect(self.finish_control)
        self.information_scanner.signals.info_box.connect(self.print_info)
        self.threadpool.start(self.information_scanner)


    def start_port_scanner(self):
        self.print_info("[✔] Port Scanner started!")
        self.port_scanner = PortScanner(self.url_without_schema)
        self.port_scanner.signals.finish_control.connect(self.finish_control)
        self.port_scanner.signals.info_box.connect(self.print_info)
        self.port_scanner.signals.result_list.connect(self.print_result)
        self.threadpool.start(self.port_scanner)

    def start_directory_scanner(self):
        self.print_info("[✔] Directory Scanner started!")
        self.dir_scanner = DirScanner(self.url)
        self.dir_scanner.signals.finish_control.connect(self.finish_control)
        self.dir_scanner.signals.info_box.connect(self.print_info)
        self.dir_scanner.signals.result_list.connect(self.print_result)
        self.threadpool.start(self.dir_scanner)

    def start_subdomain_scanner(self):
        self.print_info("[✔] Subdomain Scanner started!")
        self.subdomain_scanner = SubdomainScanner(self.url_without_schema)
        self.subdomain_scanner.signals.finish_control.connect(self.finish_control)
        self.subdomain_scanner.signals.info_box.connect(self.print_info)
        self.subdomain_scanner.signals.result_list.connect(self.print_result)
        self.threadpool.start(self.subdomain_scanner)

    def start_header_scanner(self):
        self.print_info("[✔] Header Scanner started!")
        self.header_analysis = HeaderAnalysis(self.url)
        self.header_analysis.signals.result_list.connect(self.print_result)
        self.header_analysis.signals.finish_control.connect(self.finish_control)
        self.header_analysis.signals.info_box.connect(self.print_info)
        self.threadpool.start(self.header_analysis)
    def start_xss_scanner(self):
        self.print_info("[✔] XSS Scanner started!")

    def start_sqli_scanner(self):
        self.print_info("[✔] SQLi Scanner started!")
    def start_lfi_scanner(self):
        self.print_info("[✔] Lfi/Rfi Scanner started!")

    def start_fileupload_scanner(self):
        self.print_info("[✔] File Upload Scanner started!")

    def start_resource_monitor(self):
        pid = os.getpid()
        self.resource_monitor = ResourceMonitor(pid)
        self.resource_monitor.signals.status.connect(self.set_statusbar)
        self.threadpool.start(self.resource_monitor)

    def set_statusbar(self,cpu_value,mem_value):
        text = "CPU Usage: %{} - Memory Usage: %{}".format(cpu_value,mem_value)
        self.statusbar.showMessage(text)

    def set_menu(self):
         settingsmenu = self.menu.addMenu('Settings')
         exitmenu = self.menu.addMenu('Exit')
         newAct = QAction('New', self)
         settingsmenu   .addAction(newAct)

    @property
    def is_url_valid(self):
        # Get user input
        url = self.address_text.text()

        # Validation check
        result = validators.url(url)

        # Get url without schema
        if result:
            self.url = url
            parser = urlparse(url)
            self.url_without_schema = parser.netloc
            
        return result


    def disable_enable_options(self,is_disabled):
        self.address_text.setDisabled(is_disabled)
        self.start_button.setDisabled(is_disabled)
        self.options_combobox.setDisabled(is_disabled)
        self.stop_button.setDisabled(not is_disabled)


    def set_input_and_buttons(self):
        self.address_text = QLineEdit(self.top_frame)
        self.address_text.setPlaceholderText("https://example.com") 
        self.address_text.move(20, 20)
        self.address_text.resize(300,40)


        self.start_button = QPushButton('Start Scan', self.top_frame)
        self.start_button.clicked.connect(self.start_on_click)
        self.start_button.move(177,70)
        self.start_button.resize(70,23)

        self.stop_button = QPushButton('Stop Scan', self.top_frame)
        self.stop_button.clicked.connect(self.stop_on_click)
        self.stop_button.move(250,70)
        self.stop_button.resize(70,23)
        self.stop_button.setDisabled(True)

        self.information_label = QLabel("Information Box ",self.top_frame)
        self.information_label.setGeometry(400,3,100,10)

        self.information_list = QListWidget(self.info_frame)
        self.information_list.setMinimumSize(20,20)

        self.result_list = QListWidget(self.bottom_frame)
        self.result_list.setMinimumSize(580,375)

    def set_frames(self):
        self.top_frame    = QFrame(self)
        self.top_frame.resize(50,150)

        self.info_frame = QFrame(self.top_frame)
        self.info_frame.setFrameShape(QFrame.StyledPanel)
        self.info_frame.setGeometry(340,18,220,80)

        self.bottom_frame = QFrame(self)
        self.bottom_frame.resize(500,550)

        self.top_frame.setFrameShape(QFrame.StyledPanel)
        self.bottom_frame.setFrameShape(QFrame.StyledPanel)

        
        self.splitter1 = QSplitter(Qt.Vertical,frameShape=QFrame.StyledPanel)
        self.splitter1.addWidget(self.top_frame)
        self.splitter1.addWidget(self.bottom_frame)

        self.hbox.addWidget(self.splitter1)
        
    def set_combobox(self):
        self.options_combobox = QComboBox(self.top_frame)
        option_list = [

            'Information Gather',
            'Port Scanner',
            'Directory Scanner',
            'Subdomain Scanner',
            'Header Analysis',
            'Xss Scanner',
            'SQLi Scanner',
            'LFi/RFi Scanner',
            'File Upload Scanner',

        ]

        self.options_combobox.addItems(option_list)
        self.options_combobox.move(20, 70)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
