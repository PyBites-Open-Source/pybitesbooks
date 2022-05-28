from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Category, Book, Search, UserBook,
                     BookNote, Badge, BookConversion,
                     ImportedBook)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


class BookAdmin(admin.ModelAdmin):
    list_display = ("bookid", "title", "authors", "publisher", "pages", "inserted")
    search_fields = ("bookid", "title", "authors", "publisher")


class SearchAdmin(admin.ModelAdmin):
    list_display = ("term", "user", "inserted")
    search_fields = ("term", "user__username")


class UserBookAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "status", "favorite", "completed", "inserted")
    search_fields = ("user__username", "book__title", "book__bookid",)
    list_filter = ("status", "favorite")


class BookNoteAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "type_note", "short_desc", "public", "inserted")
    search_fields = ("description", "user__username")
    list_filter = ("public", "type_note")

    def short_desc(self, obj):
        limit = 30
        desc = obj.description if obj.description else ""
        if len(desc) > limit:
            return f"{obj.description[:limit]} ..."
        else:
            return obj.description
    short_desc.short_description = 'short description'


class BadgeAdmin(admin.ModelAdmin):
    list_display = ("books", "title")


class BookConversionAdmin(admin.ModelAdmin):
    list_display = ("goodreads_id", "book_link", "inserted")
    search_fields = ("goodreads_id", "googlebooks_id")

    def book_link(self, obj):
        return mark_safe(
            f"<a href='{settings.DOMAIN}/books/{obj.googlebooks_id}' "
            f"target='_blank'>{obj.googlebooks_id}</a>"
        )
    book_link.short_description = 'Google / PyBites book link'


class ImportedBookAdmin(admin.ModelAdmin):
    list_display = ("title", "book", "reading_status", "date_completed",
                    "book_status", "user")
    search_fields = ("title",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Search, SearchAdmin)
admin.site.register(UserBook, UserBookAdmin)
admin.site.register(BookNote, BookNoteAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(BookConversion, BookConversionAdmin)
admin.site.register(ImportedBook, ImportedBookAdmin)
