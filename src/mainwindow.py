# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(895, 594)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabRelease = QtWidgets.QWidget()
        self.tabRelease.setObjectName("tabRelease")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabRelease)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pbUpdateMcgFwVersions = QtWidgets.QPushButton(self.tabRelease)
        self.pbUpdateMcgFwVersions.setMinimumSize(QtCore.QSize(210, 0))
        self.pbUpdateMcgFwVersions.setCheckable(False)
        self.pbUpdateMcgFwVersions.setObjectName("pbUpdateMcgFwVersions")
        self.horizontalLayout.addWidget(self.pbUpdateMcgFwVersions)
        self.label_4 = QtWidgets.QLabel(self.tabRelease)
        self.label_4.setMinimumSize(QtCore.QSize(130, 0))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.cbMcgFwVersion = QtWidgets.QComboBox(self.tabRelease)
        self.cbMcgFwVersion.setMinimumSize(QtCore.QSize(75, 0))
        self.cbMcgFwVersion.setMaximumSize(QtCore.QSize(150, 16777215))
        self.cbMcgFwVersion.setEditable(True)
        self.cbMcgFwVersion.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.cbMcgFwVersion.setObjectName("cbMcgFwVersion")
        self.horizontalLayout.addWidget(self.cbMcgFwVersion)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pbUpdateMcgPackVersions = QtWidgets.QPushButton(self.tabRelease)
        self.pbUpdateMcgPackVersions.setMinimumSize(QtCore.QSize(210, 0))
        self.pbUpdateMcgPackVersions.setObjectName("pbUpdateMcgPackVersions")
        self.horizontalLayout_2.addWidget(self.pbUpdateMcgPackVersions)
        self.label_5 = QtWidgets.QLabel(self.tabRelease)
        self.label_5.setMinimumSize(QtCore.QSize(130, 0))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.leMcgPackVersions = QtWidgets.QLineEdit(self.tabRelease)
        self.leMcgPackVersions.setMinimumSize(QtCore.QSize(75, 0))
        self.leMcgPackVersions.setMaximumSize(QtCore.QSize(150, 16777215))
        self.leMcgPackVersions.setObjectName("leMcgPackVersions")
        self.horizontalLayout_2.addWidget(self.leMcgPackVersions)
        self.cbPrevPackVersions = QtWidgets.QComboBox(self.tabRelease)
        self.cbPrevPackVersions.setMinimumSize(QtCore.QSize(75, 0))
        self.cbPrevPackVersions.setObjectName("cbPrevPackVersions")
        self.horizontalLayout_2.addWidget(self.cbPrevPackVersions)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pbCreateMcgPackTags = QtWidgets.QPushButton(self.tabRelease)
        self.pbCreateMcgPackTags.setMinimumSize(QtCore.QSize(210, 0))
        self.pbCreateMcgPackTags.setObjectName("pbCreateMcgPackTags")
        self.horizontalLayout_3.addWidget(self.pbCreateMcgPackTags)
        self.label_6 = QtWidgets.QLabel(self.tabRelease)
        self.label_6.setMinimumSize(QtCore.QSize(100, 0))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.lePackSrcBranchVersion = QtWidgets.QLineEdit(self.tabRelease)
        self.lePackSrcBranchVersion.setMinimumSize(QtCore.QSize(75, 0))
        self.lePackSrcBranchVersion.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lePackSrcBranchVersion.setObjectName("lePackSrcBranchVersion")
        self.horizontalLayout_3.addWidget(self.lePackSrcBranchVersion)
        self.comboBox = QtWidgets.QComboBox(self.tabRelease)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_3.addWidget(self.comboBox)
        self.label_7 = QtWidgets.QLabel(self.tabRelease)
        self.label_7.setMinimumSize(QtCore.QSize(120, 0))
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.leMcgPackTagVersion = QtWidgets.QLineEdit(self.tabRelease)
        self.leMcgPackTagVersion.setMinimumSize(QtCore.QSize(75, 0))
        self.leMcgPackTagVersion.setMaximumSize(QtCore.QSize(150, 16777215))
        self.leMcgPackTagVersion.setObjectName("leMcgPackTagVersion")
        self.horizontalLayout_3.addWidget(self.leMcgPackTagVersion)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pbCopyMcgFwToInstLoc = QtWidgets.QPushButton(self.tabRelease)
        self.pbCopyMcgFwToInstLoc.setMinimumSize(QtCore.QSize(210, 0))
        self.pbCopyMcgFwToInstLoc.setObjectName("pbCopyMcgFwToInstLoc")
        self.horizontalLayout_4.addWidget(self.pbCopyMcgFwToInstLoc)
        self.label = QtWidgets.QLabel(self.tabRelease)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.leMcgFwRepoVersion = QtWidgets.QLineEdit(self.tabRelease)
        self.leMcgFwRepoVersion.setMinimumSize(QtCore.QSize(75, 0))
        self.leMcgFwRepoVersion.setMaximumSize(QtCore.QSize(150, 16777215))
        self.leMcgFwRepoVersion.setObjectName("leMcgFwRepoVersion")
        self.horizontalLayout_4.addWidget(self.leMcgFwRepoVersion)
        self.label_2 = QtWidgets.QLabel(self.tabRelease)
        self.label_2.setMinimumSize(QtCore.QSize(120, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.leMcgFwInstVersion = QtWidgets.QLineEdit(self.tabRelease)
        self.leMcgFwInstVersion.setMinimumSize(QtCore.QSize(75, 0))
        self.leMcgFwInstVersion.setMaximumSize(QtCore.QSize(150, 16777215))
        self.leMcgFwInstVersion.setObjectName("leMcgFwInstVersion")
        self.horizontalLayout_4.addWidget(self.leMcgFwInstVersion)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.tabRelease)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.pbClearLog = QtWidgets.QPushButton(self.tabRelease)
        self.pbClearLog.setObjectName("pbClearLog")
        self.horizontalLayout_5.addWidget(self.pbClearLog)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.teLog = QtWidgets.QTextEdit(self.tabRelease)
        self.teLog.setReadOnly(True)
        self.teLog.setObjectName("teLog")
        self.verticalLayout.addWidget(self.teLog)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tabRelease, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout_6.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setEnabled(False)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 895, 26))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tabWidget, self.pbUpdateMcgFwVersions)
        MainWindow.setTabOrder(self.pbUpdateMcgFwVersions, self.pbUpdateMcgPackVersions)
        MainWindow.setTabOrder(self.pbUpdateMcgPackVersions, self.leMcgPackVersions)
        MainWindow.setTabOrder(self.leMcgPackVersions, self.pbCreateMcgPackTags)
        MainWindow.setTabOrder(self.pbCreateMcgPackTags, self.lePackSrcBranchVersion)
        MainWindow.setTabOrder(self.lePackSrcBranchVersion, self.leMcgPackTagVersion)
        MainWindow.setTabOrder(self.leMcgPackTagVersion, self.pbCopyMcgFwToInstLoc)
        MainWindow.setTabOrder(self.pbCopyMcgFwToInstLoc, self.leMcgFwRepoVersion)
        MainWindow.setTabOrder(self.leMcgFwRepoVersion, self.leMcgFwInstVersion)
        MainWindow.setTabOrder(self.leMcgFwInstVersion, self.pbClearLog)
        MainWindow.setTabOrder(self.pbClearLog, self.teLog)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MyToolsCollection"))
        self.pbUpdateMcgFwVersions.setText(_translate("MainWindow", "Update MCG Firmware Versions"))
        self.label_4.setText(_translate("MainWindow", "New MCG Fw Version:"))
        self.pbUpdateMcgPackVersions.setText(_translate("MainWindow", "Update MCG Pack Versions"))
        self.label_5.setText(_translate("MainWindow", "New Version:"))
        self.pbCreateMcgPackTags.setText(_translate("MainWindow", "Create MCG Pack Tags"))
        self.label_6.setText(_translate("MainWindow", "Branch Version:"))
        self.label_7.setText(_translate("MainWindow", "Tag Version (Base):"))
        self.pbCopyMcgFwToInstLoc.setText(_translate("MainWindow", "Copy MCG Firmware To Install Loc"))
        self.label.setText(_translate("MainWindow", "Source Version:"))
        self.label_2.setText(_translate("MainWindow", "Target Version:"))
        self.label_3.setText(_translate("MainWindow", "Logs:"))
        self.pbClearLog.setText(_translate("MainWindow", "Clear Log"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRelease), _translate("MainWindow", "Release Actions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))

