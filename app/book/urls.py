from django.urls import path, include
from rest_framework.routers import DefaultRouter

from book import views

router = DefaultRouter()
router.register('books', views.BookViewSet)

app_name = 'book'

urlpatterns = [
    path('', include(router.urls)),
    path('db/', views.BookViewSet.as_view({'post': 'create'}), name='db')
]
