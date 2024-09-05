from django.db import models
from django.core.files.storage import FileSystemStorage

fss = FileSystemStorage(location='/media/img')


class Restaurant(models.Model):
    name = models.CharField('Name', max_length=50, null=False)
    description = models.TextField('Description', null=True)
    logo = models.ImageField('Logo', upload_to='img/', storage=fss)
    cover = models.ImageField('Cover', upload_to='img/', storage=fss)

    class Meta:
        managed = True
        db_table = 'reservations_restaurant'
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return f'{self.name}'
