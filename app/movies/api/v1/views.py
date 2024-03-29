from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from ...models import Filmwork, PersonFilmwork


class MovieApiMixin:
    model = Filmwork

    def get_queryset(self):
        queryset = self.model.objects.values('id', 'title', 'description', 'creation_date', 'rating', 'type').annotate(
            genres=ArrayAgg('genres__name', distinct=True))

        for person_type in PersonFilmwork.PersonRoleTypes:

            queryset = queryset.annotate(
                **{person_type + 's': ArrayAgg('persons__full_name', filter=Q(personfilmwork__role=person_type),
                                               distinct=True)}
            )
        return queryset

    def render_to_response(self, context, *response_kwargs):
        return JsonResponse(context)


class MovieListApi(MovieApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, is_paginated = self.paginate_queryset(self.get_queryset(), self.paginate_by)
        prev_ind = page.previous_page_number() if page.has_previous() else None
        next_ind = page.next_page_number() if page.has_next() else None
        return {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": prev_ind,
            "next": next_ind,
            "results": list(queryset)
        }


class MovieDetailApi(MovieApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return self.get_queryset().filter(pk=pk).first()
