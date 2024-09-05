from django.db import models
from .customer import Customer


class Rating(models.Model):

    customer = models.ForeignKey(
        Customer, related_name='ratings', on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField('Rating')
    opinion = models.TextField('Opinion', blank=True)

    class Meta:
        managed = True
        db_table = 'reservations_rating'
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return f'Rating: {self.rating} by {self.customer}'
