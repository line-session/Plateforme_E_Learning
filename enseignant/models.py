from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class model_Cours(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    classe = models.CharField(max_length=15)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_file = models.FileField(upload_to='images/')
    video_file = models.FileField(upload_to='videos/')

    def delete(self, *args, **kwargs):
        if self.image_file:
            self.image_file.delete(save=False)
        if self.video_file:
            self.video_file.delete(save=False)
        return super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.title

class model_Devoir(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    classe = models.CharField(max_length=15)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.IntegerField()
    document_file = models.FileField(upload_to='documents/')

    def delete(self, *args, **kwargs):
        if self.document_file:
            self.document_file.delete(save=False)
        return super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.title

class model_Classe(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    effectif = models.IntegerField()

class model_Matiere(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    coef = models.IntegerField()
