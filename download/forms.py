from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import PostModel

class PostForm(ModelForm):
    class Meta:
        model = PostModel
        fields = ['post_url']
        labels = {
            'post_url': _(''),
        }

    def save(self, id, *args, **kwargs):
        s = super(PostForm, self).save(commit=False)
        s.id = id
        s.save(*args, **kwargs)
