import datetime

from django.contrib.auth.models import User
from django.db import models
from multiselectfield import MultiSelectField
from django.utils import timezone
from django.utils.formats import get_format


# Create your models here

class Usuario(models.Model):
    info = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, )
    nombre = models.CharField(max_length=200)
    #email = models.CharField(max_length=200)
    tipos = ((0, 'admin'), (1, 'alumno'), (2, 'fijo'), (3, 'ambulante'))
    tipo = models.IntegerField(choices=tipos)
    avatar = models.ImageField(upload_to='avatars')
    #contraseña = models.CharField(max_length=200)
    activo = models.BooleanField(default=False, blank=True)
    litaFormasDePago = (
        (0, 'Efectivo'),
        (1, 'Tarjeta de Crédito'),
        (2, 'Tarjeta de Débito'),
        (3, 'Tarjeta Junaeb'),
    )
    formasDePago = MultiSelectField(choices=litaFormasDePago, null=True, blank=True)
    horarioIni = models.CharField(max_length=200, blank=True, null=True)
    horarioFin = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'usuario'

    def actualizar(self):
        if self.tipo == 2:
            hi = self.horarioIni
            hf = self.horarioFin
            horai = hi[:2]
            horaf = hf[:2]
            mini = hi[3:5]
            minf = hf[3:5]

            tiempo = str(datetime.datetime.now().time())

            hora = tiempo[:2]
            minutos = tiempo[3:5]
            estado = ""
            if horaf >= hora and hora >= horai:
                if horai == hora:
                    if minf >= minutos and minutos >= mini:
                        estado = "activo"
                    else:
                        estado = "inactivo"
                elif horaf == hora:
                    if minf >= minutos and minutos >= mini:
                        estado = "activo"
                    else:
                        estado = "inactivo"
                else:
                    estado = "activo"
            else:
                estado = "inactivo"
            if estado == "activo":
                Usuario.objects.filter(nombre=self.nombre).update(activo=1)
            else:
                Usuario.objects.filter(nombre=self.nombre).update(activo=0)
    def informaciones(self):
        datosUsuarios=[]
        datosUsuarios.append(self.info.id)
        datosUsuarios.append(self.nombre)
        datosUsuarios.append(self.email)
        datosUsuarios.append(self.tipo)
        datosUsuarios.append(str(self.avatar))
        datosUsuarios.append(self.activo)
        datosUsuarios.append(self.formasDePago)
        datosUsuarios.append(self.horarioIni)
        datosUsuarios.append(self.horarioFin)
        datosUsuarios.append(self.contraseña)
        return datosUsuarios


class Comida(models.Model):
    idComida = models.AutoField(primary_key=True)
    idVendedor = models.ForeignKey(User, on_delete=models.CASCADE,
                               primary_key=False, )
    nombre = models.CharField(max_length=200, primary_key=False)
    listaCategorias = (
        (0, 'Cerdo'),
        (1, 'Chino'),
        (2, 'Completos'),
        (3, 'Egipcio'),
        (4, 'Empanadas'),
        (5, 'Ensalada'),
        (6, 'Japones'),
        (7, 'Pan'),
        (8, 'Papas fritas'),
        (9, 'Pasta'),
        (10, 'Pescado'),
        (11, 'Pollo'),
        (12, 'Postres'),
        (13, 'Sushi'),
        (14, 'Vacuno'),
        (15, 'Vegano'),
        (16, 'Vegetariano'),
    )
    categorias = MultiSelectField(choices=listaCategorias, primary_key=False)
    descripcion = models.CharField(max_length=500, primary_key=False)
    stock = models.PositiveSmallIntegerField(default=0,primary_key=False)
    precio = models.PositiveSmallIntegerField(default=0,primary_key=False)
    imagen = models.ImageField(upload_to="productos")

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Comida'

    def info(self):
        listaDeProductos = []
        listaDeProductos.append(self.nombre)
        categoria = str(self.categorias)
        listaDeProductos.append(categoria)
        listaDeProductos.append(self.stock)
        listaDeProductos.append(self.precio)
        listaDeProductos.append(self.descripcion)
        listaDeProductos.append(str(self.imagen))
        return listaDeProductos


class Favoritos(models.Model):
    idAlumno = models.ForeignKey(Usuario,
                                    related_name="id_alumno",
                                    on_delete=models.CASCADE,
                                    primary_key=False, )
    idVendedor = models.ForeignKey(Usuario,
                                      related_name="id_vendedor",
                                      on_delete=models.CASCADE,
                                      primary_key=False, )

    def __str__(self):
        return str(self.idAlumno)

    class Meta:
        db_table = 'Favoritos'


class Imagen(models.Model):
    imagen = models.ImageField(upload_to='avatars')

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'imagen'


class Transacciones(models.Model):
    my_formats = get_format('DATETIME_INPUT_FORMATS')
    idTransaccion = models.AutoField(primary_key=True)
    nombreComida = models.CharField(max_length=200, blank=True, null=True)
    idVendedor = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=False, )
    precio = models.IntegerField()
    fechaAhora = str(timezone.now()).split(' ', 1)[0]
    fecha = models.CharField(max_length=200, default=fechaAhora)

    def __str__(self):
        return str(self.idTransaccion)

    class Meta:
        db_table = 'transacciones'
