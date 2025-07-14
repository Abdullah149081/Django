from tasks.models import Task, TaskDetail
from django import forms


class TailwindMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxSelectMultiple):

                existing_classes = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    f"{existing_classes} space-y-2 p-4 bg-gray-50 border border-gray-200 rounded-lg"
                ).strip()

                widget.attrs.update(
                    {"style": "display: flex; flex-direction: column; gap: 8px;"}
                )
            elif isinstance(widget, forms.Select):
                existing_classes = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    f"{existing_classes} appearance-none w-full bg-white/80 text-gray-900 font-medium px-4 py-3 pr-10 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-yellow-300 cursor-pointer shadow-sm transition-transform duration-200 group-focus-within:scale-105"
                ).strip()
            elif isinstance(widget, (forms.DateInput, forms.TimeInput)):
                existing_classes = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    f"{existing_classes} w-full shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-yellow-300 focus:border-yellow-300"
                ).strip()
            elif isinstance(widget, forms.Textarea):
                existing_classes = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    f"{existing_classes} w-full shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-yellow-300 focus:border-yellow-300 resize-vertical min-h-[80px]"
                ).strip()
            else:
                existing_classes = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    f"{existing_classes} w-full shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-yellow-300 focus:border-yellow-300"
                ).strip()


class TaskForms(TailwindMixin, forms.ModelForm):
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
        }


class TaskDetailForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ["priority", "notes"]
        widgets = {
            "priority": forms.Select(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                    "placeholder": "Enter additional notes",
                }
            ),
        }
        labels = {
            "priority": "Priority Level",
            "notes": "Additional Notes",
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
