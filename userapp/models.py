from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='uprofile')
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    city = models.CharField(max_length=100, null=False)
    contact = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class City(models.Model):
    name = models.CharField(max_length=100,)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PackerProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='pprofile')
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    company = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class DriverProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='dprofile')
    company = models.ForeignKey(
        PackerProfile, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class Vehicles(models.Model):
    owner = models.ForeignKey(PackerProfile, on_delete=models.CASCADE)
    pnumber = models.CharField(max_length=10)
    vmodel = models.CharField(max_length=100)
    wcap = models.IntegerField()
    byear = models.DateField()

    def __str__(self):
        return self.vmodel


class Tvehicle(models.Model):
    vehicle = models.ForeignKey(
        Vehicles, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(PackerProfile, on_delete=models.CASCADE)
    spoint = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='spoint')
    epoint = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='epoint')
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE)
    cap_wt = models.IntegerField(null=True)
    cap_sz = models.IntegerField(null=True)
    date = models.DateField()

    def __str__(self):
        return self.spoint.name


class Consignment(models.Model):

    type = models.CharField(max_length=100)
    wt = models.IntegerField()
    sz = models.IntegerField()
    date = models.DateField()
    address = models.CharField(max_length=160)
    status = models.IntegerField()
    company = models.ForeignKey(PackerProfile, on_delete=models.CASCADE)
    tvehicle = models.ForeignKey(Tvehicle, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
