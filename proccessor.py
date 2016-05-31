import sys
from PyQt4 import QtCore, QtGui, uic
import unicodecsv
import csv


qtCreatorFile = "processing.ui" # Enter file here.


Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        self.setupUi(self)
        self.setWindowTitle('AINA FEATURE SELECTION')
        self.setWindowIcon(QtGui.QIcon('C:/Users/DJAN DENNIS MINTAH/Desktop/work/ui/ico.png'))
        self.directory=""
        self.vbox=QtGui.QVBoxLayout()
        self.checks=[]
        self.selected=[]
        self.widget=QtGui.QWidget()
        self.rows=[]
        self.fields=[]
        self.inputbrowser.clicked.connect(self.getFile)
        self.outputbrowser.clicked.connect(self.getFolder)
        self.convert.clicked.connect(self.writeRows)

    def clearLayout(self,layout):
    	while layout.count()>0:

    		item=layout.takeAt(0)
    		if not item:
    			continue
    		w=item.widget()
    		if w:
    			w.deleteLater()

    def reset(self):
    	self.row=[]
    	self.fields=[]
    	self.rows=[]
    	self.selected=[]
    	self.checks=[]
    	



    def getFile(self):

        self.reset()

        filepath=QtGui.QFileDialog.getOpenFileName(self,'Single File','~/Desktop/','*.csv')
        self.input.setText(filepath)
        
        with open(filepath,'rb') as f:
            reader=unicodecsv.DictReader(f)

            for row in reader:
                self.rows.append(row)

                for k, v in row.items():
                	if k not in self.fields:
                		self.fields.append(k)
        
        self.des.setText("Dataset contains %d rows and %d features" %(len(self.rows),len(self.fields)))
        self.getFeatures()
        



    def getFeatures(self):
    	#self.scrol=QtGui.QScrollArea()

    	self.clearLayout(self.vbox)

    	for i in self.fields:
    		c=QtGui.QCheckBox("%s"%i)
    		c.setChecked(True)

    		self.vbox.addWidget(c)
    		self.checks.append(c)

    	self.widget.setLayout(self.vbox)
    	self.scrol.setWidget(self.widget)




    def getSelected(self):

    	for row in self.checks:
    		if row.isChecked():
    			self.selected.append(row.text())

    	#print(self.selected)

    def getFolder(self):

        self.directory=QtGui.QFileDialog.getExistingDirectory(self,"Open Directory",'~/Destop/')
        self.output.setText(self.directory)


    def writeRows(self):
        self.progress.setValue(0)
        self.getSelected()

        self.progress.setValue(5)

        filename=self.outName.toPlainText()
        outfile=str(self.directory)+"/"+str(filename)+".csv"

        writers =unicodecsv.writer(open(outfile,'wb'),  delimiter=",")

        writers.writerow(self.selected)
        self.progress.setValue(20)
        
        for result in self.rows:
            row=[]
            i=20
            for field in self.selected:
                if field in result.keys():
                    row.append(result[field])
                else:
                    row.append("")
                self.progress.setValue(i+0.5)
            writers.writerow(row)
        self.progress.setValue(100)










            



        
       
     
        
        
    
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
