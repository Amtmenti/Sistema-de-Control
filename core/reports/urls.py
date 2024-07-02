from django.urls import path
from core.reports.views.alumno_report.views import AlumnoReportView

urlpatterns = [
    path('alumno/', AlumnoReportView.as_view(), name='alumno_report'),
]
