#
# Tools Collector which provides easy access to multiple tools developed
# during different actions.
#
import sys
import struct

from PyQt5.QtCore import pyqtSlot, QStringListModel, QByteArray
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUiType

from tcconfig import TCConfig
from releasescripts.mcgfirmware import *

TOOLS_COLLECTOR_INI_FILE = 'toolscollector.ini'

app = QApplication(sys.argv)
form_class, base_class = loadUiType('mainwindow.ui')


class TCMainWindowImpl(QMainWindow, form_class):
    def __init__(self, *args):
        super(TCMainWindowImpl, self).__init__(*args)
        self.setupUi(self)

        # read ini file
        self.config = TCConfig(TOOLS_COLLECTOR_INI_FILE)

        self.mcg_fw_dir_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_MCG_FW_DIR_HIST))
        self.cbMcgFwDir.setModel(self.mcg_fw_dir_model)

        self.mcg_fw_versions = QStringListModel(self.config.getSectionValues(TCConfig.TCC_MCG_FW_VERS_HIST))
        self.cbMcgFwVersion.setModel(self.mcg_fw_versions)

        self.pack_dir_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_MCG_PACK_DIR_HIST))
        self.cbMcgPackDir.setModel(self.pack_dir_model)

        self.pack_versions_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_MCG_PACK_VERS_HIST))
        self.cbMcgPackVersions.setModel(self.pack_versions_model)

        self.pack_branches_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_PACK_BRNCH_HIST))
        self.cbPackSrcBranchVersion.setModel(self.pack_branches_model)

        self.pack_tags_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_PACK_TAG_HIST))
        self.cbMcgPackTagVersion.setModel(self.pack_tags_model)

        self.inst_srcs_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_INST_SRC_HIST))
        self.cbMcgFwRepoVersion.setModel(self.inst_srcs_model)

        self.inst_dsts_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_INST_DST_HIST))
        self.cbMcgFwInstVersion.setModel(self.inst_dsts_model)

        self.teLog.setFontFamily('Courier New')

        layout = self.config.getSectionFull(TCConfig.TCC_LAYOUT)
        if type(layout) is dict:
            if 'geometry'in layout:
                self.restoreGeometry(QByteArray.fromBase64(layout['geometry']))
            else:
                self.move(layout['PosX'], layout['PosY'])
                self.resize(layout['Width'], layout['Height'])
            if 'state' in layout:
                self.restoreState(QByteArray.fromBase64(layout['state']))
        pass

    @pyqtSlot()
    def on_app_aboutToQuit(self):
        pos = self.pos()
        layout = dict()
        layout['PosX'] = str(pos.x())
        layout['PosY'] = str(pos.y())
        size = self.size()
        layout['Height'] = str(size.height())
        layout['Width'] = str(size.width())

        geometry = str(self.saveGeometry().toBase64())

        layout['geometry'] = str(self.saveGeometry().toBase64())
        layout['state'] = str(self.saveState().toBase64())
        self.config.updateSection(TCConfig.TCC_LAYOUT, layout)
        self.config.saveConfig(TOOLS_COLLECTOR_INI_FILE)
        return True

    @pyqtSlot(bool)
    def on_pbFwDirSel_clicked(self, checked):
        # self.teLog.append("pbFwDirSel clicked")
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        options |= QFileDialog.DontResolveSymlinks
        dir = QFileDialog.getExistingDirectory(self, "Select MCG Firmware Directory", 'c:', options = options)
        selected_dir = str(dir)
        item_list = self.mcg_fw_dir_model.stringList()
        try:
            idx = item_list.index(selected_dir)
            self.cbMcgFwDir.setCurrentIndex(idx)
        except (ValueError):
            self.cbMcgFwDir.insertItem(0, selected_dir) # adds it automatically to the list model too
            self.cbMcgFwDir.setCurrentIndex(0)
            # fetch stringList again as it was udpated in the model through the insert above
            self.config.updateSection(TCConfig.TCC_MCG_FW_DIR_HIST, self.mcg_fw_dir_model.stringList())

    @pyqtSlot(bool)
    def on_pbUpdateMcgFwVersions_clicked(self, checked):
        top_dir = Path(self.cbMcgFwDir.currentText())
        mcgFwVersion = self.cbMcgFwVersion.currentText()
        self.teLog.append("===============================================================================")
        msg = "UpdateMcgFwVersions clicked with parameter = %s" % mcgFwVersion
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------\n")
        if mcgFwVersion in self.mcg_fw_versions.stringList():
            # remove existing item and new added at front
            idx = self.cbMcgFwVersion.currentIndex()
            self.cbMcgFwVersion.removeItem(idx)
        self.cbMcgFwVersion.insertItem(0, mcgFwVersion)
        self.cbMcgFwVersion.setCurrentIndex(0)
        self.config.updateSection(TCConfig.TCC_MCG_FW_VERS_HIST, self.mcg_fw_versions.stringList())
        result, error_msg = update_mcg_fw_versions(top_dir, mcgFwVersion)
        if result:
            self.teLog.append("Mcg Firmware version files updated")
        else:
            self.teLog.append("Failed to update Mcg Firmware version files.")
            self.teLog.append("Error = " + error_msg)

    @pyqtSlot(bool)
    def on_pbPackDirSel_clicked(self, checked):
        self.teLog.append("pbPackDirSel clicked")
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        dir = QFileDialog.getExistingDirectory(self, "Select MCG Pack Directory", "c:", options = options)
        selected_dir = str(dir)
        item_list = self.pack_dir_model.stringList()
        try:
            idx = item_list.index(selected_dir)
            self.cbMcgPackDir.setCurrentIndex(idx)
        except (ValueError):
            self.cbMcgPackDir.insertItem(0, selected_dir) # adds it automatically to the list model too
            self.cbMcgPackDir.setCurrentIndex(0)
            # fetch stringList again as it was udpated in the model through the insert above
            self.config.updateSection(TCConfig.TCC_MCG_PACK_DIR_HIST, self.pack_dir_model.stringList())

    @pyqtSlot(bool)
    def on_pbUpdateMcgPackVersions_clicked(self, checked):
        mcgPackVersion = self.cbMcgPackVersions.currentText()
        self.teLog.append("===============================================================================")
        msg = "UpdateMcgPackVersions clicked with parameter = %s" % mcgPackVersion
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------\n")
        if mcgPackVersion in self.pack_versions_model.stringList():
            # remove existing item and new added at front
            idx = self.cbMcgPackVersions.currentIndex()
            self.cbMcgPackVersions.removeItem(idx)
        self.cbMcgPackVersions.insertItem(0, mcgPackVersion)
        self.cbMcgPackVersions.setCurrentIndex(0)
        self.config.updateSection(TCConfig.TCC_MCG_PACK_VERS_HIST, self.pack_versions_model.stringList())

    @pyqtSlot(bool)
    def on_pbCreateMcgPackTags_clicked(self, checked):
        brach_version = self.cbPackSrcBranchVersion.currentText()
        tag_version = self.cbMcgPackTagVersion.currentText()
        self.teLog.append("===============================================================================")
        msg = "CreateMcgPackTags clicked with packBranch = %s and packTag = %s" % (brach_version, tag_version)
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------\n")
        if brach_version in self.pack_branches_model.stringList():
            # remove existing item and new added at front
            idx = self.cbPackSrcBranchVersion.currentIndex()
            self.cbPackSrcBranchVersion.removeItem(idx)
        self.cbPackSrcBranchVersion.insertItem(0, brach_version)
        self.cbPackSrcBranchVersion.setCurrentIndex(0)
        self.config.updateSection(TCConfig.TCC_PACK_BRNCH_HIST, self.pack_branches_model.stringList())

        if tag_version in self.pack_tags_model.stringList():
            # remove existing item and new added at front
            idx = self.cbMcgPackTagVersion.currentIndex()
            self.cbMcgPackTagVersion.removeItem(idx)
        self.cbMcgPackTagVersion.insertItem(0, tag_version)
        self.cbMcgPackTagVersion.setCurrentIndex(0)
        self.config.updateSection(TCConfig.TCC_PACK_TAG_HIST, self.pack_tags_model.stringList())

    @pyqtSlot(bool)
    def on_pbCopyMcgFwToInstLoc_clicked(self, checked):
        inst_src = self.cbMcgFwRepoVersion.currentText()
        inst_dst = self.cbMcgFwInstVersion.currentText()
        self.teLog.append("===============================================================================")
        msg = "CopyMcgFwToInstLoc clicked with src = %s and dst = %s" % (inst_src, inst_dst)
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------\n")
        if inst_src in self.inst_srcs_model.stringList():
            # remove existing item and new added at front
            idx = self.cbMcgFwRepoVersion.currentIndex()
            self.cbMcgFwRepoVersion.removeItem(idx)
        self.cbMcgFwRepoVersion.insertItem(0, inst_src)
        self.cbMcgFwRepoVersion.setCurrentIndex(0)
        self.config.updateSection(TCConfig.TCC_INST_SRC_HIST, self.inst_srcs_model.stringList())

        if inst_dst in self.inst_dsts_model.stringList():
            # remove existing item and new added at front
            idx = self.cbMcgFwInstVersion.currentIndex()
            self.cbMcgFwInstVersion.removeItem(idx)
        self.cbMcgFwInstVersion.insertItem(0, inst_dst)
        self.cbMcgFwInstVersion.setCurrentIndex(0)
        self.config.updateSection(TCConfig.TCC_INST_DST_HIST, self.inst_dsts_model.stringList())

    @pyqtSlot(bool)
    def on_pbClearLog_clicked(self, checked):
        self.teLog.clear()
        

form = TCMainWindowImpl()
app.aboutToQuit.connect(form.on_app_aboutToQuit)
form.show()
sys.exit(app.exec_())
