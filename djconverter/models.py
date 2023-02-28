from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    # name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        app_label = 'djconverter'
