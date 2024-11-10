from uuid import uuid4

from student_journal.domain.subject import Subject
from student_journal.domain.value_object.subject_id import SubjectId
from unit.teacher.conftest import TEACHER2_ID, TEACHER_ID

SUBJECT_ID = SubjectId(uuid4())
SUBJECT2_ID = SubjectId(uuid4())

SUBJECT = Subject(
    subject_id=SUBJECT_ID,
    title="abracadabra",
    teacher_id=TEACHER_ID,
)

SUBJECT2 = Subject(
    subject_id=SUBJECT2_ID,
    title="abracadabra",
    teacher_id=TEACHER2_ID,
)
