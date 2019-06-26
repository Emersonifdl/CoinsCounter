from django.db import models
from django.utils import timezone
from decimal import Decimal


def dec2reais(valor_decimal):
    tmp = '{:20,.2f}'.format(valor_decimal)
    tmp = tmp.replace('.', '@').replace(',', '.').replace('@', ',')
    return 'R$ {}'.format(tmp)


class Local(models.Model):
    descricao = models.CharField(max_length=50)

    def __str__(self):
        return self.descricao


class Cofre(models.Model):
    token = models.CharField(max_length=32, primary_key=True)
    nome = models.CharField(max_length=50)
    saldo = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name='Saldo', default=0.0,
        help_text='Saldo do Cofre.',
        blank=False, null=False,
    )
    local = models.ForeignKey(
        Local, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nome


class Transacao(models.Model):
    cofre = models.ForeignKey(Cofre, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(default=timezone.now)
    valor = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name='Valor', default=0.0,
        help_text='Valor da Transação.',
        blank=False, null=False,
    )
