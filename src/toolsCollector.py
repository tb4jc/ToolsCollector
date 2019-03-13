#
# Tools Collector which provides easy access to multiple tools developed
# during different actions.
#

import pyside_extension
from PySide2.QtCore import Slot, QStringListModel, QByteArray
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog

from releasescripts.copytoinstall import *
from releasescripts.mcgconfig import *
from releasescripts.mcgfirmware import *
from releasescripts.mcgpack import *
from tcconfig import TCConfig

TOOLS_COLLECTOR_INI_FILE = 'toolscollector.ini'

form_class, base_class = pyside_extension.loadUiType('mainwindow.ui')


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

        self.inst_dirs_model = QStringListModel(self.config.getSectionValues(TCConfig.TCC_INST_DIR_HIST))
        self.cbMcgFwInstDirs.setModel(self.inst_dirs_model)

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
            TCConfig.TCC_INST_DST_HIST:      {'combox': self.cbMcgFwInstVersions,     'model': self.inst_dsts_model},
            TCConfig.TCC_INST_DIR_HIST:      {'combox': self.cbMcgFwInstDirs,         'model': self.inst_dirs_model}
        }

        self.teLog.setFontFamily('Courier New')

        layout = self.config.getSectionFull(TCConfig.TCC_LAYOUT)
        if type(layout) is dict:
            if 'geometry'in layout:
                byte_array = QByteArray().append(bytes(layout['geometry'], 'utf-8'))
                self.restoreGeometry(QByteArray.fromBase64(byte_array))
            elif 'PosX' in layout:
                self.move(layout['PosX'], layout['PosY'])
                self.resize(layout['Width'], layout['Height'])
            if 'state' in layout:
                byte_array = QByteArray().append(bytes(layout['state'], 'utf-8'))
                self.restoreState(QByteArray.fromBase64(byte_array))
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
        except ValueError:
            combox.insertItem(0, path)  # adds it automatically to the list model too
            combox.setCurrentIndex(0)
        # fetch stringList again as it was updated in the model through the insert above
        self.config.updateSection(id, model.stringList())


    def on_app_about_to_quit(self):
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

    @Slot(bool)
    def on_pbFwDirSel_clicked(self, checked):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        options |= QFileDialog.DontResolveSymlinks
        selected_dir = QFileDialog.getExistingDirectory(self, "Select MCG Firmware Directory", 'c:', options = options)
        if selected_dir is not None and selected_dir != "":
            self.update_dir_combox(TCConfig.TCC_MCG_FW_DIR_HIST, str(Path(selected_dir)))

    @Slot(bool)
    def on_pbUpdateMcgFwVersions_clicked(self, checked):
        top_dir = Path(self.cbMcgFwDirs.currentText())
        mcg_fw_version = self.cbMcgFwVersions.currentText()
        self.teLog.append("===============================================================================")
        msg = "UpdateMcgFwVersions clicked with parameter = %s" % mcg_fw_version
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------")
        self.update_version_combox(TCConfig.TCC_MCG_FW_VERS_HIST, mcg_fw_version)
        try:
            local_result, local_error_msg = update_mcg_fw_versions(top_dir, mcg_fw_version)
        except:
            local_result = False
            local_error_msg = str(sys.exc_info()[0])
        if local_result:
            self.teLog.append("Mcg Firmware version files updated")
        else:
            self.teLog.append("Failed to update Mcg Firmware version files.")
            self.teLog.append("Error = " + local_error_msg)
        self.teLog.append("-------------------------------------------------------------------------------")

    @Slot(bool)
    def on_pbCfgDirSel_clicked(self, checked):
        # self.teLog.append("pbCfgDirSel clicked")
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        options |= QFileDialog.DontResolveSymlinks
        selected_dir = QFileDialog.getExistingDirectory(self, "Select MCG Config Directory", 'c:', options = options)
        if selected_dir is not None and selected_dir != "":
            self.update_dir_combox(TCConfig.TCC_MCG_CFG_DIR_HIST, str(Path(selected_dir)))

    @Slot(bool)
    def on_pbUpdateMcgMasters_clicked(self, checked):
        top_dir = Path(self.cbMcgCfgDirs.currentText())
        mcg_fw_version = self.cbMcgFwVersions.currentText()
        self.teLog.append("===============================================================================")
        msg = "UpdateMcgMasters clicked with parameter = %s" % mcg_fw_version
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------")
        self.update_version_combox(TCConfig.TCC_MCG_FW_VERS_HIST, mcg_fw_version)
        try:
            local_result, local_err_msg = update_mcg_master_files(str(top_dir), mcg_fw_version)
        except:
            local_result = False
            local_err_msg = sys.exc_info()[0]
        if local_result:
            self.teLog.append("Mcg Master files updated")
        else:
            self.teLog.append("Failed to update Mcg Master files.")
            self.teLog.append("Error = " + local_err_msg)
        self.teLog.append("-------------------------------------------------------------------------------")

    @Slot(bool)
    def on_pbPackDirSel_clicked(self, checked):
        self.teLog.append("pbPackDirSel clicked")
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        selected_dir = QFileDialog.getExistingDirectory(self, "Select MCG Pack Directory", "c:", options = options)
        if selected_dir is not None and selected_dir != "":
            self.update_dir_combox(TCConfig.TCC_MCG_PACK_DIR_HIST, str(Path(selected_dir)))

    @Slot(bool)
    def on_pbUpdateMcgPackVersions_clicked(self, checked):
        mcg_fw_version = self.cbMcgFwVersions.currentText()
        mcg_cfg_version = self.cbMcgCfgVersions.currentText()
        prod_base_version = self.cbProdBaseVersions.currentText()
        pack_dir = self.cbMcgPackDirs.currentText()
        self.teLog.append("===============================================================================")
        msg = "UpdateMcgPackVersions clicked with parameters:\n    Firmware = %s\n    Config   = %s\n    ProdBase = %s" % \
              (mcg_fw_version, mcg_cfg_version, prod_base_version)
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------")
        self.update_version_combox(TCConfig.TCC_MCG_FW_VERS_HIST, mcg_fw_version)
        self.update_version_combox(TCConfig.TCC_MCG_CFG_VERS_HIST, mcg_cfg_version)
        self.update_version_combox(TCConfig.TCC_PRODBASE_VERS_HIST, prod_base_version)
        local_version_dic = {'fw': mcg_fw_version, 'cfg': mcg_cfg_version, 'prod_base': prod_base_version}
        local_result, local_err_msg = update_pack_files(pack_dir, local_version_dic)
        if local_result:
            self.teLog.append("Update Pack Files succeeded")
        else:
            self.teLog.append("Update Pack Files failed with error %d" % local_result)
            self.teLog.append(local_err_msg)
        self.teLog.append("-------------------------------------------------------------------------------")

    @Slot(bool)
    def on_pbCreateMcgPackTags_clicked(self, checked):
        branch_version = self.cbPackSrcBranchVersions.currentText()
        tag_version = self.cbMcgPackTagVersions.currentText()
        self.teLog.append("===============================================================================")
        msg = "CreateMcgPackTags clicked with packBranch = %s and packTag = %s" % (branch_version, tag_version)
        self.teLog.append(msg)
        self.teLog.append("-------------------------------------------------------------------------------")
        self.update_version_combox(TCConfig.TCC_PACK_BRNCH_HIST, branch_version)
        self.update_version_combox(TCConfig.TCC_PACK_TAG_HIST, tag_version)
        try:
            local_result, local_err_msg = create_pack_tags_from_branch(str(branch_version), str(tag_version))
        except:
            local_result = 1
            error_msg = sys.exc_info()[0]
        if local_result == 0:
            self.teLog.append("Creating MCG Pack Tags succeeded:")
            self.teLog.append(local_err_msg)
        else:
            self.teLog.append("Creating MCG Pack Tags failed with error %d" % local_result)
            self.teLog.append(local_err_msg)
        self.teLog.append("-------------------------------------------------------------------------------")

    @Slot(bool)
    def on_pbInstLocSel_clicked(self, checked):
        # self.teLog.append("pbInstLocSel clicked")
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        selected_dir = QFileDialog.getExistingDirectory(self, "Select MCG FW Install Directory", "c:", options=options)
        if selected_dir is not None and selected_dir != "":
            self.update_dir_combox(TCConfig.TCC_INST_DIR_HIST, str(Path(selected_dir)))

    @Slot(bool)
    def on_pbCopyMcgFwToInstLoc_clicked(self, checked):
        inst_src = self.cbMcgFwRepoVersions.currentText()
        inst_dst = self.cbMcgFwInstVersions.currentText()
        str_current_mcg_fw_inst_dir = self.cbMcgFwInstDirs.currentText()
        top_dir = ""
        if str_current_mcg_fw_inst_dir != "":
            top_dir = str(Path(str_current_mcg_fw_inst_dir)) # create windows path
            top_dir = str_current_mcg_fw_inst_dir
        self.teLog.append("===============================================================================")
        msg = "CopyMcgFwToInstLoc clicked with src = %s and dst = %s" % (inst_src, inst_dst)
        self.teLog.append(msg)
        self.update_version_combox(TCConfig.TCC_INST_SRC_HIST, inst_src)
        self.update_version_combox(TCConfig.TCC_INST_DST_HIST, inst_dst)
        self.update_dir_combox(TCConfig.TCC_INST_DIR_HIST, top_dir)
        try:
            local_result, local_err_msg = copy_fw_to_install_dir(inst_src, inst_dst, top_dir)
        except:
            local_result = 1
            error_msg = sys.exc_info()[0]
        if local_result == 0:
            self.teLog.append("Copying MCG Fw succeeded:")
            self.teLog.append(local_err_msg)
        else:
            self.teLog.append("Copying MCG Fw failed with error %d" % local_result)
            self.teLog.append(local_err_msg)
        self.teLog.append("-------------------------------------------------------------------------------")

    @Slot(bool)
    def on_pbClearLog_clicked(self, checked):
        self.teLog.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = TCMainWindowImpl()
    app.aboutToQuit.connect(form.on_app_about_to_quit)
    form.show()
    sys.exit(app.exec_())
