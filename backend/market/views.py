from rest_framework import viewsets, permissions
from .models import CryptoToken, Holding, Order, Trade
from .serializers import CryptoTokenSerializer, HoldingSerializer, OrderSerializer, TradeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class CryptoTokenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CryptoToken.objects.all()
    serializer_class = CryptoTokenSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class HoldingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HoldingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Holding.objects.filter(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, remaining=serializer.validated_data['quantity'], status='open')

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status == 'open':
            order.status = 'cancelled'
            order.save()
            return Response({'status': 'order cancelled'})
        return Response({'status': 'cannot cancel'}, status=400)

class TradeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_orders = Order.objects.filter(user=self.request.user)
        return Trade.objects.filter(buy_order__in=user_orders) | Trade.objects.filter(sell_order__in=user_orders)
