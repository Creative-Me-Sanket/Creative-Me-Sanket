from django.contrib import admin
from .models import UserProfile, DriverProfile, PackerProfile, City, Tvehicle, Consignment, Vehicles

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(DriverProfile)
admin.site.register(PackerProfile)
admin.site.register(City)
admin.site.register(Tvehicle)
admin.site.register(Consignment)
admin.site.register(Vehicles)
