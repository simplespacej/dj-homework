from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Advertisement
from .serializers import AdvertisementSerializer
from .permissions import IsOwnerOrReadOnly  # Импортируйте ваш класс разрешений здесь

class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def get_permissions(self):
        """
        Предоставляет различные разрешения в зависимости от типа запроса.
        """
        if self.action in ["create"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Автоматически присваивает текущего пользователя в качестве создателя объявления.
        """
        serializer.save(creator=self.request.user)
