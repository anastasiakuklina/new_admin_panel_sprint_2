from django.urls import path

from movies.api.v1.views import MovieListApi

urlpatterns = [
    path('movies/', MovieListApi.as_view())
]
