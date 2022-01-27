from django.urls import path
from test_wallet_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start-test-data', views.start_test_data, name='start_test_data'),
    path('api/v1/init', views.api_v1_init, name='api_v1_init'),
    path('api/v1/wallet/deposits', views.api_v1_wallet_deposits, name='api_v1_wallet_deposits'),
    path('api/v1/wallet/withdrawals', views.api_v1_wallet_withdrawals, name='api_v1_wallet_withdrawals'),
    path('api/v1/wallet', views.api_v1_wallet, name='api_v1_wallet'),

]
