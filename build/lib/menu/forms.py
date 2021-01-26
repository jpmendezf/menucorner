from django import forms
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from .models import Menu, Lunch, Option, timezone, BroadCast_Email


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["title"]


class LunchForm(forms.ModelForm):
    class Meta:
        model = Lunch
        fields = ["prompt"]


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["text"]


class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop("options")
        # Options must be a list of Option objects
        choices = {(o.pk, o.text) for o in options}
        super().__init__(*args, **kwargs)
        option_field = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, required=True)
        self.fields["option"] = option_field


class BaseAnswerFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["options"] = kwargs["options"][index]
        return kwargs
