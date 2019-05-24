import uuid
from django.db import models


class PostModel(models.Model):
    post_url = models.URLField()
    date_time = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"URL: {self.post_url}"
