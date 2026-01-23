from django import forms
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25) #who is sharing 
    email = forms.EmailField()  #sender's email
    to = forms.EmailField() #recipient's email 
    comments = forms.CharField( # optional message
        required=False,
        widget=forms.Textarea
    )
    
from .models import Comment
class CommentBoundField(forms.BoundField):  #  customize field rendering for CommentForm
    Comment_class = 'comment'  #  ensure all fields include this CSS class

    def css_classes(self, extra_classes=None):
        result = super().css_classes(extra_classes)  # why: get default classes from parent
        if self.Comment_class not in result:  # why: avoid duplicate 'comment' class
            result += f'{self.Comment_class}'  # why: append 'comment' class
        return result.strip()  # ensure no trailing spaces
class CommentForm(forms.ModelForm):
    bound_field_class = CommentBoundField
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        
class SearchForm(forms.Form):
    query = forms.CharField()