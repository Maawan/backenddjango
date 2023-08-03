from django.db import models

# Create your models here.
class data(models.Model):
    user_id = models.CharField(max_length=50, unique=True)
    user_name = models.CharField(max_length=20, blank=True, default="User")
    mov1 = models.CharField(max_length=50, null=True, blank=True, default="The Shawshank Redemption")
    mov2 = models.CharField(max_length=50, null=True, blank=True, default="The Godfather")
    mov3 = models.CharField(max_length=50, null=True, blank=True, default="The Dark Knight")
    mov4 = models.CharField(max_length=50, null=True, blank=True, default="Pulp Fiction")
    mov5 = models.CharField(max_length=50, null=True, blank=True, default="American History X")
    weekT1 = models.CharField(max_length=100, null=True, blank=True, default=None)
    weekT2 = models.CharField(max_length=100, null=True, blank=True, default=None)
    weekT3 = models.CharField(max_length=100, null=True, blank=True, default=None)
    weekT4 = models.CharField(max_length=100, null=True, blank=True, default=None)
    dailyT1 = models.CharField(max_length=100, null=True, blank=True, default=None)
    dailyT2 = models.CharField(max_length=100, null=True, blank=True, default=None)
    dailyT3 = models.CharField(max_length=100, null=True, blank=True, default=None)
    dailyT4 = models.CharField(max_length=100, null=True, blank=True, default=None)
    totalWatchTime = models.FloatField(default=0.0)
    weeklyWatchTime = models.FloatField(default=0.0)
    rewardPoints = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user_id)