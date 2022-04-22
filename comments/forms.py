from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from comments.models import Blog, Comment
from mptt.forms import TreeNodeChoiceField


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ("title", "body",)


        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Сохранить запись'))

class CommentForm(forms.ModelForm):
    author = forms.CharField(label="Ваше имя")
    parent = TreeNodeChoiceField(queryset=Comment.objects.all(), label="Ответ для:")
    text = forms.CharField(label="Ваш комментарий")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].required = False



    class Meta:
        model = Comment
        fields = ("author", "parent", "text",)


        def __init__(self, *args, **kwargs):
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Сохранить'))