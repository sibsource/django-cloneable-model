from django.contrib import admin

from cloneable_model.admin import CloneableModelAdminMixin

from .models import (
    Module, Event, EventAttendee, ScheduleModule, EventDocument,
    EventPresenter, DocumentsModule, Category, Document, PresentersModule,
    Presenter
)


class ModuleTabularInline(admin.TabularInline):
    model = Module
    extra = 0


class EventAttendeeTabularInline(admin.TabularInline):
    model = EventAttendee
    extra = 0
    fields = ('attendee',)


class EventDocumentTabularInline(admin.TabularInline):
    model = EventDocument
    extra = 0


class EventPresenterTabularInline(admin.TabularInline):
    model = EventPresenter
    extra = 0


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'conference', 'created')
    list_display_links = ('title',)
    list_select_related = True


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'schedule', 'created')
    list_display_links = ('name',)
    list_select_related = True

    inlines = [
        EventAttendeeTabularInline, EventDocumentTabularInline,
        EventPresenterTabularInline
    ]


class DocumentsModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'conference', 'created')
    list_display_links = ('title',)
    list_select_related = True


class PresentersModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'conference', 'created')
    list_display_links = ('title',)
    list_select_related = True


class CategoryAdmin(CloneableModelAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'module')
    list_display_links = ('name',)
    list_select_related = True


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_display_links = ('name',)
    list_select_related = True


admin.site.register(Module, ModuleAdmin)
admin.site.register(ScheduleModule)
admin.site.register(Event, EventAdmin)
admin.site.register(EventAttendee)
admin.site.register(EventDocument)
admin.site.register(EventPresenter)
admin.site.register(DocumentsModule, DocumentsModuleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(PresentersModule, PresentersModuleAdmin)
admin.site.register(Presenter)
