from django.db import models


class Base(models.Model):
    createdAt = models.DateField('Create at', auto_now_add=True)
    updateAt = models.DateField('Update at', auto_now=True)

    class Meta:
        abstract = True


class Todo(Base):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
