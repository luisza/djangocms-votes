from django.contrib import admin
from djcms_votes.models import Poll, Comment

# Register your models here.

# admin.site.register(Poll)


class AdminComment(admin.ModelAdmin):
    list_display = ('user', 'comment_type')


class AdminPoll(admin.ModelAdmin):
    list_display = ('user', 'poll_type')

admin.site.register(Poll, AdminPoll)
admin.site.register(Comment, AdminComment)
