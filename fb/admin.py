from django.contrib import admin

from fb.models import UserPost, UserProfile, Friendship


admin.site.register(UserPost)
admin.site.register(UserProfile)
admin.site.register(Friendship)
