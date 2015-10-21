from django.conf.urls import url, include
from cinemas import views


urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^cinemas/$', views.CinemaList.as_view(), name='cinema-list'),
    url(r'^import/cinema/$', views.import_cinemas),
    url(r'^import/showtime/$', views.get_show_times),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]