from django.contrib import admin
from .models import model_Cours, model_Devoir, model_Classe, model_Matiere

# Register your models here.
admin.site.register(model_Cours)
admin.site.register(model_Devoir)
admin.site.register(model_Classe)
admin.site.register(model_Matiere)