from django.contrib import admin

from fb.models import UserPost, UserProfile, Questionnaire, Question, Answer, Interest


admin.site.register(UserPost)
admin.site.register(UserProfile)
admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Interest)
