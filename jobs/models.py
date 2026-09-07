from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    description = models.TextField(help_text="You can use HTML for formatting.")
    requirements = models.TextField(help_text="You can use HTML for formatting.")
    is_active = models.BooleanField(default=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return self.title