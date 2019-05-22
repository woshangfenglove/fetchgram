from django.forms import ModelForm
from . import models
from random import randint

class PostForm(ModelForm):
    class Meta:
        model = models.PostModel
        fields = ['post_url']

    def save(self, id, *args, **kwargs):

        s = super(PostForm, self).save(commit=False)
        s.id = id
        s.save(*args, **kwargs)
