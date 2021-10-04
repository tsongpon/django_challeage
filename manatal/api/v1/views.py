from rest_framework import viewsets, status
from rest_framework.response import Response

from manatal.api.v1.serializers import SchoolSerializer, StudentSerializer
from manatal.exceptions.exception import SchoolCapacityException, EntityNotExist, BadArgumentException, \
    TargetSchoolNotExistException
from manatal.services.school_service import SchoolService
from manatal.services.student_service import StudentService


class SchoolViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.school_service = SchoolService()

    def get_queryset(self):
        return self.school_service.list_school()

    def create(self, request, **kwargs):
        try:
            created = self.school_service.create_school(name=request.data.get('name', None),
                                                        max_student=request.data.get('max_student', None))
            serializer = SchoolSerializer(created)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        except BadArgumentException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': str(e)})

    def retrieve(self, request, pk=None, **kwargs):
        try:
            school = self.school_service.get_school(pk)
            serializer = SchoolSerializer(school)
            return Response(serializer.data)
        except EntityNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': str(e)})

    def update(self, request, pk=None, **kwargs):
        try:
            updated = self.school_service.update_school(id=pk, name=request.data.get('name', None),
                                                        max_student=request.data.get('max_student', None))
            serializer = SchoolSerializer(updated)
            return Response(serializer.data)
        except EntityNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': str(e)})
        except BadArgumentException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': str(e)})

    def partial_update(self, request, pk=None, **kwargs):
        try:
            updated = self.school_service.partial_update(id=pk, name=request.data.get('name', None),
                                                         max_student=request.data.get('max_student', None))
            serializer = SchoolSerializer(updated)
            return Response(serializer.data)
        except EntityNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': str(e)})
        except BadArgumentException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': str(e)})

    def destroy(self, request, pk=None, **kwargs):
        try:
            self.school_service.delete_school(id=pk)
            return Response(status=status.HTTP_200_OK)
        except EntityNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': str(e)})


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.student_service = StudentService()

    def get_queryset(self):
        return self.student_service.list_student()

    def create(self, request, **kwargs):
        try:
            created = self.student_service.create_student(first_name=request.data.get('first_name', None),
                                                          last_name=request.data.get('last_name', None),
                                                          school_id=request.data.get('school', None))
            serializer = StudentSerializer(created)
        except SchoolCapacityException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': str(e)})
        except TargetSchoolNotExistException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': str(e)})
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        try:
            school = self.student_service.get_student(pk)
            serializer = StudentSerializer(school)
            return Response(serializer.data)
        except EntityNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': str(e)})

    def update(self, request, pk=None, **kwargs):
        try:
            updated = self.student_service.update_student(id=pk,
                                                          first_name=request.data.get('first_name', None),
                                                          last_name=request.data.get('last_name', None),
                                                          school_id=request.data.get('school', None))
            serializer = StudentSerializer(updated)
            return Response(serializer.data)
        except EntityNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': str(e)})
        except BadArgumentException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': str(e)})

    def partial_update(self, request, pk=None, **kwargs):
        try:
            updated = self.student_service.partial_update(id=pk,
                                                          first_name=request.data.get('first_name', None),
                                                          last_name=request.data.get('last_name', None),
                                                          school_id=request.data.get('school', None))
            serializer = StudentSerializer(updated)
            return Response(serializer.data)
        except EntityNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': str(e)})
        except BadArgumentException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': str(e)})

    def destroy(self, request, pk=None, **kwargs):
        try:
            self.student_service.delete_student(id=pk)
            return Response(status=status.HTTP_200_OK)
        except EntityNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': str(e)})
