# import string
# import pytest

# from tests.unit.mock import MockedTeacherGateway, MockedTransactionManager
# from tests.unit.teacher.conftest import TEACHER, TEAHER_ID
# from student_journal.application.invariants.teacher import FULL_NAME_MAX_LENGTH
# from student_journal.application.exceptions.base import ApplicationError
# from student_journal.application.exceptions.teacher import (
#     TeacherAlreadyExistsError,
#     TeacherDoesNotExistError,
#     TeacherFullNameError,
# )
# from student_journal.application.teacher import (
#     CreateTeacher,
#     NewTeacher,
#     ReadTeacher,
#     ReadTeachers,
#     UpdatedTeacher,
#     UpdateTeacher,
#     DeleteTeacher
#     )


# BAD_INVARIANTS = (
#     [
#         (MIN_AGE - 1, "Ilya", None, None, StudentAgeError, 0),
#         (MAX_AGE, "Ilya", None, None, StudentAgeError, 0),
#         (14, (NAME_MAX_LENGTH + 1) * "a", None, None, StudentNameError, 0),
#         (14, (NAME_MIN_LENGTH - 1) * "a", None, None, StudentNameError, 0),
#         (
#             14,
#             "Ilya",
#             (HOME_ADDRESS_MAX_LENGTH + 1) * "a",
#             None,
#             StudentHomeAddressError,
#             0,
#         ),
#         (14, "Ilya", None, None, StudentTimezoneError, 28),
#         (14, "Ilya", None, string.ascii_letters, StudentAvatarNotExistsError, 0),
#     ],
# )


# def test_create_student(
#     create_student: CreateStudent,
#     transaction_manager: MockedTransactionManager,
#     student_gateway: MockedStudentGateway,
# ) -> None:
#     data = NewStudent(
#         age=14,
#         avatar=None,
#         name="Ilya",
#         home_address=None,
#     )

#     create_student.execute(data)

#     assert transaction_manager.is_begin
#     assert transaction_manager.is_commited
#     assert student_gateway.is_wrote


# @pytest.mark.parametrize(
#     ("age", "name", "home_address", "avatar", "exc_class", "timezone"),
#     *BAD_INVARIANTS,
# )
# def test_create_student_bad_invariants(
#     create_student: CreateStudent,
#     age: int,
#     name: str,
#     home_address: str | None,
#     avatar: str | None,
#     exc_class: type[ApplicationError],
#     timezone: int,
# ) -> None:
#     data = NewStudent(
#         age=age,
#         avatar=avatar,
#         name=name,
#         home_address=home_address,
#         timezone=timezone,
#     )

#     with pytest.raises(exc_class):
#         create_student.execute(data)


# def test_read_student(
#     read_student: ReadStudent,
#     student_gateway: MockedStudentGateway,
# ) -> None:
#     student_gateway.write_student(STUDENT)
#     student = read_student.execute(0.5)

#     assert student.student_id == STUDENT_ID
#     assert student.student_overall_avg_mark == student_gateway.AVG_MARK


# def test_update_student(
#     update_student: UpdateStudent,
#     student_gateway: MockedStudentGateway,
#     transaction_manager: MockedTransactionManager,
# ) -> None:
#     student_gateway.write_student(STUDENT)

#     updated_id = update_student.execute(
#         UpdatedStudent(
#             age=STUDENT.age + 1,
#             avatar=STUDENT.avatar,
#             name=STUDENT.name,
#             home_address=STUDENT.home_address,
#         ),
#     )

#     assert student_gateway.is_updated
#     assert transaction_manager.is_begin
#     assert transaction_manager.is_commited
#     assert updated_id == STUDENT_ID


# @pytest.mark.parametrize(
#     ("age", "name", "home_address", "avatar", "exc_class", "timezone"),
#     *BAD_INVARIANTS,
# )
# def test_update_student_bad_invariants(
#     student_gateway: MockedStudentGateway,
#     update_student: UpdateStudent,
#     age: int,
#     name: str,
#     home_address: str | None,
#     avatar: str | None,
#     exc_class: type[ApplicationError],
#     timezone: int,
# ) -> None:
#     student_gateway.write_student(STUDENT)

#     with pytest.raises(exc_class):
#         update_student.execute(
#             UpdatedStudent(
#                 age=age,
#                 avatar=avatar,
#                 name=name,
#                 home_address=home_address,
#                 timezone=timezone,
#             ),
#         )
