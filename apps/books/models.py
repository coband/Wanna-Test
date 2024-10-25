import uuid
from django.db import models

# Create your models here.

class Book(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=255, null=True, blank=True)
  author = models.CharField(max_length=255, null=True, blank=True)
  ISBN = models.CharField(max_length=255, null=True, blank=True)
  subject = models.CharField(max_length=255, null=True, blank=True)
  published_date = models.DateField(null=True, blank=True)
  
  def __str__(self):
      return self.title