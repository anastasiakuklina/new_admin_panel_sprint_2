from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name', )


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ('genre',)
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('genre')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name', )


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',)
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('person')


@admin.register(Filmwork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline,)

    list_display = ('title', 'type', 'creation_date', 'rating', )
    list_filter = ('type', )
    search_fields = ('title', 'description', 'id',)
