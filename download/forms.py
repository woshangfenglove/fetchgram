import re
import requests
from django.forms import ModelForm, ValidationError
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
        """Save the data to the database from the form request."""
        s = super(PostForm, self).save(commit=False)
        s.id = id
        s.save(*args, **kwargs)

    def clean_post_url(self):
        """Sanitize tracking code and check if the url exists."""
        cleaned_data = super().clean()
        data = self.cleaned_data.get("post_url")
        sanitized_url = self._remove_utm_code(data)
        url = self._valid_url(sanitized_url)

        return url

    def _valid_url(self, url):
        """Make sure it is a working instagram url."""
        if not bool(url):
            raise ValidationError("Not an url to an instagram post.")
        if not self._url_exists(url.group()):
            raise ValidationError("The page does not exist.")

        return url.group()

    def _url_exists(self, url):
        """Return true if the HTTP request is sucessful."""
        response = requests.get(url)
        if response.status_code == 200:
            return True

        return False

    def _remove_utm_code(self, url):
        """Remove tracking code from url."""
        pattern = "^http[s]*\:\/+www.instagram.com\/[a-z]\/[A-Za-z\W]+\/"
        match = re.match(pattern, url)

        return match
