from sqlite3 import Cursor

import pytest

from student_journal.application.exceptions.subject import SubjectNotFoundError
from unit.subject.conftest import SUBJECT, SUBJECT2, SUBJECT_ID
from unit.teacher.conftest import TEACHER, TEACHER2

from student_journal.adapters.converter.subject import subject_retort
from student_journal.application.common.subject_gateway import SubjectGateway
from student_journal.application.common.teacher_gateway import TeacherGateway
from student_journal.domain.subject import Subject

READ_SUBJECT_SQL = """
        SELECT
            s.subject_id,
            s.title,
            s.teacher_id,
            COALESCE(AVG(l.mark), 0.0) AS avg_mark
        FROM Subject s
        LEFT JOIN Lesson l ON s.subject_id = l.subject_id
        GROUP BY s.subject_id
        ORDER BY avg_mark DESC
"""


def test_write_subject(
    subject_gateway: SubjectGateway,
    cursor: Cursor,
) -> None:
    subject_gateway.write_subject(SUBJECT)
    db_subject = subject_retort.load(
        dict(cursor.execute(READ_SUBJECT_SQL).fetchone()),
        Subject,
    )

    assert db_subject == SUBJECT


def test_read_subject(
    subject_gateway: SubjectGateway,
    cursor: Cursor,
) -> None:
    subject_gateway.write_subject(SUBJECT)
    db_subject = subject_retort.load(
        dict(cursor.execute(READ_SUBJECT_SQL).fetchone()),
        Subject,
    )

    assert db_subject == subject_gateway.read_subject(SUBJECT_ID)


def test_read_subject_not_exist(
    subject_gateway: SubjectGateway,
) -> None:
    with pytest.raises(SubjectNotFoundError):
        subject_gateway.read_subject(SUBJECT_ID)


def test_read_subjects(
    teacher_gateway: TeacherGateway,
    subject_gateway: SubjectGateway,
    cursor: Cursor,
) -> None:
    teacher_gateway.write_teacher(TEACHER)
    teacher_gateway.write_teacher(TEACHER2)
    subject_gateway.write_subject(SUBJECT)
    subject_gateway.write_subject(SUBJECT2)
    subjects = subject_gateway.read_subjects()

    subjects = [
        Subject(
            subject_id=x.subject_id,
            teacher_id=x.teacher.teacher_id,
            title=x.title,
        )
        for x in subjects
    ]

    subjects_list = [dict(s) for s in cursor.execute(READ_SUBJECT_SQL).fetchall()]
    db_subjects = subject_retort.load(
        subjects_list,
        list[Subject],
    )

    assert db_subjects == subjects


def test_update_subject(
    subject_gateway: SubjectGateway,
    cursor: Cursor,
) -> None:
    subject_gateway.write_subject(SUBJECT)
    updated_subject = Subject(
        subject_id=SUBJECT_ID,
        title="Updated Title",
        teacher_id=SUBJECT.teacher_id,
    )

    subject_gateway.update_subject(updated_subject)
    db_entry = dict(cursor.execute(READ_SUBJECT_SQL).fetchone())

    db_subject = subject_retort.load(
        db_entry,
        Subject,
    )

    assert db_subject == updated_subject


def test_delete_subject(
    subject_gateway: SubjectGateway,
    cursor: Cursor,
) -> None:
    subject_gateway.write_subject(SUBJECT)
    subject_gateway.delete_subject(SUBJECT_ID)

    cursor.execute(READ_SUBJECT_SQL)
    assert cursor.fetchone() is None
