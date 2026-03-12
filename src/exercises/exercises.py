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
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return {"error": "name and email are required"}, 400

    student = Student(name=name, email=email)
    db.session.add(student)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {"error": "email must be unique"}, 409

    return {"id": student.id, "name": student.name, "email": student.email}, 201



def find_student_by_email(email: str) -> Optional[Student]:
    """TODO: Return Student by email or None."""
    raise NotImplementedError


def add_grade(student_id: int, assignment_id: int, score: int) -> Grade:
    """TODO: Add a Grade for the student+assignment and commit.

    If student doesn't exist: raise LookupError
    If assignment doesn't exist: raise LookupError
    If duplicate grade: raise ValueError("duplicate grade")
    """
    s = db.session.get(Student, student_id)
    if not s:
        return {"error": "student not found"}, 404

    data = request.get_json() or {}
    score = data.get("score")
    if score is None:
        return {"error": "score is required"}, 400

    g = Grade(score=int(score), student=s)
    db.session.add(g)
    db.session.commit()

    return {"id": g.id, "score": g.score, "student_id": s.id}, 201


def average_percent(student_id: int) -> float:
    """TODO: Return student's average percent across assignments.

    percent per grade = score / assignment.max_points * 100

    If student doesn't exist: raise LookupError
    If student has no grades: return 0.0
    """
    raise NotImplementedError


# ===== QUERYING & FILTERING =====

def get_all_students() -> list[Student]:
    """TODO: Return all students in database, ordered by name."""
    raise NotImplementedError


def get_assignment_by_title(title: str) -> Optional[Assignment]:
    """TODO: Return assignment by title or None."""
    raise NotImplementedError


def get_student_grades(student_id: int) -> list[Grade]:
    """TODO: Return all grades for a student, ordered by assignment title.

    If student doesn't exist: raise LookupError
    """
    raise NotImplementedError


def get_grades_for_assignment(assignment_id: int) -> list[Grade]:
    """TODO: Return all grades for an assignment, ordered by student name.

    If assignment doesn't exist: raise LookupError
    """
    raise NotImplementedError


# ===== AGGREGATION =====

def total_student_grade_count() -> int:
    """TODO: Return total number of grades in database."""
    raise NotImplementedError


def highest_score_on_assignment(assignment_id: int) -> Optional[int]:
    """TODO: Return the highest score on an assignment, or None if no grades.

    If assignment doesn't exist: raise LookupError
    """
    raise NotImplementedError


def class_average_percent() -> float:
    """TODO: Return average percent across all students and all assignments.

    percent per grade = score / assignment.max_points * 100
    Return average of all these percents.
    If no grades: return 0.0
    """
    raise NotImplementedError


def student_grade_count(student_id: int) -> int:
    """TODO: Return number of grades for a student.

    If student doesn't exist: raise LookupError
    """
    raise NotImplementedError


# ===== UPDATING & DELETION =====

def update_student_email(student_id: int, new_email: str) -> Student:
    """TODO: Update a student's email and commit.

    If student doesn't exist: raise LookupError
    If new email is duplicate: rollback and raise ValueError("duplicate email")
    Return the updated student.
    """
    s = db.session.get(Student, student_id)
    if not s:
        return {"error": "not found"}, 404

    data = request.get_json() or {}
    if "name" in data:
        s.name = data["name"]
    if "email" in data:
        s.email = data["email"]

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {"error": "update failed (possibly duplicate email)"}, 409

    return {"id": s.id, "name": s.name, "email": s.email}


def delete_student(student_id: int) -> None:
    """TODO: Delete a student and all their grades; commit.

    If student doesn't exist: raise LookupError
    """
    s = db.session.get(Student, student_id)
    if not s:
        return {"error": "student not found"}, 404

    db.session.delete(s)
    db.session.commit()
    return {}, 204



def delete_grade(grade_id: int) -> None:
    """TODO: Delete a grade by id; commit.

    If grade doesn't exist: raise LookupError
    """
    g = db.session.get(Grade, grade_id)
    if not g:
        return {"error": "grade not found"}, 404

    db.session.delete(g)
    db.session.commit()
    return {}, 204


# ===== FILTERING & FILTERING WITH AGGREGATION =====

def students_with_average_above(threshold: float) -> list[Student]:
    """TODO: Return students whose average percent is above threshold.

    List should be ordered by average percent descending.
    percent per grade = score / assignment.max_points * 100
    """
    raise NotImplementedError


def assignments_without_grades() -> list[Assignment]:
    """TODO: Return assignments that have no grades yet, ordered by title."""
    raise NotImplementedError


def top_scorer_on_assignment(assignment_id: int) -> Optional[Student]:
    """TODO: Return the Student with the highest score on an assignment.

    If assignment doesn't exist: raise LookupError
    If no grades on assignment: return None
    If tie (multiple students with same high score): return any one
    """
    raise NotImplementedError

