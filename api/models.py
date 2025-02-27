from django.db import models

# Create your models here.
from django.db import models

class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    media = models.FileField(upload_to='notices/', blank=True, null=True)  # Upload media
    visible = models.BooleanField(default=False)  # Show/Hide Toggle
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Attendance(models.Model):
    file = models.FileField(upload_to='attendance/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attendance uploaded on {self.uploaded_at}"
