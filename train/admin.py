from django.contrib import admin
from .import models 
# Register your models here.
admin.site.register(models.Train)
admin.site.register(models.UserReviews)
admin.site.register(models.TrainPurchase)