from django.test import TestCase
from django.core.files import File
from main.models import Usuario, Comida, Favoritos, Imagen, Transacciones
import sure
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
        Usuario.objects.create(
            id=1,
            nombre='Estudiante',
            email='a@a',
            tipo=1,
            avatar=im,
            contraseña='asd1234')
        Usuario.objects.create(
            id=2,
            nombre='VendedorFijo',
            email='s@s',
            tipo=2,
            avatar=im,
            contraseña='asd1234',
            formasDePago='0,1,2,3',
            horarioIni='11:12',
            horarioFin='12:12')

    def test_attrs(self):
        estudiante = Usuario.objects.get(id=1)
        vendedor_fijo = Usuario.objects.get(id=2)

        estudiante.nombre.should.equal('Estudiante')
        vendedor_fijo.nombre.should.equal('VendedorFijo')

        estudiante.email.should.equal('a@a')
        vendedor_fijo.email.should.equal('s@s')

        estudiante.tipo.should.equal(1)
        vendedor_fijo.tipo.should.equal(2)

        #estudiante.avatar.should.be.empty
        #vendedor_fijo.avatar.should.be.empty

        vendedor_fijo.formasDePago.should.equal(['0', '1', '2', '3'])

        vendedor_fijo.horarioIni.should.equal('11:12')

        vendedor_fijo.horarioFin.should.equal('12:12')

    def test_str(self):
        estudiante = Usuario.objects.get(id=1)
        vendedor = Usuario.objects.get(id=2)

        str(estudiante).should.equal('Estudiante')
        str(vendedor).should.equal('VendedorFijo')


class ComidaTestCase(TestCase):
    def setUp(self):
        im = mock_image((200, 200))
        Usuario.objects.create(
            id=1,
            nombre="vendedor",
            email="a@a",
            tipo=2,
            avatar=im,
            contraseña='asd1234',
            formasDePago='0,1,2,3',
            horarioIni='11:12',
            horarioFin='12:12')

        Comida.objects.create(
            id=1,
            idVendedor=1,
            nombre="pasta con carne",
            categorias='10',
            descripcion='desc pasta con carne',
            stock=10,
            precio=200,
            imagen=im)

    def test_attrs(self):
        pasta = Comida.objects.get(id=1)

        pasta.name.should.equal('pasta con carne')
        pasta.idVendedor.should.equal(1)
        pasta.categorias.should.equal([10])
        pasta.descripcion.should.equal('desc pasta con carne')
        pasta.stock.should.equal(10)
        pasta.precio.should.equal(200)

        Usuario.objects.get(
            id=pasta.idVendedor).nombre.should.equal('vendedor')


    def test_str(self):
        pasta = Comida.objects.get(id=1)

        str(pasta).should.equal('pasta con carne')


class FavoritosTestCase(TestCase):
    def setUp(self):
        Favoritos.objects.create(
            id=1,
            idAlumno=1,
            idVendedor=2)

        im = mock_image((200, 200))

        Usuario.objects.create(
            id=1,
            nombre='Estudiante',
            email='a@a',
            tipo=1,
            avatar=im,
            contraseña='asd1234')

        Usuario.objects.create(
            id=2,
            nombre='VendedorFijo',
            email='s@s',
            tipo=2,
            avatar=im,
            contraseña='asd1234',
            formasDePago='0,1,2,3',
            horarioIni='11:12',
            horarioFin='12:12')

    def test_attrs(self):
        fav = Favoritos.objects.get(id=1)

        fav.idAlumno.should.equal(1)
        fav.idVendedor.should.equal(2)


    def test_str(self):
        fav = Favoritos.objects.get(id=1)

        str(fav).should.equal('Estudiante -> VendedorFijo')


class ImagenTestCase(TestCase):
    def setUp(self):
        im = mock_image((200, 200))
        Imagen.objects.create(id=1, imagen=im)


    def test_str(self):
        im = Imagen.objects.get(id=1)

        str(im).should.equal('1')


class TransaccionesTestCase(TestCase):
    def setUp(self):
        Transacciones.objects.create(
            idTransaccion=1,
            idComida=1,
            idVendedor=2,
            fecha='01/02/2003 17:12')

        Usuario.objects.create(
            id=2,
            nombre='VendedorFijo',
            email='s@s',
            tipo=2,
            avatar=im,
            contraseña='asd1234',
            formasDePago='0,1,2,3',
            horarioIni='11:12',
            horarioFin='12:12')

        Comida.objects.create(
            id=1,
            idVendedor=1,
            nombre="pasta con carne",
            categorias='10',
            descripcion='desc pasta con carne',
            stock=10,
            precio=200,
            imagen=im)


    def test_str(self):
        trans = Transacciones.objects.get(id=1)

        str(trans).should.equal('1')
