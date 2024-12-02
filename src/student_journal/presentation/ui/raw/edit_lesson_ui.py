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
        EditLesson.resize(550, 537)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EditLesson.sizePolicy().hasHeightForWidth())
        EditLesson.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(EditLesson)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.gridLayout.setObjectName("gridLayout")
        self.submit_btn = QtWidgets.QPushButton(parent=EditLesson)
        self.submit_btn.setObjectName("submit_btn")
        self.gridLayout.addWidget(self.submit_btn, 2, 0, 1, 1)
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
        self.horizontalWidget = QtWidgets.QWidget(parent=EditLesson)
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(10, 9, 10, -1)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(parent=self.horizontalWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.subject_combo = QtWidgets.QComboBox(parent=self.horizontalWidget)
        self.subject_combo.setObjectName("subject_combo")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.subject_combo)
        self.refresh = QtWidgets.QPushButton(parent=self.horizontalWidget)
        self.refresh.setObjectName("refresh")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.refresh)
        self.label_4 = QtWidgets.QLabel(parent=self.horizontalWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.date_popup = QtWidgets.QPushButton(parent=self.horizontalWidget)
        self.date_popup.setObjectName("date_popup")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.date_popup)
        self.label = QtWidgets.QLabel(parent=self.horizontalWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.time_edit = QtWidgets.QTimeEdit(parent=self.horizontalWidget)
        self.time_edit.setObjectName("time_edit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.time_edit)
        self.label_2 = QtWidgets.QLabel(parent=self.horizontalWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.datetime_preview = QtWidgets.QDateTimeEdit(parent=self.horizontalWidget)
        self.datetime_preview.setReadOnly(True)
        self.datetime_preview.setSpecialValueText("")
        self.datetime_preview.setObjectName("datetime_preview")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.datetime_preview)
        self.label_5 = QtWidgets.QLabel(parent=self.horizontalWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.note_edit = QtWidgets.QPlainTextEdit(parent=self.horizontalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.note_edit.sizePolicy().hasHeightForWidth())
        self.note_edit.setSizePolicy(sizePolicy)
        self.note_edit.setMaximumSize(QtCore.QSize(16777215, 70))
        self.note_edit.setObjectName("note_edit")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.note_edit)
        self.label_6 = QtWidgets.QLabel(parent=self.horizontalWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_6)
        self.mark_spinbox = QtWidgets.QSpinBox(parent=self.horizontalWidget)
        self.mark_spinbox.setObjectName("mark_spinbox")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.FieldRole, self.mark_spinbox)
        self.label_7 = QtWidgets.QLabel(parent=self.horizontalWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_7)
        self.room_spinbox = QtWidgets.QSpinBox(parent=self.horizontalWidget)
        self.room_spinbox.setObjectName("room_spinbox")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.ItemRole.FieldRole, self.room_spinbox)
        self.label_8 = QtWidgets.QLabel(parent=self.horizontalWidget)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_8)
        self.add_hometask = QtWidgets.QPushButton(parent=self.horizontalWidget)
        self.add_hometask.setObjectName("add_hometask")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.ItemRole.FieldRole, self.add_hometask)
        self.horizontalLayout.addLayout(self.formLayout)
        self.gridLayout.addWidget(self.horizontalWidget, 1, 0, 1, 1)
        self.delete_btn = QtWidgets.QPushButton(parent=EditLesson)
        self.delete_btn.setObjectName("delete_btn")
        self.gridLayout.addWidget(self.delete_btn, 3, 0, 1, 1)

        self.retranslateUi(EditLesson)
        QtCore.QMetaObject.connectSlotsByName(EditLesson)

    def retranslateUi(self, EditLesson):
        _translate = QtCore.QCoreApplication.translate
        EditLesson.setWindowTitle(_translate("EditLesson", "Редактирование урока"))
        self.submit_btn.setText(_translate("EditLesson", "Сохранить"))
        self.main_label.setText(_translate("EditLesson", "Редактирование урока"))
        self.label_3.setText(_translate("EditLesson", "Предмет"))
        self.refresh.setText(_translate("EditLesson", "Обновить"))
        self.label_4.setText(_translate("EditLesson", "Дата урока"))
        self.date_popup.setText(_translate("EditLesson", "Выбрать"))
        self.label.setText(_translate("EditLesson", "Время урока"))
        self.label_2.setText(_translate("EditLesson", "Выбранная дата и время"))
        self.label_5.setText(_translate("EditLesson", "Записка"))
        self.label_6.setText(_translate("EditLesson", "Оценка"))
        self.label_7.setText(_translate("EditLesson", "Кабинет"))
        self.label_8.setText(_translate("EditLesson", "Домашнее задание"))
        self.add_hometask.setText(_translate("EditLesson", "Добавить"))
        self.delete_btn.setText(_translate("EditLesson", "Удалить урок"))