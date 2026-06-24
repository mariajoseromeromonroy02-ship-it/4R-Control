from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import date

import openpyxl

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse

from .models import Registro
from .forms import RegistroForm, UsuarioForm


@user_passes_test(lambda u: u.is_superuser)
def usuarios(request):
    lista_usuarios = User.objects.all()

    return render(
        request,
        'usuarios.html',
        {
            'usuarios': lista_usuarios
        }
    )


@login_required
def dashboard(request):

    if request.method == 'POST':

        form = RegistroForm(request.POST)

        if form.is_valid():

            registro = form.save(commit=False)
            registro.usuario = request.user

            if registro.sin_boleta:
                registro.valor = 0

            registro.save()

            return redirect('dashboard')

    else:
        form = RegistroForm()

    registros = Registro.objects.filter(
        usuario=request.user,
        eliminado=False
    )

    hoy = date.today()

    total_hoy = sum(
        r.valor
        for r in registros
        if r.fecha.date() == hoy
    )

    total_mes = sum(
        r.valor
        for r in registros
        if r.fecha.month == hoy.month
        and r.fecha.year == hoy.year
    )

    total_anio = sum(
        r.valor
        for r in registros
        if r.fecha.year == hoy.year
    )

    contexto = {
        'form': form,
        'registros': registros,
        'total_hoy': total_hoy,
        'total_mes': total_mes,
        'total_anio': total_anio,
        'cantidad_registros': registros.count(),
    }

    return render(
        request,
        'dashboard.html',
        contexto
    )


@login_required
def eliminar_registro(request, registro_id):

    registro = get_object_or_404(
        Registro,
        id=registro_id,
        usuario=request.user
    )

    registro.eliminado = True
    registro.fecha_eliminacion = timezone.now()

    registro.save()

    return redirect('dashboard')


@login_required
def papelera(request):

    registros = Registro.objects.filter(
        usuario=request.user,
        eliminado=True
    )

    return render(
        request,
        'papelera.html',
        {
            'registros': registros
        }
    )


@login_required
def restaurar_registro(request, registro_id):

    registro = get_object_or_404(
        Registro,
        id=registro_id,
        usuario=request.user
    )

    registro.eliminado = False
    registro.fecha_eliminacion = None

    registro.save()

    return redirect('papelera')


@login_required
def exportar_excel(request):

    registros = Registro.objects.filter(
        usuario=request.user,
        eliminado=False
    )

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    sheet.title = "Registros"

    sheet.append([
        "Fecha",
        "Valor",
        "Sin Boleta"
    ])

    for registro in registros:

        sheet.append([
            registro.fecha.strftime("%Y-%m-%d %H:%M"),
            float(registro.valor),
            "Sí" if registro.sin_boleta else "No"
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename="registros.xlsx"'

    workbook.save(response)

    return response


@login_required
def exportar_pdf(request):

    registros = Registro.objects.filter(
        usuario=request.user,
        eliminado=False
    )

    buffer = BytesIO()

    pdf = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elementos = []

    elementos.append(
        Paragraph(
            "REPORTE 4R CONTROL",
            styles['Title']
        )
    )

    elementos.append(
        Spacer(1, 12)
    )

    total = 0

    for registro in registros:

        total += registro.valor

        elementos.append(
            Paragraph(
                f"{registro.fecha.strftime('%d/%m/%Y %H:%M')} - ${registro.valor:,.0f}",
                styles['BodyText']
            )
        )

    elementos.append(
        Spacer(1, 20)
    )

    elementos.append(
        Paragraph(
            f"TOTAL: ${total:,.0f}",
            styles['Heading2']
        )
    )

    pdf.build(elementos)

    buffer.seek(0)

    response = HttpResponse(
        buffer,
        content_type='application/pdf'
    )

    response['Content-Disposition'] = 'attachment; filename="reporte_4r.pdf"'

    return response


@user_passes_test(lambda u: u.is_superuser)
def crear_usuario(request):

    if request.method == 'POST':

        form = UsuarioForm(request.POST)

        if form.is_valid():

            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            return redirect('usuarios')

    else:
        form = UsuarioForm()

    return render(
        request,
        'crear_usuario.html',
        {
            'form': form
        }
    )


@user_passes_test(lambda u: u.is_superuser)
def eliminar_usuario(request, usuario_id):

    usuario = get_object_or_404(
        User,
        id=usuario_id
    )

    if not usuario.is_superuser:
        usuario.delete()

    return redirect('usuarios')