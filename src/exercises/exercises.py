"""Exercises: ORM fundamentals.

Implement the TODO functions. Autograder will test them.
"""

from __future__ import annotations

from typing import Optional

from flask import request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from src.exercises.extensions import db
from src.exercises.models import Student, Grade, Assignment



# ===== BASIC CRUD =====

def create_student(name: str, email: str) -> Student:
    """TODO: Create and commit a Student; handle duplicate email.


    If email is duplicate:
      - rollback
      - raise ValueError("duplicate email")
    """
    student = Student(name=name, email=email)
    db.session.add(student)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("duplicate email")
    return student



def find_student_by_email(email: str) -> Optional[Student]:
    """TODO: Return Student by email or None."""
    return db.session.query(Student).filter(Student.email == email).first()


def add_grade(student_id: int, assignment_id: int, score: int) -> Grade:
    """TODO: Add a Grade for the student+assignment and commit.

    If student doesn't exist: raise LookupError
    If assignment doesn't exist: raise LookupError
    If duplicate grade: raise ValueError("duplicate grade")
    """
    student = db.session.get(Student, student_id)
    if not student:
        raise LookupError(f"Student with id {student_id} not found")

    assignment = db.session.get(Assignment, assignment_id)
    if not assignment:
        raise LookupError(f"Assignment with id {assignment_id} not found")

    grade = Grade(student_id=student_id, assignment_id=assignment_id, score=score)
    db.session.add(grade)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("duplicate grade")

    return grade


def average_percent(student_id: int) -> float:
    """TODO: Return student's average percent across assignments.

    percent per grade = score / assignment.max_points * 100

    If student doesn't exist: raise LookupError
    If student has no grades: return 0.0
    """
    student = db.session.get(Student, student_id)
    if not student:
        raise LookupError(f"Student with id {student_id} not found")

    grades_data = (
        db.session.query(Grade.score, Assignment.max_points)
        .join(Assignment, Grade.assignment_id == Assignment.id)
        .filter(Grade.student_id == student_id)
        .all()
    )

    if not grades_data:
        return 0.0

    total_percent = 0.0
    for score, max_points in grades_data:
        total_percent += (score / max_points) * 100

    return total_percent / len(grades_data)

# ===== QUERYING & FILTERING =====

def get_all_students() -> list[Student]:
    """TODO: Return all students in database, ordered by name."""
    return db.session.query(Student).order_by(Student.name).all()


def get_assignment_by_title(title: str) -> Optional[Assignment]:
    """TODO: Return assignment by title or None."""
    return db.session.query(Assignment).filter(Assignment.title == title).first()

def get_student_grades(student_id: int) -> list[Grade]:
    """TODO: Return all grades for a student, ordered by assignment title.

    If student doesn't exist: raise LookupError
    """
    student = db.session.get(Student, student_id)
    if not student:
        raise LookupError(f"Student with id {student_id} not found")

    return (
        db.session.query(Grade)
        .join(Assignment, Grade.assignment_id == Assignment.id)
        .filter(Grade.student_id == student_id)
        .order_by(Assignment.title)
        .all()
    )


def get_grades_for_assignment(assignment_id: int) -> list[Grade]:
    """TODO: Return all grades for an assignment, ordered by student name.

    If assignment doesn't exist: raise LookupError
    """
    assignment = db.session.get(Assignment, assignment_id)
    if not assignment:
        raise LookupError(f"Assignment with id {assignment_id} not found")

    return (
        db.session.query(Grade)
        .join(Student, Grade.student_id == Student.id)
        .filter(Grade.assignment_id == assignment_id)
        .order_by(Student.name)
        .all()
    )


# ===== AGGREGATION =====

def total_student_grade_count() -> int:
    """TODO: Return total number of grades in database."""
    return db.session.query(func.count(Grade.id)).scalar()

def highest_score_on_assignment(assignment_id: int) -> Optional[int]:
    """TODO: Return the highest score on an assignment, or None if no grades.

    If assignment doesn't exist: raise LookupError
    """
    assignment = db.session.get(Assignment, assignment_id)
    if not assignment:
        raise LookupError(f"Assignment with id {assignment_id} not found")

    highest_score = db.session.query(func.max(Grade.score)).filter(Grade.assignment_id == assignment_id).scalar()
    return highest_score if highest_score is not None else None


