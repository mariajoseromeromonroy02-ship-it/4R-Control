from django.db import models
from django.contrib.auth.models import User


class Registro(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    sin_boleta = models.BooleanField(
        default=False
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    eliminado = models.BooleanField(
        default=False
    )

    fecha_eliminacion = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.valor}"