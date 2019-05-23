import uuid
import json
import requests
from download.forms import PostForm
from download.models import PostModel
from bs4 import BeautifulSoup
from django.shortcuts import redirect
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
        post = self._get_record()
        if post:
            self.file_url, self.post_type = self._get_data(post)
        else:
            self.file_url, self.post_type = (None, None)

    def dispatch(self, request, *args, **kwargs):
        """Redirect if no post in database match the session id."""

        if not self.file_url:
            return redirect('form-page')

        return super(DownloadPageView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file_url'] = self.file_url
        context['post_type'] = self.post_type
        return context

    def _get_record(self):
        """Get the latest record that match the current session."""
        session_id = self.request.session.get('session_id', 0)
        # Try to get the post from the database.
        try:
            db_record = PostModel.objects.get(id__exact=session_id)
        except ObjectDoesNotExist:
            return None

        return db_record

    def _get_data(self, db_record):
        """Returns the file URLs and the post type."""
        post_url = db_record.post_url
        html = requests.get(post_url).text
        soup = BeautifulSoup(html, 'html.parser')
        data = json.loads(soup.select("script[type='text/javascript']")[3].text[21:-1])
        post_type = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["__typename"]

        if post_type == "GraphVideo":
            image_url = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["video_url"]
        elif post_type == "GraphImage":
            image_url = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["display_url"]
        elif post_type == "GraphSidecar":
            edges = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
            # Differentiate between images and videos in multi-content posts.
            # Get urls with .jpg for images and .mp4 for videos.
            image_url = [edge["node"]["video_url"] if edge["node"]["__typename"] == "GraphVideo" else edge["node"]["display_url"] for edge in edges]

        return image_url, post_type
