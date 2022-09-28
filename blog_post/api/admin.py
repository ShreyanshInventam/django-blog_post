from django.contrib import admin
from api.models import User, Blog, Post, Tags
# Register your models here.

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Tags)
admin.site.register(Post)