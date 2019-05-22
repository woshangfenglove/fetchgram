from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from . import forms
from . import models

import uuid
import json
import requests
from bs4 import BeautifulSoup

def index(request):

    session_id = None

    if request.method == 'POST':

        if session_id == None:
            id = uuid.uuid4()
            session_id = request.session.get('session_id', 0)
            request.session['session_id'] = str(id)

        form = forms.PostForm(request.POST)
        if form.is_valid():
            form.save(id)
            return HttpResponseRedirect(reverse('download-page'))
        else:
            messages.error(request, "Error")

    context = {
        'form': forms.PostForm(),
        'id': session_id,
    }

    return render(request, 'download/index.html', context)


def result(request):

    session_id = request.session.get('session_id', 0)
    try:
        image = models.PostModel.objects.get(id__exact=session_id)
        image_id = str(image.id)
    except ObjectDoesNotExist:
        image = None
        image_id = None

    image_url = None

    if session_id == image_id:
        print("worked????")
        url = image.post_url
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        data = json.loads(soup.select("script[type='text/javascript']")[3].text[21:-1])
        image_url = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["display_url"]

    context = {
        'image_url': image_url,
        'image_id': image_id,
        'session_id': session_id,
    }

    return render(request, 'download/result.html', context)
