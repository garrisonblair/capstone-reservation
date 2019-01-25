from django.db import models


class EmailId(models.Model):
    email_id = models.CharField(max_length=16)
