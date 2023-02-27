from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')

    class Meta:
        app_label = 'djconverter'
