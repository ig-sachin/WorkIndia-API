
from django.db import models

# Create your models here.


# Question Model
class Questions(models.Model):
    question_title = models.CharField(max_length=255)
    question_body = models.CharField(max_length=1000)
    tags = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.question_title
