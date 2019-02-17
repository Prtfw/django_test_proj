from django.db import models

class Tx(models.Model):
	item = models.IntegerField()
	amt = models.FloatField(default=False)
	note = models.CharField(max_length=200,  default='')

	def __str__(self):
		return  str(self.item) + ' | '  + self.note  + ' | ' +  str(self.amt)

	def _create(self, **kwargs):
		obj = self.model(**kwargs)
		self._for_write = True
		print(**kwargs)
		obj.save(force_insert=True, using=self.db)
		return obj
