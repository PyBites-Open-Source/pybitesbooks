from django.contrib import admin

from .models import (Book, Search, UserBook,
                     BookNote, Badge)


class BookAdmin(admin.ModelAdmin):
    pass


class SearchAdmin(admin.ModelAdmin):
    pass


class UserBookAdmin(admin.ModelAdmin):
    pass


class BookNoteAdmin(admin.ModelAdmin):
    pass


class BadgeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(Search, SearchAdmin)
admin.site.register(UserBook, UserBookAdmin)
admin.site.register(BookNote, BookNoteAdmin)
admin.site.register(Badge, BadgeAdmin)
