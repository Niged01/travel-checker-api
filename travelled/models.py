from django.db import models
from django.contrib.auth.models import User


class Travelled(models.Model):
    '''database model for travelled page'''
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=250)
    city = models.TextField()
    image = models.ImageField(
        upload_to='images/', default='../default_profile_qdjgyp',
    )

    class Meta:
        ''' how to order'''
        ordering = ['-date_created']

    def __str__(self):
        '''what to return'''
        return f'{self.id} {self.title}'
