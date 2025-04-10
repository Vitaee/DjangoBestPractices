from django.http import HttpResponse
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Magaza
from .serializers import MagazaSerializer
from .permissions import IsOwnerOrReadOnly
from .tasks import notify_magaza_change
import asyncio


class MagazaViewSet(viewsets.ModelViewSet):
    queryset = Magaza.objects.all()
    serializer_class = MagazaSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['active', 'owner']
    search_fields = ['ad']
    ordering_fields = ['created_at', 'ad']
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        # Trigger Celery task after creation
        notify_magaza_change.delay(
            magaza_id=serializer.instance.id,
            action="created",
            user_id=self.request.user.id
        )
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        magaza = self.get_object()
        magaza.active = False
        magaza.save()
        notify_magaza_change.delay(
            magaza_id=magaza.id,
            action="deactivated",
            user_id=request.user.id
        )
        return Response({'status': 'deactivated'})
    
    @action(detail=False)
    async def nearby(self, request):
        """Async method to find nearby stores based on provided coordinates"""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        
        if not lat or not lng:
            return Response({"error": "Latitude and longitude required"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Use async query
        nearby_stores = await self.get_nearby_stores(float(lat), float(lng))
        serializer = self.get_serializer(nearby_stores, many=True)
        return Response(serializer.data)
    
    async def get_nearby_stores(self, lat, lng):
        """Async method to get nearby stores"""
        from django.contrib.gis.geos import Point
        from django.contrib.gis.db.models.functions import Distance
        
        user_location = Point(lng, lat, srid=4326)
        
        # Simulating async operation
        await asyncio.sleep(0.1)  # Simulate async delay
        
        # This would use proper async ORM in production
        return list(Magaza.objects.filter(active=True, location__isnull=False)
                   .annotate(distance=Distance('location', user_location))
                   .order_by('distance')[:10])