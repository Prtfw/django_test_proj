from django.test import TestCase
from tx_list.models import Tx
import time


class TxTests(TestCase):
    def setUp(self):
        Tx.objects.create(item=int(time.time()), note='test note', amt=9.09)

    def make_tx(self):
        tx = Tx.objects.create(item=int(time.time()), note='test note2', amt=9.09)
        return tx

    def test_create(self):
        tx = self.make_tx()
        all_items = Tx.objects.all().order_by('-item')
        self.assertTrue(isinstance(tx, Tx))
        self.assertTrue(len(all_items) == 2)

    def test_del(self):
        tx = self.make_tx()
        self.assertTrue(len(Tx.objects.all().order_by('-item')) == 2)
        tx.delete()
        self.assertTrue(len(Tx.objects.all().order_by('-item')) == 1)

    def test_edit(self):
        tx = self.make_tx()
        mod = Tx.objects.get(pk=tx.id)
        mod.note = "mod note"
        mod.save()
        tx = Tx.objects.get(pk=tx.id)
        self.assertTrue(tx)
        self.assertTrue(tx.note == mod.note)
