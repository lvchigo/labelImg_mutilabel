from PyQt4.QtGui import *
from PyQt4.QtCore import *

from lib import newIcon, labelValidator

BB = QDialogButtonBox

class LabelDialog(QDialog):

    def __init__(self, text="Enter object label", parent=None, listItem=None):
        super(LabelDialog, self).__init__(parent)
        self.edit = QLineEdit()
        self.edit.setText(text)
        self.edit.setValidator(labelValidator())
        self.edit.editingFinished.connect(self.postProcess)
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        if listItem is not None and len(listItem) > 0:
            self.listWidget = QListWidget(self)
            for item in listItem:
                self.listWidget.addItem(item)

            #add by chigo
            #self.listWidget.itemDoubleClicked.connect(self.listItemClick)
            self.listWidget.itemClicked.connect(self.listItemClick)
            layout.addWidget(self.listWidget)

        self.setLayout(layout)

    #add by chigo
    def __init__(self, text="Enter object label", parent=None, listItem=None, mutilistItem=None):
        super(LabelDialog, self).__init__(parent)
        self.edit = QLineEdit()
        self.edit.setText(text)
        self.edit.setValidator(labelValidator())
        self.edit.editingFinished.connect(self.postProcess)
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        root_len = len(listItem)
        if listItem is not None and root_len > 0:
            self.tableWidget = QTableWidget(self)
            self.tableWidget.setColumnCount(root_len);

            row_max = 0;
            for mutiIndex,mutiItem in enumerate(mutilistItem):
                tmp_row_len = len(mutilistItem[mutiIndex])
                if row_max < tmp_row_len:
                    row_max = tmp_row_len

            self.tableWidget.setRowCount(row_max);
            self.tableWidget.setHorizontalHeaderLabels(listItem)
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) 
            
            for index1,item1 in enumerate(mutilistItem):
                for index2,item2 in enumerate(mutilistItem[index1]):
                    newItem = QTableWidgetItem(item2)
                    self.tableWidget.setItem(index2, index1, newItem)

            self.tableWidget.itemClicked.connect(self.listItemClick)
            self.tableWidget.resizeColumnsToContents() 
            self.tableWidget.resizeRowsToContents() 
            self.tableWidget.setMinimumSize(QSize(1000, 500))
            layout.addWidget(self.tableWidget)  
            
        self.setLayout(layout)

    def validate(self):
        if self.edit.text().trimmed():
            self.accept()

    def postProcess(self):
        self.edit.setText(self.edit.text().trimmed())

    def popUp(self, text='', move=True):
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)
        if move:
            self.move(QCursor.pos())
        return self.edit.text() if self.exec_() else None

    def listItemClick(self, tQListWidgetItem):
        text = tQListWidgetItem.text().trimmed()
        self.edit.setText(text)
        self.validate()

