# Form implementation generated from reading ui file 'edit_teacher.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EditTeacher(object):
    def setupUi(self, EditTeacher):
        EditTeacher.setObjectName("EditTeacher")
        EditTeacher.setWindowModality(QtCore.Qt.WindowModality.WindowModal)

        self.gridLayout = QtWidgets.QGridLayout(EditTeacher)
        self.gridLayout.setObjectName("gridLayout")
        self.submit_btn = QtWidgets.QPushButton(parent=EditTeacher)
        self.submit_btn.setObjectName("submit_btn")
        self.gridLayout.addWidget(self.submit_btn, 2, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(0, 10, 10, -1)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(parent=EditTeacher)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.full_name_input = QtWidgets.QLineEdit(parent=EditTeacher)
        self.full_name_input.setObjectName("full_name_input")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.full_name_input)
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 1)
        self.main_label = QtWidgets.QLabel(parent=EditTeacher)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_label.sizePolicy().hasHeightForWidth())
        self.main_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.main_label.setFont(font)
        self.main_label.setObjectName("main_label")
        self.gridLayout.addWidget(self.main_label, 0, 0, 1, 1)
        self.delete_btn = QtWidgets.QPushButton(parent=EditTeacher)
        self.delete_btn.setEnabled(True)
        self.delete_btn.setCheckable(False)
        self.delete_btn.setObjectName("delete_btn")
        self.gridLayout.addWidget(self.delete_btn, 3, 0, 1, 1)

        self.retranslateUi(EditTeacher)
        QtCore.QMetaObject.connectSlotsByName(EditTeacher)

    def retranslateUi(self, EditTeacher):
        _translate = QtCore.QCoreApplication.translate
        EditTeacher.setWindowTitle(_translate("EditTeacher", "Редактирование учителя"))
        self.submit_btn.setText(_translate("EditTeacher", "Сохранить"))
        self.label.setText(_translate("EditTeacher", "Полное имя"))
        self.main_label.setText(_translate("EditTeacher", "Редактирование учителя"))
        self.delete_btn.setText(_translate("EditTeacher", "Удалить"))
