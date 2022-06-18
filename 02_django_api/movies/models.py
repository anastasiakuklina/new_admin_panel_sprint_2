import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('fullname'), db_index=True)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):

    class FilmworkTypes(models.TextChoices):
        Movie = 'movie'
        Tv_show = 'tv_show'

    title = models.TextField(_('title'), db_index=True)
    description = models.TextField(_('description'), null=True, blank=True)
    creation_date = models.DateField(_('creation_date'), null=True, db_index=True)
    rating = models.FloatField(_('rating'), null=True, blank=True,
                               validators=[MinValueValidator(0), MaxValueValidator(10)], db_index=True)
    type = models.TextField(_('type'), choices=FilmworkTypes.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _("Filmwork Genre")
        verbose_name_plural = _("Filmwork Genres")
        constraints = [
            UniqueConstraint(fields=['film_work', 'genre'], name='genre_film_work_unique_idx')
        ]


class PersonFilmwork(UUIDMixin):

    class PersonRoleTypes(models.TextChoices):
        Actor = 'actor'
        Director = 'director'
        Writer = 'writer'

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), choices=PersonRoleTypes.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _("Filmwork Person")
        verbose_name_plural = _("Filmwork Persons")
        constraints = [
            UniqueConstraint(fields=['film_work', 'person', 'role'], name='person_film_work_role_unique_idx')
        ]
