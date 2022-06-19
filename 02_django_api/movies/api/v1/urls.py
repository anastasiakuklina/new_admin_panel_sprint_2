from django.urls import path

from movies.api.v1.views import MovieDetailApi, MovieListApi

urlpatterns = [
    path('movies/', MovieListApi.as_view()),
    path('movies/<uuid:pk>/', MovieDetailApi.as_view())
]
