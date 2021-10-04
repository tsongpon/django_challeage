from manatal.exceptions.exception import EntityNotExist, BadArgumentException
from manatal.models.models import School


class SchoolService:
    def create_school(self, name, max_student):
        self.validate_school(name, max_student)
        new_school = School(name=name, max_student=max_student)
        new_school.save()
        return new_school

    def list_school(self):
        return School.objects.all()

    def get_school(self, id):
        try:
            return School.objects.get(pk=id)
        except School.DoesNotExist:
            raise EntityNotExist('school id {} does not exists'.format(id))

    def update_school(self, id, name, max_student):
        self.validate_school(name, max_student)
        try:
            school_from_db = School.objects.get(pk=id)
            school_from_db.name = name
            school_from_db.max_student = max_student
            school_from_db.save()
            return school_from_db
        except School.DoesNotExist:
            raise EntityNotExist('school id {} does not exists'.format(id))

    def partial_update(self, id, name, max_student):
        try:
            school_from_db = School.objects.get(pk=id)
            if name is not None:
                school_from_db.name = name
            if max_student is not None:
                if max_student < 0:
                    raise BadArgumentException('max_student must be positive number')
                school_from_db.max_student = max_student
            school_from_db.save()
            return school_from_db
        except School.DoesNotExist:
            raise EntityNotExist('school id {} does not exists'.format(id))

    def delete_school(self, id):
        try:
            School.objects.get(pk=id).delete()
        except School.DoesNotExist:
            raise EntityNotExist('school id {} does not exists'.format(id))

    def validate_school(self, name, max_student):
        if not name or not max_student:
            raise BadArgumentException('name and max_student are required')
        if max_student < 0:
            raise BadArgumentException('max_student must be positive number')
