import uuid

from manatal.exceptions.exception import SchoolCapacityException, EntityNotExist, BadArgumentException, \
    TargetSchoolNotExistException
from manatal.models.models import Student, School


class StudentService:
    def create_student(self, first_name, last_name, school_id):
        self.validate_student(first_name=first_name, last_name=last_name, school_id=school_id)
        if self.is_school_full(school_id):
            raise SchoolCapacityException('maximum number of student reached')
        generated_student_id = str(uuid.uuid4())
        new_student = Student(student_id=generated_student_id, first_name=first_name, last_name=last_name, school_id=school_id)
        new_student.save()
        return new_student

    def list_student(self):
        return Student.objects.all()

    def get_student(self, id):
        try:
            return Student.objects.get(pk=id)
        except Student.DoesNotExist:
            raise EntityNotExist('student id {} does not exists'.format(id))

    def update_student(self, id, first_name, last_name, school_id):
        self.validate_student(first_name, last_name, school_id)
        try:
            student_from_db = Student.objects.get(pk=id)
            student_from_db.first_name = first_name
            student_from_db.last_name = last_name
            student_from_db.school_id = school_id
            student_from_db.save()
            return student_from_db
        except Student.DoesNotExist:
            raise EntityNotExist('student id {} does not exists'.format(id))

    def partial_update(self, id, first_name, last_name, school_id):
        try:
            student_from_db = Student.objects.get(pk=id)
            if first_name:
                student_from_db.first_name = first_name
            if last_name:
                student_from_db.last_name = last_name
            if school_id:
                student_from_db.student_id = school_id

            student_from_db.save()
            return student_from_db
        except Student.DoesNotExist:
            raise EntityNotExist('student id {} does not exists'.format(id))

    def delete_student(self, id):
        try:
            Student.objects.get(pk=id).delete()
        except Student.DoesNotExist:
            raise EntityNotExist('student id {} does not exists'.format(id))

    def validate_student(self, first_name, last_name, school_id):
        if not first_name or not last_name or not school_id:
            raise BadArgumentException('first_name, last_name and school are required')
        try:
            School.objects.get(pk=school_id)
        except School.DoesNotExist:
            raise TargetSchoolNotExistException('assigning school id {} does not exists'.format(school_id))

    def is_school_full(self, school_id):
        school = School.objects.get(pk=school_id)
        students_in_school = Student.objects.filter(school=school_id)
        return len(students_in_school) >= school.max_student
