from django.contrib import admin

from cloneable_model.admin import CloneableModelAdminMixin

from modules.admin import ModuleTabularInline
from .models import Conference, ConferenceAttendee, Settings, Uroboros


class AttendeeTabularInline(admin.TabularInline):
    model = ConferenceAttendee
    extra = 0


class ConferenceAdmin(CloneableModelAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'code', 'created')
    list_display_links = ('title',)
    readonly_fields = ('code',) 
    inlines = [AttendeeTabularInline, ModuleTabularInline]
    save_on_top = True
    fieldsets = (
        ('Main', {
            'fields': ['client', 'title', 'code', 'settings']
        }),
    )


class ConferenceAttendeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'conference', 'user')
    list_display_links = ('conference',)
    list_select_related = True


class UroborosAdmin(CloneableModelAdminMixin, admin.ModelAdmin):
    list_display = ('id', '__str__', 'parent')
    list_display_links = ('__str__',)
    list_select_related = True


admin.site.register(Conference, ConferenceAdmin)
admin.site.register(ConferenceAttendee, ConferenceAttendeeAdmin)
admin.site.register(Settings)
admin.site.register(Uroboros, UroborosAdmin)
