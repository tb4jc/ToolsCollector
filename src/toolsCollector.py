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
from releasescripts.mcgconfig import *

TOOLS_COLLECTOR_INI_FILE = 'toolscollector.ini'

app = QApplication(sys.argv)
form_class, base_class = loadUiType('mainwindow.ui')


class TCMainWindowImpl(QMainWindow, form_class):
    def __init__(self, *args):
        super(TCMainWindowImpl, self).__init__(*args)
        self.setupUi(self)

        # read ini file
        self.config = TCConfig(TOOLS_COLLECTOR_INI_FILE)

        self.mcg_fw_versions = QStringListModel(self.config.getSectionValues(TCConfig.TCC_MCG_FW_VERS_HIST))
        self.cbMcgFwVersions.setModel(self.mcg_fw_versions)

        self.mcg_cfg_versions = QStringListModel(self.config.getSectionValues(TCConfig.TCC_MCG_CFG_VERS_HIST))
        self.cbMcgCfgVersions.setModel(self.mcg_cfg_versions)

        self.prodbase_versions = QStringListModel(self.config.getSectionValues(TCConfig.TCC_PRODBASE_VERS_HIST))
        self.cbProdBaseVersions.setModel(self.prodbase_versions)

        self.mcg_fw_dir_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_MCG_FW_DIR_HIST))
        self.cbMcgFwDirs.setModel(self.mcg_fw_dir_model)

        self.mcg_cfg_dir_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_MCG_CFG_DIR_HIST))
        self.cbMcgCfgDirs.setModel(self.mcg_cfg_dir_model)

        self.pack_dir_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_MCG_PACK_DIR_HIST))
        self.cbMcgPackDirs.setModel(self.pack_dir_model)

        self.pack_branches_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_PACK_BRNCH_HIST))
        self.cbPackSrcBranchVersions.setModel(self.pack_branches_model)

        self.pack_tags_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_PACK_TAG_HIST))
        self.cbMcgPackTagVersions.setModel(self.pack_tags_model)

        self.inst_srcs_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_INST_SRC_HIST))
        self.cbMcgFwRepoVersions.setModel(self.inst_srcs_model)

        self.inst_dsts_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_INST_DST_HIST))
        self.cbMcgFwInstVersions.setModel(self.inst_dsts_model)

        self._data_dic = {
            TCConfig.TCC_MCG_FW_DIR_HIST:    {'combox': self.cbMcgFwDirs,             'model': self.mcg_fw_dir_model},
            TCConfig.TCC_MCG_FW_VERS_HIST:   {'combox': self.cbMcgFwVersions,         'model': self.mcg_fw_versions},
            TCConfig.TCC_MCG_CFG_DIR_HIST:   {'combox': self.cbMcgCfgDirs,            'model': self.mcg_cfg_dir_model},
            TCConfig.TCC_MCG_CFG_VERS_HIST:  {'combox': self.cbMcgCfgVersions,        'model': self.mcg_cfg_versions},
            TCConfig.TCC_MCG_PACK_DIR_HIST:  {'combox': self.cbMcgPackDirs,           'model': self.pack_dir_model},
            TCConfig.TCC_PRODBASE_VERS_HIST: {'combox': self.cbProdBaseVersions,      'model': self.prodbase_versions},
            TCConfig.TCC_PACK_BRNCH_HIST:    {'combox': self.cbPackSrcBranchVersions, 'model': self.pack_branches_model},
            TCConfig.TCC_PACK_TAG_HIST:      {'combox': self.cbMcgPackTagVersions,    'model': self.pack_tags_model},
            TCConfig.TCC_INST_SRC_HIST:      {'combox': self.cbMcgFwRepoVersions,     'model': self.inst_srcs_model},
            TCConfig.TCC_INST_DST_HIST:      {'combox': self.cbMcgFwInstVersions,     'model': self.inst_dsts_model}
        }

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


    def update_version_combox(self, id, version):
        combox = self._data_dic[id]['combox']
        model = self._data_dic[id]['model']
        if version in model.stringList():
            # remove existing item and new added at front
            idx = combox.currentIndex()
            combox.removeItem(idx)
        combox.insertItem(0, version)
        combox.setCurrentIndex(0)
        self.config.updateSection(id, model.stringList())


    def update_dir_combox(self, id, path):
        combox = self._data_dic[id]['combox']
        model = self._data_dic[id]['model']
        try:
            idx = model.stringList().index(path)
            combox.setCurrentIndex(idx)
        except (ValueError):
            combox.insertItem(0, path) # adds it automatically to the list model too
            combox.setCurrentIndex(0)
        # fetch stringList again as it was udpated in the model through the insert above
        self.config.updateSection(id, model.stringList())

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
        self.update_dir_combox(TCConfig.TCC_MCG_FW_DIR_HIST, selected_dir)

    @pyqtSlot(bool)
    def on_pbUpdateMcgFwVersions_clicked(self, checked):
        top_dir = Path(self.cbMcgFwDirs.currentText())
        mcgFwVersion = self.cbMcgFwVersions.currentText()
        self.teLog.append("===============================================================================")
        msg = "UpdateMcgFwVersions clicked with parameter = %s" % mcgFwVersion
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------")
        self.update_version_combox(TCConfig.TCC_MCG_FW_VERS_HIST, mcgFwVersion)
        result, error_msg = update_mcg_fw_versions(top_dir, mcgFwVersion)
        if result:
            self.teLog.append("Mcg Firmware version files updated")
        else:
            self.teLog.append("Failed to update Mcg Firmware version files.")
            self.teLog.append("Error = " + error_msg)

    @pyqtSlot(bool)
    def on_pbCfgDirSel_clicked(self, checked):
        # self.teLog.append("pbCfgDirSel clicked")
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        options |= QFileDialog.DontResolveSymlinks
        dir = QFileDialog.getExistingDirectory(self, "Select MCG Config Directory", 'c:', options = options)
        selected_dir = str(dir)
        self.update_dir_combox(TCConfig.TCC_MCG_CFG_DIR_HIST, selected_dir)

    @pyqtSlot(bool)
    def on_pbUpdateMcgMasters_clicked(self, checked):
        top_dir = Path(self.cbMcgCfgDirs.currentText())
        mcgFwVersion = self.cbMcgFwVersions.currentText()
        self.teLog.append("===============================================================================")
        msg = "UpdateMcgMasters clicked with parameter = %s" % mcgFwVersion
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------")
        self.update_version_combox(TCConfig.TCC_MCG_FW_VERS_HIST, mcgFwVersion)
        result, error_msg = update_mcg_master_files(top_dir, mcgFwVersion)
        if result:
            self.teLog.append("Mcg Master files updated")
        else:
            self.teLog.append("Failed to update Mcg Master files.")
            self.teLog.append("Error = " + error_msg)

    @pyqtSlot(bool)
    def on_pbPackDirSel_clicked(self, checked):
        self.teLog.append("pbPackDirSel clicked")
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        dir = QFileDialog.getExistingDirectory(self, "Select MCG Pack Directory", "c:", options = options)
        selected_dir = str(dir)
        self.update_dir_combox(TCConfig.TCC_MCG_PACK_DIR_HIST, selected_dir)

    @pyqtSlot(bool)
    def on_pbUpdateMcgPackVersions_clicked(self, checked):
        mcgFwVersion = self.cbMcgFwVersions.currentText()
        mcgCfgVersion = self.cbMcgCfgVersions.currentText()
        prodBaseVersion = self.cbProdBaseVersions.currentText()
        self.teLog.append("===============================================================================")
        msg = "UpdateMcgPackVersions clicked with parameters:\n    Firmware = %s\n    Config   = %s\n    ProdBase = %s" % \
              (mcgFwVersion, mcgCfgVersion, prodBaseVersion)
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------")
        self.update_version_combox(TCConfig.TCC_MCG_FW_VERS_HIST, mcgFwVersion)
        self.update_version_combox(TCConfig.TCC_MCG_CFG_VERS_HIST, mcgCfgVersion)
        self.update_version_combox(TCConfig.TCC_PRODBASE_VERS_HIST, prodBaseVersion)

    @pyqtSlot(bool)
    def on_pbCreateMcgPackTags_clicked(self, checked):
        branch_version = self.cbPackSrcBranchVersions.currentText()
        tag_version = self.cbMcgPackTagVersions.currentText()
        self.teLog.append("===============================================================================")
        msg = "CreateMcgPackTags clicked with packBranch = %s and packTag = %s" % (branch_version, tag_version)
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------")
        self.update_version_combox(TCConfig.TCC_PACK_BRNCH_HIST, branch_version)
        self.update_version_combox(TCConfig.TCC_PACK_TAG_HIST, tag_version)

    @pyqtSlot(bool)
    def on_pbCopyMcgFwToInstLoc_clicked(self, checked):
        inst_src = self.cbMcgFwRepoVersions.currentText()
        inst_dst = self.cbMcgFwInstVersions.currentText()
        self.teLog.append("===============================================================================")
        msg = "CopyMcgFwToInstLoc clicked with src = %s and dst = %s" % (inst_src, inst_dst)
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------")
        self.update_version_combox(TCConfig.TCC_INST_SRC_HIST, inst_src)
        self.update_version_combox(TCConfig.TCC_INST_DST_HIST, inst_dst)

    @pyqtSlot(bool)
    def on_pbClearLog_clicked(self, checked):
        self.teLog.clear()
        

form = TCMainWindowImpl()
app.aboutToQuit.connect(form.on_app_aboutToQuit)
form.show()
sys.exit(app.exec_())
