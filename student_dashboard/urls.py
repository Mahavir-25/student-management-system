from django.urls import path
from django.urls import reverse_lazy
from django.conf import settings
from student_dashboard.views import Indexview
from django.contrib.auth.views import LogoutView
from student_dashboard.views import StudentProfileView,MyCoursesView,CourseDetailView,StudentUpdateView
urlpatterns = [
    path('index/',Indexview.as_view(),name='student_index'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', StudentProfileView.as_view(), name='student_profile'),
    path('student-course/', MyCoursesView.as_view(), name='student-course'),
    path('student/update/<int:pk>/', StudentUpdateView.as_view(), name='update_student'),
    path('student/course/<int:pk>/', CourseDetailView.as_view(), name='student_course_details')
]
