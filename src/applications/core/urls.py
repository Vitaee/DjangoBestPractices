from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import  MagazaViewSet

router = DefaultRouter()
router.register(r'loc', MagazaViewSet)

urlpatterns = [
    path('/', include(router.urls)),
]