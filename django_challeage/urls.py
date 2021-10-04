from django.urls import path, include
from rest_framework_nested import routers
from manatal.api.v1 import views

router = routers.DefaultRouter()
router.register(r'api/v1/schools', views.SchoolViewSet, basename='school')
router.register(r'api/v1/students', views.StudentViewSet, basename='student')

school_router = routers.NestedDefaultRouter(
    router,
    r'api/v1/schools',
    lookup='school')

school_router.register(
    r'students',
    views.StudentViewSet,
    basename='school'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(school_router.urls)),
]
