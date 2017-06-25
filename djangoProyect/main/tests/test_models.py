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
            nombre="Estudiante",
            email="a@a",
            tipo=1,
            avatar=im,
            contraseña='asd1234')
        Usuario.objects.create(
            id=2,
            nombre="VendedorFijo",
            email="s@s",
            tipo=2,
            avatar=im,
            contraseña='asd1234',
            formasDePago='0,1,2,3',
            horarioIni='11:12',
            horarioFin='12:12')

    def test_attrs(self):
        estudiante = Usuario.objects.get(id=1)
        vendedor_fijo = Usuario.objects.get(id=2)

        str(estudiante).should.equal("Estudiante")
        str(vendedor_fijo).should.equal("VendedorFijo")

        estudiante.email.should.equal("a@a")
        vendedor_fijo.email.should.equal("s@s")

        estudiante.tipo.should.equal(1)
        vendedor_fijo.tipo.should.equal(2)

        #estudiante.avatar.should.be.empty
        #vendedor_fijo.avatar.should.be.empty

        vendedor_fijo.formasDePago.should.equal(['0', '1', '2', '3'])

        vendedor_fijo.horarioIni.should.equal('11:12')

        vendedor_fijo.horarioFin.should.equal('12:12')


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

        str(pasta).should.equal('pasta con carne')
        pasta.idVendedor.should.equal(1)
        pasta.categorias.should.equal([10])
        pasta.descripcion.should.equal('desc pasta con carne')
        pasta.stock.should.equal(10)
        pasta.precio.should.equal(200)

        Usuario.objects.get(
            id=pasta.idVendedor).nombre.should.equal('vendedor')
