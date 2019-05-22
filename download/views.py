import uuid
import json
import requests
from download.forms import PostForm
from download.models import PostModel
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView


class FormPageView(FormView):

    template_name = 'download/index.html'
    form_class = PostForm
    success_url = '/download/'

    def form_valid(self, form):
        id = self.session_data()
        form.save(id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def session_data(self):
        session_id = None
        if session_id == None:
            id = uuid.uuid4()
            session_id = self.request.session.get('session_id', 0)
            self.request.session['session_id'] = str(id)
        return id


class DownloadPageView(TemplateView):
    """The download page that the instagram post will show up on."""

    template_name = 'download/result.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        post = self.get_record()

        if post:
            self.image_url = self.get_url(post)
        else:
            self.image_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_url'] = self.image_url
        return context

    def get_record(self):
        """Get the latest record that match the current session."""

        session_id = self.request.session.get('session_id', 0)

        # Try to get the post from the database.
        try:
            db_record = PostModel.objects.get(id__exact=session_id)
        except ObjectDoesNotExist:
            return None

        return db_record

    def get_url(self, db_record):
        """Get the url to the image in the post."""
        post_url = db_record.post_url
        html = requests.get(post_url).text
        soup = BeautifulSoup(html, 'html.parser')
        data = json.loads(soup.select("script[type='text/javascript']")[3].text[21:-1])
        image_url = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["display_url"]

        return image_url
