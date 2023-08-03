from dataclasses import fields
from email import message
from pyexpat import model
from django import forms
from .models import Post, Topic

# Topic form
class NewTopicForm(forms.ModelForm):

    message = forms.CharField(widget=forms.Textarea( attrs={'rows':5, 'placeholder':"what's in your mind"} ), 
                              max_length=4000, 
                              help_text="the maximumu size of this post is 4000 character")
                                
    class Meta:
        model = Topic
        fields = ['subject', 'message']




# post form
class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['message']
