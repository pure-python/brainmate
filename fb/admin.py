from django.contrib import admin

from fb.models import UserPost, UserProfile, Interest


admin.site.register(UserPost)
admin.site.register(UserProfile)
admin.site.register(Interest)
