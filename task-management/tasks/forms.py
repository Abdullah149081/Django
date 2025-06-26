from tasks.models import Task
from django import forms


class TaskForms(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "assigned_to"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                    "placeholder": "Enter task title",
                },
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                    "placeholder": "Enter task description",
                },
            ),
            "due_date": forms.DateInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                    "type": "date",
                }
            ),
            "assigned_to": forms.CheckboxSelectMultiple(),
        }
        labels = {
            "title": "Task Title",
            "description": "Task Description",
            "due_date": "Due Date",
            "assigned_to": "Assigned To",
            "priority": "Priority",
        }


# Basic form for creating tasks
# class TaskForms(forms.Form):
# title = forms.CharField(max_length=100, required=True, label="Title")
# description = forms.CharField(
#     widget=forms.Textarea, required=True, label="Description"
# )
# due_date = forms.DateField(
#     required=True, label="Due Date", widget=forms.DateInput(attrs={"type": "date"})
# )
# assigned_to = forms.MultipleChoiceField(
#     required=True,
#     label="Assigned To",
#     widget=forms.CheckboxSelectMultiple,
#     choices=[],
# )

# def __init__(self, *args, **kwargs):
#     employees = kwargs.pop("employees", [])
#     self_choices = [(emp_id, emp_name) for emp_id, emp_name in employees]
#     super().__init__(*args, **kwargs)
#     self.fields["assigned_to"].choices = self_choices
