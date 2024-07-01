from django.db import models
from userauth.models import Student, Teacher
from academics.models import TeacherCourse
from shortuuid.django_fields import ShortUUIDField
from django.core.exceptions import ValidationError


class Assignment(models.Model):
    """
    Model for Assignment.
    """
    assignment_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="Asmt", alphabet="1234567890", primary_key=True)
    teacher_course = models.ForeignKey(TeacherCourse, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField()
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    file = models.FileField(upload_to='assignments/', null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"

class AssignmentSubmission(models.Model):
    """
    Model to store the Assignment submissions by students.
    """
    submission_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="Subm", alphabet="1234567890", primary_key=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignment_submissions')
    file = models.FileField(upload_to='assignment_submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.assignment.title} - {self.student.user.username}"

    class Meta:
        unique_together = ('assignment', 'student')
        verbose_name = "Assignment Submission"
        verbose_name_plural = "Assignment Submissions"

 

def validate_choice(instance):
    if not instance.choice_1_text and not instance.choice_1_image:
        raise ValidationError('Choice 1 must have either text or an image.')
    if not instance.choice_2_text and not instance.choice_2_image:
        raise ValidationError('Choice 2 must have either text or an image.')
    if not instance.choice_3_text and not instance.choice_3_image:
        raise ValidationError('Choice 3 must have either text or an image.')
    if not instance.choice_4_text and not instance.choice_4_image:
        raise ValidationError('Choice 4 must have either text or an image.')

def validate_question(instance):
    if not instance.question_text and not instance.question_image:
        raise ValidationError('Question must have either text or an image.')

class Quiz(models.Model):
    """
    Model for Quiz.
    """
    quiz_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="Quiz", alphabet="1234567890", primary_key=True)
    teacher_course = models.ForeignKey('academics.TeacherCourse', on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    quiz_starting_date_and_time = models.DateTimeField()
    total_questions = models.PositiveIntegerField()
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    time_limit = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

class QuizQuestion(models.Model):
    """
    Model for storing quiz questions.
    """
    
    question_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="Ques", alphabet="1234567890", primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

    question_text = models.TextField(null=True, blank=True)
    question_image = models.ImageField(upload_to='questions/', null=True, blank=True)
    
    choice_1_text = models.CharField(max_length=255, null=True, blank=True)
    choice_1_image = models.ImageField(upload_to='choices/', null=True, blank=True)
    choice_1_is_correct = models.BooleanField(default=False)
    
    choice_2_text = models.CharField(max_length=255, null=True, blank=True)
    choice_2_image = models.ImageField(upload_to='choices/', null=True, blank=True)
    choice_2_is_correct = models.BooleanField(default=False)
    
    choice_3_text = models.CharField(max_length=255, null=True, blank=True)
    choice_3_image = models.ImageField(upload_to='choices/', null=True, blank=True)
    choice_3_is_correct = models.BooleanField(default=False)
    
    choice_4_text = models.CharField(max_length=255, null=True, blank=True)
    choice_4_image = models.ImageField(upload_to='choices/', null=True, blank=True)
    choice_4_is_correct = models.BooleanField(default=False)

    def get_correct_choice(self):
        if self.choice_1_is_correct:
            return 1
        elif self.choice_2_is_correct:
            return 2
        elif self.choice_3_is_correct:
            return 3
        elif self.choice_4_is_correct:
            return 4
        return None

    def clean(self):
        validate_question(self)
        validate_choice(self)

    def __str__(self):
        return f"{self.question_text or 'Image Question'}"

    class Meta:
        verbose_name = "Quiz Question"
        verbose_name_plural = "Quiz Questions"

class QuizSubmission(models.Model):
    """
    Model to store the submissions of Quizzes.
    """
    submission_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="Subm", alphabet="1234567890", primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey('userauth.Student', on_delete=models.CASCADE, related_name='quiz_submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('quiz', 'student')
        verbose_name = "Quiz Submission"
        verbose_name_plural = "Quiz Submissions"

    def __str__(self):
        return f"{self.quiz.title} - {self.student.user.username}"

class QuizAnswer(models.Model):
    """
    Model to store answers to quiz questions.
    """
    answer_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="Ans", alphabet="1234567890", primary_key=True)
    submission = models.ForeignKey(QuizSubmission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='answers')
    selected_choice = models.PositiveIntegerField()

    def __str__(self):
        return f"Answer to {self.question.question_text or 'Image Question'}"

    class Meta:
        unique_together = ('submission', 'question')
        verbose_name = "Quiz Answer"
        verbose_name_plural = "Quiz Answers"
