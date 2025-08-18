from django.urls import path
from dashboard.views import IndexView,BookedCourseDeleteView,BookedCourseUpdateView,BookedCourseCreateView,BookedCourseListView,CourseDetailView,DeleteCourseView,UpdateCourseView,AddCourseView,CourseListView,StaffListView,StaffDetailView,HomeView,LoginView,AppProfileView,StudentCreateView,StudentListView,StudentDetailView,DeleteUserView,LogoutView,ForgotPasswordView,ResetPasswordView
from django.conf import settings
from django.urls import reverse_lazy

from django.conf.urls.static import static
urlpatterns = [
    path('index',HomeView.as_view(),name='Home'),
    path('',LoginView.as_view(),name="login"),
    path('index/',IndexView.as_view(),name='index'),
    path('apps/profiles/',AppProfileView.as_view(),name='app_profile'),
    path('student/addstudent/', StudentCreateView.as_view(), name='add_student'),
    path('student/list/', StudentListView.as_view(), name='student_list'),
    path('staff/list/', StaffListView.as_view(), name='staff_list'),
    path('student/view/<int:pk>/', StudentDetailView.as_view(), name='view_student'),
    path('staff/view/<int:pk>/', StaffDetailView.as_view(), name='view_Staff'),
    path('delete/user/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('course/addcourse/',AddCourseView.as_view(),name='add_course'),
    path('course/<int:pk>/update/', UpdateCourseView.as_view(), name='update_course'),
    path('course/courselist/',CourseListView.as_view(),name='course_list'),
    path('course/<int:pk>/delete/', DeleteCourseView.as_view(), name='delete_course'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('Book-course/', BookedCourseCreateView.as_view(), name='book_course'),
    path('booked-courses/', BookedCourseListView.as_view(), name='bookedcourse_list'),
    path('bookedcourse/update/<int:pk>/', BookedCourseUpdateView.as_view(), name='update_booked_course'),
    path('delete_bookedcourse/update/<int:pk>/', BookedCourseDeleteView.as_view(), name='delete_bookedcourse'),



    
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

