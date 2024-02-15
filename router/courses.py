import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session


router = APIRouter(
    tags=["Courses"],
    prefix="/courses"
)


@router.get("/allCourses",
            response_model=list[dict],
            status_code=200)
def allCourses(db: Session = Depends(database.get_db)):

    result = db.query(models.Courses, models.CourseFees, models.CourseTeacher, models.Teacher).join(models.CourseFees, models.Courses.id == models.CourseFees.courseID).join(
        models.CourseTeacher, models.Courses.id == models.CourseTeacher.courseID).join(models.Teacher, models.CourseTeacher.teacherUserName == models.Teacher.userName).all()

    courses_dict = {}
    for course, courseFees, courseTeacher, teacher in result:
        if course.id not in courses_dict:
            courses_dict[course.id] = {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "duration": course.duration,
                "startDate": course.startDate,
                "fees": courseFees.fees,
                "discount": courseFees.discount,
                "discountUpTo": courseFees.discountUpTo,
                "teachers": []
            }

        courses_dict[course.id]["teachers"].append({
            "userName": teacher.userName,
            "name": teacher.name,
            "phone": teacher.phone,
            "batch": teacher.batch,
            "college": teacher.college,
            "university": teacher.university,
            "department": teacher.department,
            "subject": teacher.subject
        })

    courses = list(courses_dict.values())

    courses = sorted(courses, key=lambda x: x["id"])
    return courses


@router.get("/searchCourse",
            response_model=list[dict],
            status_code=200)
def searchCourse(search: str, db: Session = Depends(database.get_db)):
    result = db.query(models.Courses, models.CourseFees, models.CourseTeacher, models.Teacher).join(models.CourseFees, models.Courses.id == models.CourseFees.courseID).join(
        models.CourseTeacher, models.Courses.id == models.CourseTeacher.courseID).join(models.Teacher, models.CourseTeacher.teacherUserName == models.Teacher.userName).filter(models.Courses.name.like(f"%{search}%")).all()

    result += db.query(models.Courses, models.CourseFees, models.CourseTeacher, models.Teacher).join(models.CourseFees, models.Courses.id == models.CourseFees.courseID).join(
        models.CourseTeacher, models.Courses.id == models.CourseTeacher.courseID).join(models.Teacher, models.CourseTeacher.teacherUserName == models.Teacher.userName).filter(models.Courses.description.like(f"%{search}%")).all()

    courses_dict = {}

    for course, courseFees, courseTeacher, teacher in result:
        if course.id not in courses_dict:
            courses_dict[course.id] = {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "duration": course.duration,
                "startDate": course.startDate,
                "fees": courseFees.fees,
                "discount": courseFees.discount,
                "discountUpTo": courseFees.discountUpTo,
                "teachers": []
            }

        courses_dict[course.id]["teachers"].append({
            "userName": teacher.userName,
            "name": teacher.name,
            "phone": teacher.phone,
            "batch": teacher.batch,
            "college": teacher.college,
            "university": teacher.university,
            "department": teacher.department,
            "subject": teacher.subject
        })

    courses = list(courses_dict.values())

    courses = sorted(courses, key=lambda x: x["id"])
    return courses
