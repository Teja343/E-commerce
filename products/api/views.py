from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from products.models import Product, Category, Cart, CartItem, OrderItem,Order
from .serializers import (
    ProductSerializer, CategorySerializer,
    CartSerializer, CartItemSerializer,
    OrderSerializer
)
from rest_framework import permissions

class IsAdminOrCreatorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_staff
            or obj.created_by == request.user
        )

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrCreatorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order, product=item.product, quantity=item.quantity
            )
        cart.items.all().delete()