from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25) #who is sharing 
    email = forms.EmailField()  #sender's email
    to = forms.EmailField() #recipient's email 
    comments = forms.CharField( # optional message
        required=False,
        widget=forms.Textarea
    )
    
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
        fields = ['body']
        labels = {'body': ''}
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'Write your comment...',
                'rows': 4,
            })
        }
        
class SearchForm(forms.Form):
    query = forms.CharField()

class LLMForm(forms.Form):
    prompt = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={
            'rows': 1,
            'class': 'llm--textarea',
            'placeholder': 'Ask anything',
            'id': 'id_prompt',
            'style': 'resize:none;overflow:hidden;'
        })
    )
        
