from django.test import TestCase
from .models import Conta
from datetime import date

class ModelTesting(TestCase):

    def setUp(self):
        self.conta = Conta.objects.create(
            nome='django',
            cpf=98665141022,
            email='example@example.com',
            senha='senha123',
            numCartao=1234567812345678,
            nomeCartao='Django Teste',
            cvv=123,
            val_cartao=date(2025, 12, 31),
            aceite=True,
            valor_plano=100
        )

    def test_post_model(self):
        d = self.conta
        self.assertTrue(isinstance(d, Conta))
        self.assertEqual(d.nome, 'django')