from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from web.views import DashboardView, LoginView, LogoutView, \
    TransacaoViewSet, CadastrarLocalView, ListarLocalView, \
    DeletarLocalView, CadastrarCofreView, ListarCofreView, \
    DeletarCofreView, ListarTransacaoView, DetalharCofreView,\
    DetalharLocalView, RecolherCofreView


router = routers.DefaultRouter()
router.register(r'transacoes', TransacaoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),

    path('', DashboardView.as_view(), name='dashboard'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Local
    path('cadastrar/local/', CadastrarLocalView.as_view(), name='cadastrar_local'),
    path('listar/local/', ListarLocalView.as_view(), name='listar_locais'),
    path('deletar/local/<int:id>', DeletarLocalView.as_view(), name='deletar_local'),
    path('detalhes/local/<int:id>', DetalharLocalView.as_view(), name='detalhes_local'),

    # Cofre
    path('cadastrar/cofre/', CadastrarCofreView.as_view(), name='cadastrar_cofre'),
    path('listar/cofre/', ListarCofreView.as_view(), name='listar_cofres'),
    path('deletar/cofre/<str:token>', DeletarCofreView.as_view(), name='deletar_cofre'),
    path('detalhes/cofre/<str:token>', DetalharCofreView.as_view(), name='detalhes_cofre'),
    path('recolher/cofre/<str:token>', RecolherCofreView.as_view(), name='recolher_cofre'),

    # Transacão
    path('listar/transacoes/', ListarTransacaoView.as_view(), name='listar_transacoes'),
    # path('read/devices/', ReadDevicesView.as_view(), name='read_devices'),
    # path('update/device/<str:token>/', UpdateDeviceView.as_view(), name='update_device'),
    # path('delete/device/<str:token>/', DeleteDeviceView.as_view(), name='delete_device'),

    # Sensor
    # path('update/sensor/<int:id>/', AjaxUpdateSensorView.as_view(), name='sensor_update'),
    # path('delete/sensor/<int:id>/', DeleteSensorView.as_view(), name='sensor_delete'),
    # path('sensor/table/<int:id>/', TableSensorView.as_view(), name='sensor_table'),
    # path('sensor/chart/<int:id>/', ChartSensorView.as_view(), name='sensor_chart'),
    # path('update/device/<str:token>/add/sensor/', CreateSensorView.as_view(), name='sensor_create'),
    path('api-auth/', include('rest_framework.urls')),

    # Transacao
    # path('ajax/event/', AjaxEventsView.as_view(), name='ajax_event'),
    # path('json/read/events/', json_read_events, name='json_read_events'),
    # path('json/create/events/', json_create_events, name='json_read_events'),
]

