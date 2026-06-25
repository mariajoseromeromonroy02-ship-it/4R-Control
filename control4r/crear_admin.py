from django.contrib.auth.models import User

usuario = "Maria"
correo = "admin@4rcontrol.com"
clave = "12345678"

if not User.objects.filter(username=usuario).exists():
    User.objects.create_superuser(
        username=usuario,
        email=correo,
        password=clave
    )
    print("Superusuario creado")
else:
    print("Superusuario ya existe")