def class_average_percent() -> float:
    """TODO: Return average percent across all students and all assignments.

    percent per grade = score / assignment.max_points * 100
    Return average of all these percents.
    If no grades: return 0.0
    """
    grades_data = (
        db.session.query(Grade.score, Assignment.max_points)
        .join(Assignment, Grade.assignment_id == Assignment.id)
        .all()
    )

    if not grades_data:
        return 0.0

    total_percent = 0.0
    for score, max_points in grades_data:
        total_percent += (score / max_points) * 100

    return total_percent / len(grades_data)


def student_grade_count(student_id: int) -> int:
    """TODO: Return number of grades for a student.

    If student doesn't exist: raise LookupError
    """
    student = db.session.get(Student, student_id)
    if not student:
        raise LookupError(f"Student with id {student_id} not found")

    return db.session.query(func.count(Grade.id)).filter(Grade.student_id == student_id).scalar()


# ===== UPDATING & DELETION =====

def update_student_email(student_id: int, new_email: str) -> Student:
    """TODO: Update a student's email and commit.

    If student doesn't exist: raise LookupError
    If new email is duplicate: rollback and raise ValueError("duplicate email")
    Return the updated student.
    """
    student = db.session.get(Student, student_id)
    if not student:
        raise LookupError(f"Student with id {student_id} not found")
    student.email = new_email
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("duplicate email")
    return student


def delete_student(student_id: int) -> None:
    """TODO: Delete a student and all their grades; commit.

    If student doesn't exist: raise LookupError
    """
    student = db.session.get(Student, student_id)
    if not student:
        raise LookupError(f"Student with id {student_id} not found")
    db.session.query(Grade).filter(Grade.student_id == student_id).delete()
    db.session.delete(student)
    db.session.commit()



def delete_grade(grade_id: int) -> None:
    """TODO: Delete a grade by id; commit.

    If grade doesn't exist: raise LookupError
    """
    grade = db.session.get(Grade, grade_id)
    if not grade:
        raise LookupError(f"Grade with id {grade_id} not found")

    db.session.delete(grade)
    db.session.commit()


# ===== FILTERING & FILTERING WITH AGGREGATION =====

def students_with_average_above(threshold: float) -> list[Student]:
    """TODO: Return students whose average percent is above threshold.

    List should be ordered by average percent descending.
    percent per grade = score / assignment.max_points * 100
    """
    grade_percent = (Grade.score / Assignment.max_points) * 100
    avg_percent = func.avg(grade_percent)
    results = (
        db.session.query(Student)
        .join(Grade, Student.id == Grade.student_id)
        .join(Assignment, Grade.assignment_id == Assignment.id)
        .group_by(Student)  # Grouping by the entire Student model object resolves the attribute errors
        .having(avg_percent > threshold)
        .order_by(avg_percent.desc())
        .all()
    )
    return results


def assignments_without_grades() -> list[Assignment]:
    """TODO: Return assignments that have no grades yet, ordered by title."""
    return (
        db.session.query(Assignment)
        .outerjoin(Grade, Grade.assignment_id == Assignment.id)
        .filter(Grade.id == None)
        .order_by(Assignment.title)
        .all()
    )


def top_scorer_on_assignment(assignment_id: int) -> Optional[Student]:
    """TODO: Return the Student with the highest score on an assignment.

    If assignment doesn't exist: raise LookupError
    If no grades on assignment: return None
    If tie (multiple students with same high score): return any one
    """
    assignment = db.session.get(Assignment, assignment_id)
    if not assignment:
        raise LookupError(f"Assignment with id {assignment_id} not found")

    top_grade = (
        db.session.query(Grade)
        .filter(Grade.assignment_id == assignment_id)
        .order_by(Grade.score.desc())
        .first()
    )

    if not top_grade:
        return None

    return db.session.get(Student, top_grade.student_id)


