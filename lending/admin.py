from django.contrib import admin

from . import models

admin.site.register(models.Student)
admin.site.register(models.Book)
admin.site.register(models.Lending)
admin.site.register(models.BibliographicPlan)
admin.site.register(models.StudyTopic)
