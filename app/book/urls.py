from rest_framework.routers import SimpleRouter

from book import views

router = SimpleRouter()
router.register('books', views.BookViewSet)
router.register('', views.BookUpdateViewSet, basename='db')

app_name = 'book'

urlpatterns = router.urls
