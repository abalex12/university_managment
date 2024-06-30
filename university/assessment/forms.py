from django import forms
from .models import Assignment, AssignmentSubmission, Quiz, QuizQuestion, QuizSubmission, QuizAnswer
from django.forms import modelformset_factory
from django.utils import timezone


# Form for creating an Assignment
class AssignmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'max_score', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

# Form for submitting an Assignment
class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = [ 'file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class QuizCreateForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'quiz_starting_date_and_time', 'total_questions', 'time_limit', 'max_score']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'quiz_starting_date_and_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'total_questions': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'time_limit':forms.NumberInput(attrs={'class':'form-control'}),
        }
class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = [
            'question_text', 'question_image',
            'choice_1_text', 'choice_1_image', 'choice_1_is_correct',
            'choice_2_text', 'choice_2_image', 'choice_2_is_correct',
            'choice_3_text', 'choice_3_image', 'choice_3_is_correct',
            'choice_4_text', 'choice_4_image', 'choice_4_is_correct'
        ]
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 2,'class': 'form-control'}),
            'choice_1_text': forms.Textarea(attrs={'rows': 1,'class': 'form-control'}),
            'choice_2_text': forms.Textarea(attrs={'rows': 1,'class': 'form-control'}),
            'choice_3_text': forms.Textarea(attrs={'rows': 1,'class': 'form-control'}),
            'choice_4_text': forms.Textarea(attrs={'rows': 1,'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Validate question
        question_text = cleaned_data.get("question_text")
        question_image = cleaned_data.get("question_image")
        if not question_text and not question_image:
            raise forms.ValidationError('Question must have either text or an image.')

        # Validate choices
        choices = [
            (cleaned_data.get("choice_1_text"), cleaned_data.get("choice_1_image")),
            (cleaned_data.get("choice_2_text"), cleaned_data.get("choice_2_image")),
            (cleaned_data.get("choice_3_text"), cleaned_data.get("choice_3_image")),
            (cleaned_data.get("choice_4_text"), cleaned_data.get("choice_4_image")),
        ]
        for i, (text, image) in enumerate(choices, start=1):
            if not text and not image:
                raise forms.ValidationError(f'Choice {i} must have either text or an image.')
        return cleaned_data

