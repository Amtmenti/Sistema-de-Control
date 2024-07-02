from django.urls import path
from core.pos.views.alumno.views import *
from core.pos.views.horario.views import *
from core.pos.views.registroentrada.views import *
from core.pos.views.registrosalida.views import *
from core.pos.views.actividad.views import *
from core.pos.views.registrocombinado.views import *

urlpatterns = [
    path('alumno/', AlumnoListView.as_view(), name='alumno_list'),
    path('alumno/add/', AlumnoCreateView.as_view(), name='alumno_create'),
    path('alumno/update/<int:pk>/', AlumnoUpdateView.as_view(), name='alumno_update'),
    path('alumno/delete/<int:pk>/', AlumnoDeleteView.as_view(), name='alumno_delete'),

    path('horario/', HorarioListView.as_view(), name='horario_list'),
    path('horario/add/', HorarioCreateView.as_view(), name='horario_create'),
    path('horario/update/<int:pk>/', HorarioUpdateView.as_view(), name='horario_update'),
    path('horario/delete/<int:pk>/', HorarioDeleteView.as_view(), name='horario_delete'),

    path('registroentrada/', RegistroEntradaListView.as_view(), name='registroentrada_list'),
    path('registroentrada/add/', RegistroEntradaCreateView.as_view(), name='registroentrada_create'),
    path('registroentrada/update/<int:pk>/', RegistroEntradaUpdateView.as_view(), name='registroentrada_update'),
    path('registroentrada/delete/<int:pk>/', RegistroEntradaDeleteView.as_view(), name='registroentrada_delete'),

    path('registrosalida/', RegistroSalidaListView.as_view(), name='registrosalida_list'),
    path('registrosalida/add/', RegistroSalidaCreateView.as_view(), name='registrosalida_create'),
    path('registrosalida/update/<int:pk>/', RegistroSalidaUpdateView.as_view(), name='registrosalida_update'),
    path('registrosalida/delete/<int:pk>/', RegistroSalidaDeleteView.as_view(), name='registrosalida_delete'),

    path('actividad/', ActividadListView.as_view(), name='actividad_list'),
    path('actividad/add/', ActividadCreateView.as_view(), name='actividad_create'),
    path('actividad/update/<int:pk>/', ActividadUpdateView.as_view(), name='actividad_update'),
    path('actividad/delete/<int:pk>/', ActividadDeleteView.as_view(), name='actividad_delete'),

    path('registrocombinado/', RegistroEntradaSalidaListView.as_view(), name='registro_entrada_salida_list'),
    path('registrocombinado/add/', RegistroEntradaSalidaCreateView.as_view(), name='registro_entrada_salida_create'),
]
