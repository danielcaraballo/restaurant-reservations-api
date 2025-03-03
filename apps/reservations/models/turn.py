from django.db import models
from django.core.exceptions import ValidationError


class TurnStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'


class Turn(models.Model):
    name = models.CharField('Name', max_length=50, null=False, blank=False)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    status = models.CharField(
        'Status', max_length=20, choices=TurnStatus.choices, default=TurnStatus.ACTIVE)

    class Meta:
        managed = True
        db_table = 'reservations_turn'
        verbose_name = 'Turn'
        verbose_name_plural = 'Turns'

    def clean(self):
        """Validaciones antes de guardar el modelo"""
        if self.opening_time >= self.closing_time:
            raise ValidationError('Opening time must be before closing time.')

        overlapping_turns = Turn.objects.filter(
            opening_time__lt=self.closing_time,
            closing_time__gt=self.opening_time,
            status=TurnStatus.ACTIVE  # Solo verifica solapamiento en turnos activos
        ).exclude(pk=self.pk)

        if overlapping_turns.exists():
            raise ValidationError(
                "This turn overlaps with another active turn.")

    def save(self, *args, **kwargs):
        """Asegura que clean() se ejecute antes de guardar"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.get_status_display()})'
