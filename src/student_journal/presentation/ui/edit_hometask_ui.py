# Form implementation generated from reading ui file 'edit_hometask.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EditHometask(object):
    def setupUi(self, EditHometask):
        EditHometask.setObjectName("EditHometask")
        self.gridLayout = QtWidgets.QGridLayout(EditHometask)
        self.gridLayout.setObjectName("gridLayout")
        self.main_label = QtWidgets.QLabel(parent=EditHometask)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_label.sizePolicy().hasHeightForWidth())
        self.main_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        self.main_label.setFont(font)
        self.main_label.setObjectName("main_label")
        self.gridLayout.addWidget(self.main_label, 0, 0, 1, 1)
        self.submit_btn = QtWidgets.QPushButton(parent=EditHometask)
        self.submit_btn.setObjectName("submit_btn")
        self.gridLayout.addWidget(self.submit_btn, 2, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.lesson = QtWidgets.QComboBox(parent=EditHometask)
        self.lesson.setObjectName("lesson")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lesson)
        self.label = QtWidgets.QLabel(parent=EditHometask)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.is_done = QtWidgets.QCheckBox(parent=EditHometask)
        self.is_done.setText("")
        self.is_done.setObjectName("is_done")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.is_done)
        self.label_2 = QtWidgets.QLabel(parent=EditHometask)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.description = QtWidgets.QTextEdit(parent=EditHometask)
        self.description.setObjectName("description")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.description)
        self.label_3 = QtWidgets.QLabel(parent=EditHometask)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 1)
        self.delete_btn = QtWidgets.QPushButton(parent=EditHometask)
        self.delete_btn.setObjectName("delete_btn")
        self.gridLayout.addWidget(self.delete_btn, 3, 0, 1, 1)

        self.retranslateUi(EditHometask)
        QtCore.QMetaObject.connectSlotsByName(EditHometask)

    def retranslateUi(self, EditHometask):
        _translate = QtCore.QCoreApplication.translate
        EditHometask.setWindowTitle(_translate("EditHometask", "Редактирование ДЗ"))
        self.main_label.setText(_translate("EditHometask", "Редактирование ДЗ"))
        self.submit_btn.setText(_translate("EditHometask", "Сохранить"))
        self.label.setText(_translate("EditHometask", "Выполнил?"))
        self.label_2.setText(_translate("EditHometask", "Урок"))
        self.label_3.setText(_translate("EditHometask", "Описание"))
        self.delete_btn.setText(_translate("EditHometask", "Удалить"))
