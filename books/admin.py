from django.contrib import admin

from .models import Book, Search, UserBook


class BookAdmin(admin.ModelAdmin):
    pass


class SearchAdmin(admin.ModelAdmin):
    pass


class UserBookAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(Search, SearchAdmin)
admin.site.register(UserBook, UserBookAdmin)
