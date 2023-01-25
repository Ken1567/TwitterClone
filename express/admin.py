from django.contrib import admin
from .models import Profile, Message, Comment

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'comment', 'timestamp')

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'reply', 'timestamp')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Comment, CommentAdmin)