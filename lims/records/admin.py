from django.contrib import admin
from records.models import *
import django.contrib.auth.models

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False

class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]

admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(User)
admin.site.register(Record)
admin.site.register(Borrow)
admin.site.unregister(django.contrib.auth.models.User)
admin.site.register(django.contrib.auth.models.User, UserAdmin)

