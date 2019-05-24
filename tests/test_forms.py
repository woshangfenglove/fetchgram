from django.test import TestCase
from django.forms import ValidationError
from download.forms import PostForm


class PostFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.post_form = PostForm()

    def test_url_exists_with_response_200(self):
        response_200 = "https://www.instagram.com/p/BxiH_HHBcq7"
        self.assertTrue(self.post_form._url_exists(response_200), 200)

    def test_url_exists_with_response_404(self):
        response_404 = "https://www.instagram.com/ppppppppp/BxiH_HHBcq7"
        self.assertFalse(self.post_form._url_exists(response_404), 404)

    def test_remove_utm_code(self):
        has_utm = "https://www.instagram.com/p/BrlwBBKgK4P/?utm_source=ig_web_copy_link"
        has_not_utm = "https://www.instagram.com/p/BrlwBBKgK4P"
        self.assertEqual(self.post_form._remove_utm_code(has_utm).group(), has_not_utm)

    def test_valid_url_raise_error_not_instagram_post(self):
        # List of urls that shouldn't match the pattern
        # of an instagram posts url.
        urls = [
            "http://127.0.0.1",
            "https://docs.djangoproject.com/en/2.2/",
            "https://developer.mozilla.org/en-US/docs/",
            "https://duckduckgo.com/?q=hello+world&t=ffab&ia=web",
            "https://www.instagram.com/"
        ]

        for url in urls:
            with self.assertRaises(ValidationError) as msg:
                self.post_form._valid_url(self.post_form._remove_utm_code(url))
            self.assertTrue("That's not an instagram post." in msg.exception)

    def test_valid_url_raise_error_is_instagram_post_but_404(self):
        # List of urls to instagram posts that match the pattern
        # for working urls, but gives a 404 response.
        urls = [
            "https://www.instagram.com/p/BxiH_H4HBc-q7bbb/",
            "https://www.instagram.com/p/Bx3iH_HHBcq-7aaa/",
        ]

        for url in urls:
            with self.assertRaises(ValidationError) as msg:
                self.post_form._valid_url(self.post_form._remove_utm_code(url))
            self.assertTrue("The page does not exist." in msg.exception)

    def test_valid_url_is_instagram_post(self):

        # List of working urls to instagram posts.
        urls = [
            "https://www.instagram.com/p/Bx0qIjAgiv7/?utm_source=ig_web_copy_link",
            "https://www.instagram.com/p/Bw-V6TyhBMd/?utm_source=ig_web_copy_link",
            "https://www.instagram.com/p/BxiH_HHBcq7/",
        ]

        for url in urls:
            cleaned_url = self.post_form._remove_utm_code(url)
            result = self.post_form._valid_url(cleaned_url)
            self.assertEqual(result, cleaned_url.group())
