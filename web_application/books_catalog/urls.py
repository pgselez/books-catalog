"""books_catalog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from catalog import views
from seo.views import robots_txt_view
from django.urls import include
from rest_framework import routers
from catalog.rest import BookViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'books', BookViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include(router.urls)),
    path('summernote/', include('django_summernote.urls')),
    path('', views.IndexView.as_view(), name='index'),
    path('tag/<slug:slug>/', views.TagView.as_view(), name='tag'),
    path('search', views.SearchView.as_view(), name='search'),
    path('run-crawler', views.crawler, name='crawler'),
    path('robots.txt', robots_txt_view, name='robots_txt'),
    path('category/<slug:slug>/', views.BookListView.as_view(), name='catalog'),
    path('book/<slug:slug>/', views.BookView.as_view(), name='book'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
