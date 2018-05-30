#
# Tools Collector which provides easy access to multiple tools developed
# during different actions.
#
import sys
from tcconfig import TCConfig

from PyQt5.QtCore import pyqtSlot, QStringListModel
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUiType

TOOLS_COLLECTOR_INI_FILE = 'toolscollector.ini'

app = QApplication(sys.argv)
form_class, base_class = loadUiType('mainwindow.ui')

class TCMainWindowImpl(QMainWindow, form_class):
    def __init__(self, *args):
        super(TCMainWindowImpl, self).__init__(*args)
        self.setupUi(self)

        # read ini file
        self.config = TCConfig(TOOLS_COLLECTOR_INI_FILE)
        self.mcg_fw_dirs = self.config.getSectionValues(TCConfig.TCC_MCG_FW_DIR_HIST)
        self.mcg_fw_versions = self.config.getSectionValues(TCConfig.TCC_MCG_FW_VERS_HIST)
        self.pack_dirs = self.config.getSectionValues(TCConfig.TCC_MCG_PACK_DIR_HIST)
        self.pack_vers = self.config.getSectionValues(TCConfig.TCC_MCG_PACK_VERS_HIST)
        self.pack_branches = self.config.getSectionValues(TCConfig.TCC_PACK_BRNCH_HIST)
        self.pack_tags = self.config.getSectionValues(TCConfig.TCC_PACK_TAG_HIST)
        self.inst_srcs = self.config.getSectionValues(TCConfig.TCC_INST_SRC_HIST)
        self.inst_dsts = self.config.getSectionValues(TCConfig.TCC_INST_DST_HIST)

    @pyqtSlot()
    def on_app_aboutToQuit(self):
        self.config.saveConfig(TOOLS_COLLECTOR_INI_FILE)

    @pyqtSlot(bool)
    def on_pbUpdateMcgFwVersions_clicked(self, checked):
        mcgFwVersion = self.cbMcgFwVersion.currentText()
        self.teLog.append("===============================================================================")
        msg = "UpdateMcgFwVersions clicked with parameter = %s" % mcgFwVersion
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------\n")
        if mcgFwVersion in self.mcg_fw_versions:
            # remove existing item and new added at front
            self.mcg_fw_versions.remove(mcgFwVersion)
        self.mcg_fw_versions.insert(0, mcgFwVersion)
        self.config.updateSection(TCConfig.TCC_MCG_FW_VERS_HIST, self.mcg_fw_versions)

    @pyqtSlot(bool)
    def on_pbUpdateMcgPackVersions_clicked(self, checked):
        mcgPackVersion = self.cbMcgPackVersions.currentText()
        self.teLog.append("===============================================================================")
        msg = "UpdateMcgPackVersions clicked with parameter = %s" % mcgPackVersion
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------\n")
        if mcgPackVersion in self.pack_vers:
            # remove existing item and new added at front
            self.pack_vers.remove(mcgPackVersion)
        self.pack_vers.insert(0, mcgPackVersion)
        self.config.updateSection(TCConfig.TCC_MCG_PACK_VERS_HIST, self.pack_vers)

    @pyqtSlot(bool)
    def on_pbCreateMcgPackTags_clicked(self, checked):
        brach_version = self.cbPackSrcBranchVersion.currentText()
        tag_version = self.cbMcgPackTagVersion.currentText()
        self.teLog.append("===============================================================================")
        msg = "CreateMcgPackTags clicked with packBranch = %s and packTag = %s" % (brach_version, tag_version)
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------\n")
        if brach_version in self.pack_branches:
            # remove existing item and new added at front
            self.pack_branches.remove(brach_version)
        self.pack_branches.insert(0, brach_version)
        self.config.updateSection(TCConfig.TCC_PACK_BRNCH_HIST, self.pack_branches)
        if tag_version in self.pack_tags:
            # remove existing item and new added at front
            self.pack_tags.remove(tag_version)
        self.pack_tags.insert(0, tag_version)
        self.config.updateSection(TCConfig.TCC_PACK_TAG_HIST, self.pack_tags)

    @pyqtSlot(bool)
    def on_pbCopyMcgFwToInstLoc_clicked(self, checked):
        inst_src = self.cbMcgFwRepoVersion.currentText()
        inst_dst = self.cbMcgFwInstVersion.currentText()
        self.teLog.append("===============================================================================")
        msg = "CopyMcgFwToInstLoc clicked with src = %s and dst = %s" % (inst_src, inst_dst)
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------\n")
        if inst_src in self.inst_srcs:
            # remove existing item and new added at front
            self.inst_srcs.remove(inst_src)
        self.inst_srcs.insert(0, inst_src)
        self.config.updateSection(TCConfig.TCC_INST_SRC_HIST, self.inst_srcs)
        if inst_dst in self.inst_dsts:
            # remove existing item and new added at front
            self.inst_dsts.remove(inst_dst)
        self.inst_dsts.insert(0, inst_dst)
        self.config.updateSection(TCConfig.TCC_INST_DST_HIST, self.inst_dsts)

    @pyqtSlot(bool)
    def on_pbClearLog_clicked(self, checked):
        self.teLog.clear()
        

form = TCMainWindowImpl()
app.aboutToQuit.connect(form.on_app_aboutToQuit)
form.show()
sys.exit(app.exec_())
