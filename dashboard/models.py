from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# ✅ Custom User Manager
class StudentUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

# ✅ Custom User Model
class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    


    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('student', 'Student'),
    ]

    phone = models.CharField(max_length=15 ,blank=True,null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,blank=True,null=True)
    dob = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='students/', blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    enroll_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    objects = StudentUserManager()

    def save(self, *args, **kwargs):
        if self.role == 'student' and not self.enroll_number:
            last_student = User.objects.filter(role='student').exclude(enroll_number__isnull=True).order_by('-id').first()
            if last_student and last_student.enroll_number and last_student.enroll_number.startswith("ENR"):
                try:
                    last_number = int(last_student.enroll_number.replace("ENR", ""))
                except ValueError:
                    last_number = 0
                self.enroll_number = f"ENR{last_number + 1:04d}"
            else:
                self.enroll_number = "ENR0001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"
class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)  # Example: "3 Months"
    
    trainers = models.ManyToManyField(
        User,
        null=True,
        blank=True,
        limit_choices_to={'role': 'staff'},
        related_name='courses_as_trainer'
    )

    timing = models.CharField(max_length=100)  # Example: "Mon–Fri, 10AM–12PM"

    def __str__(self):
        return self.name
class BookedCourse(models.Model):
    BATCH_CHOICES = [
        ('8-9', '8:00 AM to 9:00 AM'),
        ('9-10', '9:00 AM to 10:00 AM'),
        ('10-11', '10:00 AM to 11:00 AM'),
        ('11-12', '11:00 AM to 12:00 PM'),
        ('1-2', '1:00 PM to 2:00 PM'),
        ('2-3', '2:00 PM to 3:00 PM'),
        ('3-4', '3:00 PM to 4:00 PM'),
        ('4-5', '4:00 PM to 5:00 PM'),
        ('5-6', '5:00 PM to 6:00 PM'),
        ('6-7', '6:00 PM to 7:00 PM'),
        ('7-8', '7:00 PM to 8:00 PM'),
        ('8-9pm', '8:00 PM to 9:00 PM'),  # ✅ changed duplicate key
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    students = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='booked_courses_as_student',
        limit_choices_to={'role': 'student'}
    )

    staff = models.ManyToManyField(
        User,
        blank=True,
        related_name='booked_courses_as_staff',
        limit_choices_to={'role': 'staff'}
    )

    batch = models.CharField(max_length=20, choices=BATCH_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # first save object

        # ✅ Copy trainers from course to staff
        if self.course and self.course.trainers.exists():
            self.staff.set(self.course.trainers.all())  # overwrite staff with course trainers

    def __str__(self):
        return f"{self.course.name} - {self.batch}"

