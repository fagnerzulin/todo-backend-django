from django.db import models
from django.contrib.auth.models import User


class Base(models.Model):
    createdAt = models.DateField('Created at', auto_now_add=True)
    updatedAt = models.DateField('Updated at', auto_now=True)

    class Meta:
        abstract = True


class Todo(Base):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
