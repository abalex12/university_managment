from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class Role(models.Model):


    role_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="Role", alphabet="1234567890")
    role_name = models.CharField(max_length=100)
    def __str__(self):
        return self.role_name

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

class User(AbstractUser):
    user_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="User", alphabet="1234567890", primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100, unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    account_status = models.CharField(max_length=20, default='Active')
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role:
            if instance.role.role_name == 'Student':
                Student.objects.create(user=instance)
            elif instance.role.role_name == 'Teacher':
                Teacher.objects.create(user=instance)
                


class Teacher(models.Model):
    teacher_id = ShortUUIDField(
        length=7, 
        prefix='tea', 
        primary_key=True,
        alphabet="1234567890"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,editable=False)
    qualifications = models.TextField(null=True, blank=True)
    # experience = models.PositiveIntegerField()
    office_hours = models.CharField(max_length=255, null=True, blank=True)
    research_interests = models.TextField(null=True, blank=True)
    department = models.ForeignKey('academics.Department', on_delete=models.SET_NULL, null=True,related_name='Teacher')

    def __str__(self):
        return f"Teacher: {self.user.username}"

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

class Student(models.Model):
    student_id = ShortUUIDField(
         length=7, 
         prefix='stu', 
         primary_key=True,alphabet="1234567890"
    )    
    user = models.OneToOneField(User, on_delete=models.CASCADE,editable=False)
    section=models.ForeignKey('academics.Section',on_delete=models.SET_NULL,null=True)
    year=models.ForeignKey('academics.year',on_delete=models.SET_NULL,null=True)
    semester=models.ForeignKey('academics.SemesterYear',on_delete=models.SET_NULL,null=True)
    department = models.ForeignKey('academics.Department', on_delete=models.SET_NULL, null=True)
    

    def __str__(self):
        return f"Student: {self.user.username}"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        