import sys
from PyQt5 import QtWidgets

class Example(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # create widgets
        graph = QtWidgets.QFrame()
        graph.setFixedHeight(40)
        graph.setFrameShape(QtWidgets.QFrame.Box)
        graph.setStyleSheet("QWidget { background-color: red }" )

        qlist = QtWidgets.QListWidget()
        qlist.setFrameStyle(QtWidgets.QFrame.Raised)
        qlist.addItems(map(str, range(31)))

        # create QHBoxLayout and add QListWidget
        hlay = QtWidgets.QHBoxLayout()
        hlay.addWidget(qlist)
        hlay.addStretch(1)

        # create QVBoxLayout and add QFrame and QHBoxLayout
        vlay = QtWidgets.QVBoxLayout(self)
        vlay.addWidget(graph)
        vlay.addLayout(hlay) 

        self.setStyleSheet("font: 20pt Cambria")
        self.showMaximized()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())