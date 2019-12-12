class WorkerSignals(QObject):
    
    progress = pyqtSignal(float,str)