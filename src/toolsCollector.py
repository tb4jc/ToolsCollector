#
# Tools Collector which provides easy access to multiple tools developed
# during different actions.
#
import sys
import ConfigParser

from PyQt5.QtCore import pyqtSlot, QStringListModel
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUiType

app = QApplication(sys.argv)
form_class, base_class = loadUiType('mainwindow.ui')

class TCMainWindowImpl(QMainWindow, form_class):
    def __init__(self, *args):
        super(TCMainWindowImpl, self).__init__(*args)
        self.setupUi(self)
        # read ini file
        self.config = ConfigParser.ConfigParser()
        self.config.optionxform = str
        self.config.read('toolsCollector.ini')
        for section_name in self.config.sections():
            print 'Section:', section_name
            print '  Options:', self.config.options(section_name)
            for name, value in self.config.items(section_name):
                print '  %s = %s' % (name, value)
            print

        self.mcgFwVersions = list()
        for name, value in self.config.items('McgFwVersionHistory'):
            self.mcgFwVersions.append(value)
            self.cbMcgFwVersion.addItem(value)
            # print '  %s = %s' % (name, value)
        # self.cbPrevFwVers.insertItems(-1, self.mcgFwVersions)
        # self.mcgFwVersionsModel = QStringListModel(self.mcgFwVersions, self)
        # self.cbPrevFwVers.setModel(self.mcgFwVersionsModel)

    @pyqtSlot()
    def on_app_aboutToQuit(self):
        optionCounter = 0
        for item in self.mcgFwVersions:
            self.config.set('McgFwVersionHistory', str(optionCounter), item)
            optionCounter += 1
        with open('toolsCollector_s.ini', 'wb') as configfile:
            self.config.write(configfile)

    @pyqtSlot(bool)
    def on_pbUpdateMcgFwVersions_clicked(self, checked):
        mcgFwVersion = self.cbMcgFwVersion.currentText()
        self.teLog.append("===============================================================================")
        msg = "UpdateMcgFwVersions clicked with parameter = %s" % mcgFwVersion
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------\n")
        if mcgFwVersion in self.mcgFwVersions:
            # remove existing item and new added at front
            self.mcgFwVersions.remove(mcgFwVersion)
        self.mcgFwVersions.insert(0, mcgFwVersion)

    @pyqtSlot(bool)
    def on_pbUpdateMcgPackVersions_clicked(self, checked):
        self.teLog.append("===============================================================================")
        msg = "UpdateMcgPackVersions clicked with parameter = %s" % self.leMcgPackVersions.text()
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------\n")

    @pyqtSlot(bool)
    def on_pbCreateMcgPackTags_clicked(self, checked):
        self.teLog.append("===============================================================================")
        msg = "CreateMcgPackTags clicked with packBranch = %s and packTag = %s" %\
              (self.lePackSrcBranchVersion.text(), self.leMcgPackTagVersion.text())
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------\n")

    @pyqtSlot(bool)
    def on_pbCopyMcgFwToInstLoc_clicked(self, checked):
        self.teLog.append("===============================================================================")
        msg = "CopyMcgFwToInstLoc clicked with src = %s and dst = %s" %\
              (self.leMcgFwRepoVersion.text(), self.leMcgFwInstVersion.text())
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------\n")

    @pyqtSlot(bool)
    def on_pbClearLog_clicked(self, checked):
        self.teLog.clear()
        

form = TCMainWindowImpl()
app.aboutToQuit.connect(form.on_app_aboutToQuit)
form.show()
sys.exit(app.exec_())
