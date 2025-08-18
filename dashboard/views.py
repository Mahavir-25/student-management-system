from django.views.generic import TemplateView,ListView,UpdateView,DeleteView,DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from dashboard.models import User,Course,BookedCourse
from dashboard.form import UserForm,LoginForm,ForgotPasswordForm, ResetPasswordForm,CourseForm,BookedCourseForm
from django.shortcuts import redirect,render
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.views.generic import FormView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
class LoginRequiredAdminOnlyMixin(LoginRequiredMixin):
    login_url = '/'  # Redirect to login if not authenticated

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Check if user is admin
        if getattr(request.user, 'role', None) != 'admin':
            raise Http404("Page not found")

        return super().dispatch(request, *args, **kwargs)
 
class LoginView(FormView):
    template_name = 'dashboard/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')  # fallback if role is not matched

    def form_valid(self, form):
        user = form.user
        login(self.request, user)

        # Redirect based on user role
        if user.role == 'student':
            return redirect('student_index')
        elif user.role == 'admin':
            return redirect('index')
        else:
            # fallback if role is unknown
            return redirect('index')

    def form_invalid(self, form):
        return super().form_invalid(form)
    



class DeleteUserView(LoginRequiredAdminOnlyMixin, DeleteView):
    login_url = '/'
    model = User
    template_name = 'dashboard/confirm-delete.html'  # Optional, you can keep or remove

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        role = self.object.role

        self.object.delete()
        messages.success(request, f"{role.capitalize()} deleted successfully.")

        # Redirect based on role
        if role == 'student':
            return redirect('student_list')
        elif role == 'staff':
            return redirect('staff_list')
        else:
            return redirect('/')

class StudentDetailView(LoginRequiredAdminOnlyMixin,DetailView):
    login_url='/'
    model = User
    template_name = 'dashboard/student_detail.html'
    context_object_name = 'student'
class StaffDetailView(LoginRequiredAdminOnlyMixin,DetailView):
    login_url='/'
    model = User
    template_name = 'dashboard/staff_detail.html'
    context_object_name = 'staff' 

class StudentListView(LoginRequiredAdminOnlyMixin, ListView):
    login_url = '/'
    model = User
    template_name = 'dashboard/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        return User.objects.filter(role='student')
class StaffListView(LoginRequiredAdminOnlyMixin, ListView):
    login_url = '/'
    model = User
    template_name = 'dashboard/staff_list.html'
    context_object_name = 'Staff'

    def get_queryset(self):
        return User.objects.filter(role='staff')
class CourseListView(LoginRequiredAdminOnlyMixin,ListView):
    login_url = '/'
    model = Course
    template_name = 'dashboard/course-list.html'
    context_object_name = 'courses'

class StudentCreateView(LoginRequiredAdminOnlyMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'dashboard/add-student.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        if user.role == 'student':
            return redirect('student_list')
        else:
            return redirect('staff_list')

    def form_invalid(self, form):
        print()
        print("Form Errors:", form.errors)
        return super().form_invalid(form)
    
class AddCourseView(LoginRequiredAdminOnlyMixin,CreateView):
    model=Course
    form_class=CourseForm
    template_name = 'dashboard/course-form.html'
    success_url = reverse_lazy('course_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context

    def form_valid(self,form):
        Course =form.save(commit=False)
        print("saving Course:",Course.name)
        Course.save()
        return redirect('course_list')
    def form_invalid(self,form):
        print("Form Error:",form.errors)
        return super().form_invalid(form)
    
class UpdateCourseView(LoginRequiredAdminOnlyMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'dashboard/course-form.html'
    success_url = reverse_lazy('course_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True 
        return context
class DeleteCourseView(LoginRequiredAdminOnlyMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('course_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)

class CourseDetailView(LoginRequiredAdminOnlyMixin, DetailView):
    model = Course
    template_name = 'dashboard/course-details.html'
    context_object_name = 'course'
        

class HomeView(LoginRequiredAdminOnlyMixin,TemplateView):
    login_url = '/'
    template_name = "dashboard/index.html"
    

class AppProfileView(LoginRequiredAdminOnlyMixin,TemplateView):
    login_url='/'
    template_name = "dashboard/app-profile.html"




class ForgotPasswordView(FormView):
    template_name = 'dashboard/forgot_password.html'
    form_class = ForgotPasswordForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        self.request.session['reset_email'] = email
        return redirect('reset-password')


class ResetPasswordView(FormView):
    template_name = 'dashboard/reset_password.html'
    form_class = ResetPasswordForm

    def dispatch(self, request, *args, **kwargs):
        if 'reset_email' not in request.session:
            messages.error(request, "Session expired. Please try again.")
            return redirect('forgot-password')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = self.request.session.get('reset_email')
        user = User.objects.get(email=email)
        new_password = form.cleaned_data['new_password']
        user.set_password(new_password)
        user.save()
        messages.success(self.request, "Password reset successfully.")
        return redirect('login')
class IndexView(LoginRequiredAdminOnlyMixin,TemplateView):
    login_url = '/'
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_count'] = User.objects.filter(role='student').count()
        context['staff_count'] = User.objects.filter(role='staff').count()
        context['course_count'] = Course.objects.count()
        return context
class BookedCourseCreateView(CreateView):
    model = BookedCourse
    form_class = BookedCourseForm
    template_name = 'dashboard/book_course.html'
    success_url = reverse_lazy('bookedcourse_list')
    def form_valid(self, form):
        booked_course = form.save(commit=False)
        booked_course.save()
        return super().form_valid(form)
    def form_invalid(self, form):
        return super().form_invalid(form)



class BookedCourseListView(ListView):
    model = BookedCourse
    template_name = 'dashboard/bookedcourse-list.html' 
    context_object_name = 'booked_courses'

class BookedCourseUpdateView(UpdateView):
    model = BookedCourse
    form_class = BookedCourseForm
    template_name = 'dashboard/book_course.html'  # Reuse template
    success_url = reverse_lazy('bookedcourse_list')

class BookedCourseDeleteView(TemplateView):
    def get(self, request, pk):
        course = get_object_or_404(BookedCourse, pk=pk)
        course.delete()
        return redirect(reverse_lazy('bookedcourse_list'))
# Optional: Commented pages (uncomment as needed)
# class EmailComposeView(TemplateView):
#     template_name = "dashboard/email-compose.html"

# class EmailInboxView(TemplateView):
#     template_name = "dashboard/email-inbox.html"

# class EmailReadView(TemplateView):
#     template_name = "dashboard/email-read.html"

# class AppCalenderView(TemplateView):
#     template_name = "dashboard/app-calender.html"

# class ChartFlotView(TemplateView):
#     template_name = "dashboard/chart-flot.html"

# class ChartMorrisView(TemplateView):
#     template_name = "dashboard/chart-morris.html"

# class ChartChartjsView(TemplateView):
#     template_name = "dashboard/chart-chartjs.html"

# class ChartChartistView(TemplateView):
#     template_name = "dashboard/chart-chartist.html"

# class ChartSparklineView(TemplateView):
#     template_name = "dashboard/chart-sparkline.html"

# class ChartPeityView(TemplateView):
#     template_name = "dashboard/chart-peity.html"
# class UpdatePasswordView(FormView):
#     template_name ="dashboard/update_password.html"
#     form_class = Updatepassword