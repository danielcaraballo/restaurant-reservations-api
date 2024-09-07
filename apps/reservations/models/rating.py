from django.db import models
from django.core.exceptions import ValidationError
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

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5.')

    def __str__(self):
        return f'Rating: {self.rating} by {self.customer}'
