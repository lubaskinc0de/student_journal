# Form implementation generated from reading ui file 'edit_lesson.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EditLesson(object):
    def setupUi(self, EditLesson):
        EditLesson.setObjectName("EditLesson")
        EditLesson.resize(512, 704)
        self.gridLayout = QtWidgets.QGridLayout(EditLesson)
        self.gridLayout.setObjectName("gridLayout")
        self.main_label = QtWidgets.QLabel(parent=EditLesson)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_label.sizePolicy().hasHeightForWidth())
        self.main_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.main_label.setFont(font)
        self.main_label.setIndent(-1)
        self.main_label.setObjectName("main_label")
        self.gridLayout.addWidget(self.main_label, 0, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(10, 9, 10, -1)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(parent=EditLesson)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.subject_combo = QtWidgets.QComboBox(parent=EditLesson)
        self.subject_combo.setObjectName("subject_combo")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.subject_combo)
        self.label_4 = QtWidgets.QLabel(parent=EditLesson)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(parent=EditLesson)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.label_6 = QtWidgets.QLabel(parent=EditLesson)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_6)
        self.mark_spinbox = QtWidgets.QSpinBox(parent=EditLesson)
        self.mark_spinbox.setObjectName("mark_spinbox")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.mark_spinbox)
        self.label_7 = QtWidgets.QLabel(parent=EditLesson)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_7)
        self.room_spinbox = QtWidgets.QSpinBox(parent=EditLesson)
        self.room_spinbox.setObjectName("room_spinbox")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.room_spinbox)
        self.label_8 = QtWidgets.QLabel(parent=EditLesson)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_8)
        self.index_number_spinbox = QtWidgets.QSpinBox(parent=EditLesson)
        self.index_number_spinbox.setObjectName("index_number_spinbox")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.FieldRole, self.index_number_spinbox)
        self.refresh = QtWidgets.QPushButton(parent=EditLesson)
        self.refresh.setObjectName("refresh")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.refresh)
        self.note_edit = QtWidgets.QPlainTextEdit(parent=EditLesson)
        self.note_edit.setObjectName("note_edit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.note_edit)
        self.label = QtWidgets.QLabel(parent=EditLesson)
        self.label.setObjectName("label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.time_edit = QtWidgets.QTimeEdit(parent=EditLesson)
        self.time_edit.setObjectName("time_edit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.time_edit)
        self.date_popup = QtWidgets.QPushButton(parent=EditLesson)
        self.date_popup.setObjectName("date_popup")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.date_popup)
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 1)
        self.submit_btn = QtWidgets.QPushButton(parent=EditLesson)
        self.submit_btn.setObjectName("submit_btn")
        self.gridLayout.addWidget(self.submit_btn, 2, 0, 1, 1)
        self.delete_btn = QtWidgets.QPushButton(parent=EditLesson)
        self.delete_btn.setObjectName("delete_btn")
        self.gridLayout.addWidget(self.delete_btn, 4, 0, 1, 1)

        self.retranslateUi(EditLesson)
        QtCore.QMetaObject.connectSlotsByName(EditLesson)

    def retranslateUi(self, EditLesson):
        _translate = QtCore.QCoreApplication.translate
        EditLesson.setWindowTitle(_translate("EditLesson", "Редактирование урока"))
        self.main_label.setText(_translate("EditLesson", "Редактирование урока"))
        self.label_3.setText(_translate("EditLesson", "Предмет"))
        self.label_4.setText(_translate("EditLesson", "Дата урока"))
        self.label_5.setText(_translate("EditLesson", "Записка"))
        self.label_6.setText(_translate("EditLesson", "Оценка"))
        self.label_7.setText(_translate("EditLesson", "Кабинет"))
        self.label_8.setText(_translate("EditLesson", "Номер урока"))
        self.refresh.setText(_translate("EditLesson", "Обновить"))
        self.label.setText(_translate("EditLesson", "Время урока"))
        self.date_popup.setText(_translate("EditLesson", "Выбрать"))
        self.submit_btn.setText(_translate("EditLesson", "Сохранить"))
        self.delete_btn.setText(_translate("EditLesson", "Удалить"))