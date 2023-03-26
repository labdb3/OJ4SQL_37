from django.contrib import admin
from . import models

admin.site.register(models.Problem)
admin.site.register(models.Group)
admin.site.register(models.UserGroup)
admin.site.register(models.Submission)
