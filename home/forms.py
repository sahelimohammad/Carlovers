from django import forms
from .models import Post , Comment

class PostCreateUpdateForm (forms.ModelForm):
    class Meta():
        model = Post
        fields = ('body', 'image1' , 'image2' , 'image3' , 'image4' , 'priority' , 'status')


class CommentCreateForm (forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment':forms.Textarea(attrs={'class':'form-control'})
        }

class CommentReplyForm (forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment':forms.TextInput(attrs={'class':'form-control'})
        }

class PostSearchForm (forms.Form):
    search = forms.CharField()



