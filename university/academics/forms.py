from django import forms
from userauth.models import User, Student, Teacher
from academics.models import SemesterYear,AcademicYear,Semester

from .models import SemesterYear

class SemesterYearForm(forms.Form):
    # semester_year = forms.ModelChoiceField(queryset=SemesterYear.objects.all(), label="Select Semester and Academic Year")
    academic_year=forms.ModelChoiceField(queryset=AcademicYear.objects.all(), label="select the Acadamic year")
    semester=forms.ModelChoiceField(queryset=Semester.objects.all(), label="select the semester")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['academic_year'].widget.attrs.update({'class': 'form-control'})
        self.fields['semester'].widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'gender', 'date_of_birth', 'email', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        readonly_fields = ['first_name', 'last_name', 'username', 'date_of_birth']
        for field in readonly_fields:
            self.fields[field].widget.attrs['readonly'] = 'readonly'
        self.fields['gender'].widget.attrs['disabled'] = 'disabled'

        self.fields['profile_picture'].required = False
        self.fields['gender'].widget.attrs['class'] = 'form-control my-custom-class'
        self.fields['first_name'].widget.attrs['class'] = 'form-control my-custom-class'
        self.fields['last_name'].widget.attrs['class'] = 'form-control my-custom-class'
        self.fields['username'].widget.attrs['class'] = 'form-control my-custom-class'
        self.fields['date_of_birth'].widget.attrs['class'] = 'form-control my-custom-class'
        self.fields['email'].widget.attrs['class'] = 'form-control my-custom-class'
        self.fields['profile_picture'].widget.attrs['class'] = 'form-control-file my-custom-class'

    def clean_gender(self):
        # Return the existing gender value to prevent it from being changed
        return self.instance.gender

class StudentDetailsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['semester', 'department', 'year', 'section']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        readonly_fields = ['semester', 'department', 'section', 'year']
        for field in readonly_fields:
            self.fields[field].widget.attrs['disabled'] = 'disabled'

        self.fields['semester'].queryset = SemesterYear.objects.all()
        self.fields['semester'].widget.attrs['class'] = 'form-control my-custom-class'
        self.fields['department'].widget.attrs['class'] = 'form-control my-custom-class'
        self.fields['section'].widget.attrs['class'] = 'form-control my-custom-class'
        self.fields['year'].widget.attrs['class'] = 'form-control my-custom-class'

class TeacherDetailsForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['qualifications', 'department', 'research_interests', 'office_hours']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        readonly_fields = ['qualifications', 'department']
        for field in readonly_fields:
            self.fields[field].widget.attrs['readonly'] = 'readonly'

        self.fields['qualifications'].widget.attrs['class'] = 'form-control my-custom-class'
        self.fields['department'].widget.attrs['class'] = 'form-control my-custom-class'
        self.fields['research_interests'].widget.attrs['class'] = 'form-control my-custom-class'
        self.fields['office_hours'].widget.attrs['class'] = 'form-control my-custom-class'
