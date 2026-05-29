from django.db import models

# Create your models here.


class FileRecord(models.Model):
    file = models.FileField(upload_to='uploads/')
    hash_value = models.CharField(max_length=64)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} - {self.uploaded_at:%Y-%m-%d %H:%M}"
