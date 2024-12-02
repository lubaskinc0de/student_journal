from student_journal.application.invariants.student import (
    HOME_ADDRESS_MAX_LENGTH,
    MAX_AGE,
    MIN_AGE,
    NAME_MAX_LENGTH,
)
from student_journal.presentation.ui.raw.register_ui import Ui_Register


class RegisterUI(Ui_Register):
    def setupUi(self, *args, **kwargs):
        super().setupUi(*args, **kwargs)
        self.set_invariants()

    def set_invariants(self):
        self.name_input.setMaxLength(NAME_MAX_LENGTH)
        self.age_input.setMinimum(MIN_AGE)
        self.age_input.setValue(5)
        self.age_input.setSpecialValueText("Не выбран")
        self.age_input.setMaximum(MAX_AGE)
        self.address_input.setMaxLength(HOME_ADDRESS_MAX_LENGTH)
