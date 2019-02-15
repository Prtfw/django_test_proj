from django.db import models

class Tx(models.Model):
	item = models.CharField(max_length=200)
	completed = models.BooleanField(default=False)
	note = models.CharField(max_length=200,  default='')

	def __str__(self):
		return self.item + ' | '  + self.note  + ' | ' +  str(self.completed)
