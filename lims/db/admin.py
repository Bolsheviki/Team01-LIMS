from django.contrib import admin
from django.contrib.auth.models import User
from db.models import *

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False

class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]

admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Record)
admin.site.register(Borrow)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

