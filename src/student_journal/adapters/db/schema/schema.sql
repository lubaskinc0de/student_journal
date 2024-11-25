CREATE TABLE IF NOT EXISTS "Student" (
	"student_id" TEXT NOT NULL UNIQUE,
	"age" INTEGER,
	"avatar" TEXT,
	"name" VARCHAR NOT NULL,
	"home_address" VARCHAR,
	-- от -14 до 12
	"timezone" INTEGER NOT NULL,
	PRIMARY KEY("student_id")
);

CREATE TABLE IF NOT EXISTS "Teacher" (
	"teacher_id" TEXT NOT NULL UNIQUE,
	"full_name" VARCHAR NOT NULL,
	"avatar" TEXT,
	PRIMARY KEY("teacher_id")
);

CREATE TABLE IF NOT EXISTS "Subject" (
	"subject_id" TEXT NOT NULL UNIQUE,
	"title" VARCHAR NOT NULL,
	"teacher_id" TEXT NOT NULL,
	PRIMARY KEY("subject_id"),
	FOREIGN KEY ("teacher_id") REFERENCES "Teacher"("teacher_id")
	ON UPDATE NO ACTION ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS "Lesson" (
	"lesson_id" TEXT NOT NULL UNIQUE,
	"subject_id" TEXT NOT NULL,
	"at" DATETIME NOT NULL,
	"mark" INTEGER,
	"note" TEXT,
	"room" INTEGER NOT NULL,
	"index_number" INTEGER NOT NULL,
	PRIMARY KEY("lesson_id"),
	FOREIGN KEY ("subject_id") REFERENCES "Subject"("subject_id")
	ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "Hometask" (
	"task_id" TEXT NOT NULL UNIQUE,
	"description" TEXT NOT NULL,
	"is_done" BOOLEAN NOT NULL DEFAULT 0,
	"lesson_id" TEXT NOT NULL,
	PRIMARY KEY("task_id"),
	FOREIGN KEY ("lesson_id") REFERENCES "Lesson"("lesson_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
