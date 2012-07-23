from django.db import models
from django.forms.models import ModelForm
from django.conf import settings


########
# Do Not Use! Use look.models
########

# Create your models here.
class Look(models.Model):
    look_photo = models.ImageField(upload_to='looks')
    look_photo_path = models.FilePathField()
    look_short_desc = models.TextField()
    look_description = models.TextField()
    look_photo_upload_datetime = models.DateTimeField(auto_now=True)
    look_photo_upload_IP_addr = models.IPAddressField()

class LookUploadForm(ModelForm):
    class Meta:
        model = Look
        fields = {'look_photo','look_description'}
