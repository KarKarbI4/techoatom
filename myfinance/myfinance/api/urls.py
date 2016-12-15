from django.conf.urls import url, include

from rest_framework.routers import SimpleRouter

from api.views import ChargeViewSet, AccountViewSet, UserViewDetail

router = SimpleRouter()
router.register(r'charges', ChargeViewSet)
router.register(r'accounts', AccountViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^accounts/(?P<account_pk>\d+)/charges/$',
        ChargeViewSet.as_view({'get': 'charges'}), name='charge-list'),
    url(r'^users/(?P<user_pk>\w+)/accounts/$', AccountViewSet.as_view(
        {'get': 'accounts', 'post': 'create_account'}), name='account-list'),
    url(r'^users/(?P<pk>\w+)/$', UserViewDetail.as_view(), name='user-detail')
]
