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
from crawler import Crawler
from xss_scaner import XssScanner
import os
from sql_scanner import SqliScanner


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
        menubar = self.menuBar()


        self.window = Window(self.statusBar,menubar)
        self.setCentralWidget(self.window)
        self.show()


class Window(QWidget):
    def __init__(self,statusBar,menubar):
        super().__init__()
        self.statusbar = statusBar
        self.menubar = menubar
        self.url_without_schema =""
        self.url = ""
        self.login_form = None
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
            'Crawler':self.start_crawler,
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

    def start_crawler(self):
        self.print_info("[✔] Crawler started!")
        self.crawler = Crawler(self.url,self.login_form)
        self.crawler.signals.result_list.connect(self.print_result)
        self.crawler.signals.finish_control.connect(self.finish_control)
        self.crawler.signals.info_box.connect(self.print_info)
        self.threadpool.start(self.crawler)
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

        self.xss_scanner = XssScanner(self.url,self.login_form)
        self.xss_scanner.signals.info_box.connect(self.print_info)
        self.xss_scanner.signals.result_list.connect(self.print_result)
        self.xss_scanner.signals.finish_control.connect(self.finish_control)
        self.threadpool.start(self.xss_scanner)


    def start_sqli_scanner(self):
        self.print_info("[✔] SQLi Scanner started!")
        self.sqli_scanner = SqliScanner(self.url,self.login_form)
        self.sqli_scanner.signals.result_list.connect(self.print_result)
        self.sqli_scanner.signals.info_box.connect(self.print_info)
        self.sqli_scanner.signals.finish_control.connect(self.finish_control)
        self.threadpool.start(self.sqli_scanner)
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
        settingsmenu = self.menubar.addMenu('Settings')
        settingsAct = QAction('Settings', self)
        settingsAct.setShortcut("Ctrl+S")
        settingsAct.setStatusTip('Set Scanner Settings')
        settingsAct.triggered.connect(self.show_settings_window)

        settingsmenu.addAction(settingsAct)

        exitmenu = self.menubar.addMenu('Exit')
        exitAct = QAction('Exit',self)
        exitmenu.addAction(exitAct)

    def set_login_settings(self):
        user_input_name = self.form_input_name_user.text()
        user_input_value = self.form_input_value_user.text()

        password_input_name = self.form_input_name_password.text()
        password_input_value  = self.form_input_value_password.text()

        form_address = self.form_url_address_line.text()
        form_action = self.form_action_url_line.text()

        self.login_form = {}
        self.login_form['user_name_field'] = user_input_name
        self.login_form['user_value_field'] = user_input_value
        self.login_form['password_name_field'] = password_input_name
        self.login_form['password_value_field'] = password_input_value
        self.login_form['url'] = form_address
        self.login_form['action'] = form_action



    def show_settings_window(self):
        self.dlg = QDialog(self)
        self.dlg.setFixedSize(400, 250)
        self.dlg.setWindowTitle("Settings")

        # Initialize tab screen
        self.tabs = QTabWidget(self.dlg)
        self.general_settings_tab = QWidget()
        self.login_tab = QWidget()
        self.tabs.resize(400,270)
        
        # Add tabs
        self.tabs.addTab(self.general_settings_tab,"General Settings")
        self.tabs.addTab(self.login_tab,"Login Settings")
        
        # Create first tab
        self.general_settings_tab.layout = QVBoxLayout(self.dlg)
        self.pushButton1 = QPushButton("PyQt5 button",self.general_settings_tab)

        self.label_login_information = QLabel(self.login_tab)
        self.label_login_information.setText('Login Form Informations')
        self.label_login_information.move(10,10)

        self.label_input_name_user = QLabel(self.login_tab)
        self.label_input_name_user.setText('Input Name: ')
        self.label_input_name_user.move(20,50)

        self.label_input_name_password = QLabel(self.login_tab)
        self.label_input_name_password.setText('Input Name: ')
        self.label_input_name_password.move(20,80)


        self.label_input_value_user = QLabel(self.login_tab)
        self.label_input_value_user.setText('Input Value: ')
        self.label_input_value_user.move(210,50)

        self.label_input_value_password = QLabel(self.login_tab)
        self.label_input_value_password.setText('Input Value: ')
        self.label_input_value_password.move(210,80)

        self.form_input_name_user = QLineEdit(self.login_tab)
        self.form_input_name_user.resize(100,18)
        self.form_input_name_user.move(100,50)

        self.form_input_name_password = QLineEdit(self.login_tab)
        self.form_input_name_password.resize(100,18)
        self.form_input_name_password.move(100,80)

        self.form_input_value_user = QLineEdit(self.login_tab)
        self.form_input_value_user.resize(100,18)
        self.form_input_value_user.move(285,50)

        self.form_input_value_password = QLineEdit(self.login_tab)
        self.form_input_value_password.resize(100,18)
        self.form_input_value_password.move(285,80)


        self.form_url_address_label = QLabel(self.login_tab)
        self.form_url_address_label.setText("Form URL address : ")
        self.form_url_address_label.move(20,120)


        self.form_url_address_line = QLineEdit(self.login_tab)
        self.form_url_address_line.resize(200,18)
        self.form_url_address_line.move(138,120)


        self.form_action_url_label = QLabel(self.login_tab)
        self.form_action_url_label.setText("Form Action URL   : ")
        self.form_action_url_label.move(20,150)


        self.form_action_url_line = QLineEdit(self.login_tab)
        self.form_action_url_line.resize(200,18)
        self.form_action_url_line.move(138,150)

        self.save_button = QPushButton('Save',self.login_tab)
        self.save_button.move(280,180)
        self.save_button.clicked.connect(self.set_login_settings)


        self.dlg.exec_()


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
            'Crawler',
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
