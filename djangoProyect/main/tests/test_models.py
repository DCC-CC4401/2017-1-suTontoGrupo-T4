from django.contrib.auth.models import User
from django.test import TestCase
from django.core.files import File
import sure
from main.models import Usuario, Comida, Favoritos, Imagen, Transacciones
from PIL import Image
from io import BytesIO


def mock_image(size):
    """
    Crea una imagen de tamano size en memoria para testear con los modelos
    @param size: tuple
    @returns: BytesIO file
    """
    file = BytesIO()
    image = Image.new('RGBA', size=size, color=(255, 255, 255))
    image.save(file, 'png')
    file.seek(0)
    return File(file)


class UsuarioTestCase(TestCase):
    def setUp(self):
        im = mock_image((200, 200))
        user1 = User(email='a@a', username='a@a')
        user1.set_password('asd1234')
        user2 = User(email='s@s', username='s@s')
        user2.set_password('asd1234')
        user1.save()
        user2.save()
        Usuario.objects.create(
            info=user1,
            nombre='Estudiante',
            tipo=1,
            avatar=im, )
        Usuario.objects.create(
            info=user2,
            nombre='VendedorFijo',
            tipo=2,
            avatar=im,
            formasDePago='0,1,2,3',
            horarioIni='11:12',
            horarioFin='12:12')

    def test_attrs(self):
        estudiante = Usuario.objects.get(info_id=1)
        vendedor_fijo = Usuario.objects.get(info_id=2)

        estudiante.nombre.should.equal('Estudiante')
        vendedor_fijo.nombre.should.equal('VendedorFijo')

        estudiante.info.email.should.equal('a@a')
        vendedor_fijo.info.email.should.equal('s@s')

        estudiante.tipo.should.equal(1)
        vendedor_fijo.tipo.should.equal(2)

        # estudiante.avatar.should.be.empty
        # vendedor_fijo.avatar.should.be.empty

        vendedor_fijo.formasDePago.should.equal(['0', '1', '2', '3'])

        vendedor_fijo.horarioIni.should.equal('11:12')

        vendedor_fijo.horarioFin.should.equal('12:12')

    def test_str(self):
        estudiante = Usuario.objects.get(info_id=1)
        vendedor = Usuario.objects.get(info_id=2)

        str(estudiante).should.equal('Estudiante')
        str(vendedor).should.equal('VendedorFijo')


class ComidaTestCase(TestCase):
    def setUp(self):
        im = mock_image((200, 200))
        user1 = User(email='a@a', username='a@a')
        user1.set_password('asd1234')
        user1.save()
        user = Usuario(
            info=user1,
            nombre="vendedor",
            tipo=2,
            avatar=im,
            formasDePago='0,1,2,3',
            horarioIni='11:12',
            horarioFin='12:12')
        user.save()
        Comida.objects.create(
            idComida=1,
            idVendedor=user1,
            nombre="pasta con carne",
            categorias='10',
            descripcion='desc pasta con carne',
            stock=10,
            precio=200,
            imagen=im)

    def test_attrs(self):
        pasta = Comida.objects.get(idComida=1)

        pasta.nombre.should.equal('pasta con carne')
        pasta.idVendedor.id.should.equal(1)
        pasta.categorias.should.equal(['10'])
        pasta.descripcion.should.equal('desc pasta con carne')
        pasta.stock.should.equal(10)
        pasta.precio.should.equal(200)

        Usuario.objects.get(
            info_id=pasta.idVendedor).nombre.should.equal('vendedor')

    def test_str(self):
        pasta = Comida.objects.get(idComida=1)

        str(pasta).should.equal('pasta con carne')


class FavoritosTestCase(TestCase):
    def setUp(self):
        im = mock_image((200, 200))
        user1 = User(email='a@a', username='a@a')
        user1.set_password('asd1234')
        user2 = User(email='s@s', username='s@s')
        user2.set_password('asd1234')
        user1.save()
        user2.save()
        estudiante = Usuario(
            info=user1,
            nombre='Estudiante',
            tipo=1,
            avatar=im, )
        estudiante.save()
        vendedor = Usuario(
            info=user2,
            nombre='VendedorFijo',
            tipo=2,
            avatar=im,
            formasDePago='0,1,2,3',
            horarioIni='11:12',
            horarioFin='12:12')
        vendedor.save()
        Favoritos.objects.create(
            id=1,
            idAlumno=estudiante,
            idVendedor=vendedor)


    def test_attrs(self):
        fav = Favoritos.objects.get(id=1)

        fav.idAlumno.info.id.should.equal(1)
        fav.idVendedor.info.id.should.equal(2)




class TransaccionesTestCase(TestCase):
    def setUp(self):
        im = mock_image((200, 200))
        user1 = User(email='a@a', username='a@a')
        user1.set_password('asd1234')
        user1.save()

        Transacciones.objects.create(
            idTransaccion=1,
            nombreComida='lasagna',
            idVendedor=user1,
            fecha='01/02/2003 17:12',
            precio=2000,)

        Comida.objects.create(
            idComida=1,
            idVendedor=user1,
            nombre="pasta con carne",
            categorias='10',
            descripcion='desc pasta con carne',
            stock=10,
            precio=200,
            imagen=im)

    def test_str(self):
        trans = Transacciones.objects.get(idTransaccion=1)

        str(trans).should.equal('1')
