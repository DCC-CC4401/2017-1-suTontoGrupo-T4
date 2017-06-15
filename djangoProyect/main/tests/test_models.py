from django.test import TestCase
from main.models import Usuario, Comida, Favoritos, Imagen, Transacciones

class UsuarioTestCase (TestCase):
    def setUp(self):
        Usuario.objects.create(id=1,
                               nombre="Estudiante",
                               email="a@a",
                               tipo=1,
                               avatar='',
                               contraseña='asd1234')
        Usuario.objects.create(id=2,
                               nombre="VendedorFijo",
                               email="s@s",
                               tipo=2,
                               avatar='',
                               contraseña='asd1234',
                               formasDePago='0,1,2,3',
                               horarioIni='11:12',
                               horarioFin='12:12')

    def test_names(self):
        estudiante = Usuario.objects.get(id=1)
        vendedor_fijo = Usuario.objects.get(id=2)

        self.assertEquals(str(estudiante), "Estudiante")
        self.assertEquals(str(vendedor_fijo), "VendedorFijo")
