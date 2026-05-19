from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Rating)