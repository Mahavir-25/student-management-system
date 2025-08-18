from django.shortcuts import redirect
from django.views.generic import TemplateView,ListView,DetailView,UpdateView
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models import BookedCourse,Course,User
from student_dashboard.form import EditUserForm
from django.urls import reverse_lazy


class StudentOnlyView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'  # replace with your actual template

    def dispatch(self, request, *args, **kwargs):
        # Check if user is authenticated and role is 'student'
        if not request.user.is_authenticated or getattr(request.user, 'role', None) != 'student':
            raise Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)
class Indexview(StudentOnlyView, TemplateView):
    template_name = 'student_dashboard/index.html'
    login_url = 'login'  # name of your login URL

class StudentProfileView(StudentOnlyView,TemplateView):
    template_name = 'student_dashboard/student_profile.html'


class StudentUpdateView(UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'student_dashboard/edit-student.html' 
    login_url = '/'

    def form_valid(self, form):
        self.object = form.save()
        print("✅ Student data updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("❌ Form errors:", form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('student_profile')  # Replace with your correct success URL

class MyCoursesView(LoginRequiredMixin, ListView):
    model = BookedCourse
    template_name = 'student_dashboard/student_course.html'
    context_object_name = 'courses'

    def get_queryset(self):
        # Show only booked courses for the currently logged-in student
        return BookedCourse.objects.select_related('course').filter(
            students=self.request.user
        ).order_by('-created_at')


class CourseDetailView(DetailView):
    model = BookedCourse
    template_name = 'student_dashboard/student_course_details.html'
    context_object_name = 'course'

    