"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

# from articles.views import article_home_view
from articles.views import(
    article_detail_view,
    article_search_view,
    article_create_view,
        )


app_name = "articles"
urlpatterns = [
    path("", article_search_view, name="search"),
    path("create/", article_create_view, name="create"),
    path("<slug:slug>/", article_detail_view, name="detail"),
     # The name parameter sets the name of the view
]
