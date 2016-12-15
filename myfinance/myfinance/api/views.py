
from django.shortcuts import get_list_or_404, get_object_or_404, render

from api.serializers import AccountSerializer, ChargeSerializer, UserSerializer
from finance.models import Account, Charge, User
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.settings import api_settings


# Create your views here.

class AccountOwnerOrAdmin(permissions.BasePermission):
    message = 'Account view is not allowed.'

    def has_object_permission(self, request, view, obj):
        return (obj.owner == request.user) or request.user.is_staff


class ChargeOwnerOrAdmin(permissions.BasePermission):
    message = 'Charge view is not allowed.'

    def has_object_permission(self, request, view, obj):
        return (obj.account.owner == request.user) or request.user.is_staff


class ChargeViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
    permission_classes = [permissions.IsAuthenticated, ChargeOwnerOrAdmin]
    def charges(self, request, account_pk=None):
        account = get_object_or_404(Account, id=account_pk)
        charges = get_list_or_404(Charge, account=account)
        serializer = ChargeSerializer(charges, many=True)
        return Response(serializer.data)


class AccountViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, AccountOwnerOrAdmin]

    def accounts(self, request, user_pk=None):
        user = get_object_or_404(User, username=user_pk)
        accounts = get_list_or_404(Account, owner=user)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def create_account(self, request, user_pk=None):
        data = {
            'card_num': request.data['card_num'],
            'name': request.data['name'],
            'total': request.data['total'],
        }
        user = get_object_or_404(
            User, username=user_pk) if user_pk else request.user
        data['owner'] = {'username': user.username, 'email': user.email,
                         'phone_number': user.phone_number, 'address': user.address}
        serializer = AccountSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @detail_route(methods=["get"])
    def stat(self, request, pk=None):
        account = get_object_or_404(Account, pk=pk)
        charges = Charge.objects.filter(account=account)
        hist_values = Account.get_hist_data(charges)
        hist_data = [['Month', 'Total']] + hist_values
        return Response(hist_data)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}


class UserViewDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        kwargs['pk'] = self.get_pk(request, **kwargs)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        kwargs['pk'] = self.get_pk(request, **kwargs)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['pk'] = self.get_pk(request, **kwargs)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_pk(self, request, **kwargs):
        return kwargs.get('pk', request.user.username)
