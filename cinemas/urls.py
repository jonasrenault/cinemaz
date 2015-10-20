from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from cinemas import views

router = DefaultRouter()
router.register(r'cinemas', views.CinemaViewSet)
router.register(r'chains', views.CinemaChainViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^import/cinema/$', views.import_cinemas),
    url(r'^import/showtime/$', views.get_show_times),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]