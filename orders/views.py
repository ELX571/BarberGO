from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from base.permissions import IsBarber, IsCustomer
from notifications.models import Notifications
from notifications.views import notify_user
from orders.models import Order
from orders.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ('accept', 'cancel'):
            return [permission() for permission in (IsAuthenticated, IsBarber)]
        if self.action == 'create':
            return [permission() for permission in (IsAuthenticated, IsCustomer)]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Order.objects.filter(customer=user)
        if user.role == 'barber':
            return Order.objects.filter(barber=user)
        return Order.objects.none()

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def _notify_customer(self, order, new_status):
        barber_name = (
            order.barber.get_full_name().strip()
            or order.barber.first_name.strip()
            or order.barber.username
        )
        action_text = 'accept qildi' if new_status == Order.Status.ACCEPTED else 'cancel qildi'
        message = f'{barber_name} sizning orderingizni {action_text}'

        Notifications.objects.create(
            title='Order statusi o\'zgardi',
            description=message,
            receptions=order.customer,
        )
        notify_user(order.customer.id, message)
        return message

    def _change_status(self, request, new_status):
        order = self.get_object()

        if order.barber != request.user:
            return Response(
                'Siz bu orderga tegishli emassiz',
                status=status.HTTP_403_FORBIDDEN
            )

        if order.status != Order.Status.PENDING:
            return Response(
                'Siz bu orderni o\'zgartira olmaysiz',
                status=status.HTTP_403_FORBIDDEN
            )

        order.status = new_status
        order.save(update_fields=['status', 'updated_at'])
        message = self._notify_customer(order, new_status)

        return Response(
            {
                'detail': message,
                'order_id': order.id,
                'status': order.status,
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['patch'], url_path='accept')
    def accept(self, request, *args, **kwargs):
        return self._change_status(request, Order.Status.ACCEPTED)

    @action(detail=True, methods=['patch'], url_path='cancel')
    def cancel(self, request, *args, **kwargs):
        return self._change_status(request, Order.Status.CANCELED)
