from django.contrib import admin
from problems.models import Problem, TestCase
from django import forms
from ckeditor.widgets import CKEditorWidget

class ProblemAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    input_format = forms.CharField(widget=CKEditorWidget())
    output_format = forms.CharField(widget=CKEditorWidget())
    note = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Problem
        
class ProblemAdmin(admin.ModelAdmin):
    form = ProblemAdminForm
    
admin.site.register(Problem, ProblemAdmin)
admin.site.register(TestCase)