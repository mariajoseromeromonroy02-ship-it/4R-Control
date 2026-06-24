from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'eliminar/<int:registro_id>/',
        views.eliminar_registro,
        name='eliminar_registro'
    ),

    path(
        'papelera/',
        views.papelera,
        name='papelera'
    ),

    path(
        'restaurar/<int:registro_id>/',
        views.restaurar_registro,
        name='restaurar_registro'
    ),

    path(
        'exportar-excel/',
        views.exportar_excel,
        name='exportar_excel'
    ),

    path(
        'exportar-pdf/',
        views.exportar_pdf,
        name='exportar_pdf'
    ),

    path(
        'usuarios/',
        views.usuarios,
        name='usuarios'
    ),

    path(
        'usuarios/crear/',
        views.crear_usuario,
        name='crear_usuario'
    ),

    path(
        'usuarios/eliminar/<int:usuario_id>/',
        views.eliminar_usuario,
        name='eliminar_usuario'
    ),

]