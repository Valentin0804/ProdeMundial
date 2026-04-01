from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    avatar = models.ImageField(upload_to='avatares/', null=True, blank=True)
    bio = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username


class GrupoPrivado(models.Model):
    nombre = models.CharField(max_length=100)
    codigo_invitacion = models.CharField(max_length=8, unique=True)
    admin = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='grupos_admin'
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Grupo privado'
        verbose_name_plural = 'Grupos privados'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.codigo_invitacion:
            import random, string
            self.codigo_invitacion = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=8)
            )
        super().save(*args, **kwargs)


class Miembro(models.Model):
    grupo = models.ForeignKey(
        GrupoPrivado, on_delete=models.CASCADE, related_name='miembros'
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='membresías'
    )
    fecha_union = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('grupo', 'usuario')
        verbose_name = 'Miembro'
        verbose_name_plural = 'Miembros'

    def __str__(self):
        return f'{self.usuario} en {self.grupo}'
