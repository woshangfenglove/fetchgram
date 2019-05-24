![preview image](preview.gif)

# Fetchgram

A simple Django website that makes it easy to download images and videos from public Instagram posts.

## What it does

Check that the entered url is valid and working.

Remove any [UTM parameters](https://en.wikipedia.org/wiki/UTM_parameters) from the url.

Get a response of the given url with the HTML code of the page before javascript has generated the real page.

Extract the JSON from the html and use it to get files from three types of posts:

- *GraphImage:* Posts containing one photo.
- *GraphVideo:* Posts containing one video.
- *GraphSidecar:* Posts containing multiple photos and/or videos.

### Running tests

`python3 manage.py test`

### Built with

- [Python 3.6.8](https://docs.python.org/3.6/)
- [Django 2.2.1](https://www.djangoproject.com/)
- [Beautiful Soup 4.7.1](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests 2.22.0](https://2.python-requests.org/en/master/)
