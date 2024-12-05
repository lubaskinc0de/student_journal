import datetime
import random
from dataclasses import dataclass
from datetime import date, timedelta

from faker import Faker

from student_journal.application.hometask.create_home_task import (
    CreateHomeTask,
    NewHomeTask,
)
from student_journal.application.lesson.create_lesson import CreateLesson, NewLesson
from student_journal.application.student.create_student import CreateStudent, NewStudent
from student_journal.application.student.read_student import ReadStudent
from student_journal.application.subject.create_subject import CreateSubject, NewSubject
from student_journal.application.teacher import CreateTeacher, NewTeacher
from student_journal.domain.value_object.student_id import StudentId

fake = Faker(locale="ru_RU")

SUBJECTS = [
    "Математика",
    "Физика",
    "Информатика",
    "Химия",
    "Физкультура",
    "История",
    "Обществознание",
    "Биология",
    "Английский язык",
    "Русский язык",
]


@dataclass(slots=True, frozen=True)
class TestDataLoader:
    create_student: CreateStudent
    create_teacher: CreateTeacher
    create_subject: CreateSubject
    read_student: ReadStudent
    create_lesson: CreateLesson
    create_home_task: CreateHomeTask

    def insert_student(self) -> StudentId:
        student_name = fake.name()
        student_address = fake.address()
        student_age = fake.random_int(min=14, max=18)
        student_id = self.create_student.execute(
            NewStudent(
                age=student_age,
                name=student_name,
                home_address=student_address,
                avatar=None,
            ),
        )
        student = self.read_student.execute(student_id)
        return student.student_id

    def insert_data(self, student_id: StudentId) -> None:
        teacher_names = [fake.name() for _ in range(10)]
        teachers = []
        student = self.read_student.execute(student_id)

        for name in teacher_names:
            teacher = self.create_teacher.execute(
                NewTeacher(
                    full_name=name,
                    avatar=None,
                ),
            )
            teachers.append(teacher)

        subjects = []
        for teacher_id, subject in zip(teachers, SUBJECTS, strict=True):
            new_subject = self.create_subject.execute(
                NewSubject(
                    teacher_id=teacher_id,
                    title=subject,
                ),
            )
            subjects.append(new_subject)

        da_te = date.today()  # noqa: DTZ011
        week_start = da_te - timedelta(days=da_te.weekday())
        week_end = week_start + timedelta(days=6)
        week = [
            week_start + datetime.timedelta(days=x)
            for x in range((week_end - week_start).days)
        ]

        for da_te in week:
            for hour in range(8, 14):
                time = datetime.time(hour=hour)
                lesson_subject = random.choice(subjects)  # noqa: S311
                at = datetime.datetime.combine(
                    da_te,
                    time,
                    tzinfo=student.time_zone,
                )
                lesson_id = self.create_lesson.execute(
                    NewLesson(
                        subject_id=lesson_subject,
                        at=at,
                        mark=random.randint(2, 5),  # noqa: S311
                        note=fake.text(),
                        room=random.randint(1000, 4000),  # noqa: S311
                    ),
                )

                if random.random() > 0.5:  # noqa: PLR2004, S311
                    self.create_home_task.execute(
                        NewHomeTask(
                            lesson_id=lesson_id,
                            description="Домашнее задание!",
                            is_done=random.choice([True, False]),  # noqa: S311
                        ),
                    )
