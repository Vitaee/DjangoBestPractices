from django.urls import path, include
from django.conf.urls.static import static
from .views import test_view


urlpatterns = [
    path('/', test_view),
]