from django.contrib.auth.models import User, Group
from .models import DriverProfile, PackerProfile, UserProfile, City, Tvehicle, Consignment, Vehicles
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout

from datetime import date, datetime

from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index(request):
    return render(request, 'index.html')


def udashbaord(request):

    if request.user.is_authenticated:
        cities = City.objects.all()
        today = datetime.today()
        vehicles = Tvehicle.objects.filter(
            date=str(today.strftime('%Y-%m-%d'))).all()
        consignments = Consignment.objects.filter(
            user=request.user).order_by('-id')

        if request.method == "POST":
            sp = request.POST['sp']
            ep = request.POST['ep']

            cities = City.objects.all()
            vehicles = Tvehicle.objects.filter(spoint=sp, epoint=ep).all()
            return render(request, 'dashboard.html', {"cities": cities, "vehicles": vehicles, "consign": consignments})
        return render(request, 'dashboard.html', {"cities": cities, "vehicles": vehicles, "consign": consignments})

    return redirect('login')


def ulogout(request):
    logout(request)
    return redirect('')


def ulogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:

            if user.groups.filter(name='user').exists():
                login(request, user)
                return redirect('dashboard')
            else:
                return redirect('login')
        else:
            return redirect('login')

    return render(request, 'login.html')


def addconsign(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            user = request.user
            tvid = request.POST['tvid']
            ctype = request.POST['ctype']
            cwt = request.POST['cwt']
            csz = request.POST['csz']
            cadd = request.POST['cadd']
            ddate = date.today()
            status = 1

            cs = Tvehicle.objects.filter(id=tvid).first()
            consignment = Consignment(
                type=ctype, company=cs.company, wt=cwt, sz=csz, date=ddate, address=cadd, status=status, tvehicle=cs, user=user)
            consignment.save()

            return redirect('dashboard')
        return redirect('dashboard')


def uregister(request):

    if request.method == "POST":

        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        email = request.POST["email"]
        contact = request.POST['contact']
        password = request.POST['password']
        city = request.POST['city']

        user = User.objects.create_user(email, email, password)
        user.save()

        ugroup = Group.objects.get(name='user')
        ugroup.user_set.add(user)

        profile = UserProfile(user=user, city=city, contact=contact,
                              first_name=first_name, last_name=last_name)
        profile.save()

        return redirect('login')

    return render(request, 'user-register.html')


# View Operations for Vendor


def vendor(request):
    if request.user.is_authenticated:

        pf = PackerProfile.objects.get(user=request.user)

        # tv = Tvehicle.objects.get(company=pf)

        vehicles = Vehicles.objects.filter(owner=pf)
        drivers = DriverProfile.objects.filter(company=pf)
        consign = Consignment.objects.filter(company=pf)
        city = City.objects.all()
        return render(request, 'vendor/vendor_dash.html', {'vehicles': vehicles, 'drivers': drivers, 'tvs': consign, 'city': city})
    else:
        return redirect('vendor-login')


@csrf_exempt
def paystatus(request, pk):
    Consignment.objects.filter(id=pk).update(status=3)
    return redirect('dashboard')
    # return HttpResponse('Payment Success')


def add_tvride(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            pf = PackerProfile.objects.get(user=request.user)
            fcity = request.POST['fcity']
            ecity = request.POST['ecity']
            veh = request.POST['veh']
            driver = request.POST['driver']
            date = request.POST['date']

            vh = Vehicles.objects.get(pk=veh)
            c1 = City.objects.get(pk=fcity)
            c2 = City.objects.get(pk=ecity)
            d = DriverProfile.objects.get(pk=driver)
#  vehicle = models.ForeignKey(
#         Vehicles, on_delete=models.CASCADE, null=True)
#     company = models.ForeignKey(PackerProfile, on_delete=models.CASCADE)
#     spoint = models.ForeignKey(
#         City, on_delete=models.CASCADE, related_name='spoint')
#     epoint = models.ForeignKey(
#         City, on_delete=models.CASCADE, related_name='epoint')
#     driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE)
#     cap_wt = models.IntegerField(null=True)
#     cap_sz = models.IntegerField(null=True)
#     date = models.DateField()

            tvf = Tvehicle(vehicle=vh, company=pf, spoint=c1,
                           epoint=c2, driver=d, date=date)

            tvf.save()
            return redirect('vendor')


def update_status(request, pk):
    Consignment.objects.filter(pk=pk).update(status=2)
    return redirect('vendor')


def addvehicle(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            model = request.POST['vmodel']
            cap = request.POST['vcap']
            passn = request.POST['vpass']
            year = request.POST['vyear']

            packer = PackerProfile.objects.get(user=request.user)

            vh = Vehicles(owner=packer, pnumber=passn,
                          vmodel=model, wcap=cap, byear=year)
            vh.save()

            return redirect('vendor')


def add_driver(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            fname = request.POST['dfname']
            lname = request.POST['dlname']
            email = request.POST['demail']
            contact = request.POST['dcno']
            city = request.POST['dcity']
            dpass = "driver"

            packer = PackerProfile.objects.get(user=request.user)

            user = User.objects.create_user(email, email, dpass)
            user.save()

            driver = DriverProfile(
                user=user, company=packer, first_name=fname, last_name=lname, contact=contact, city=city)
            driver.save()

            return redirect('vendor')

        # vh = Vehicles(owner=packer, pnumber=passn,
        #               vmodel=model, wcap=cap, byear=year)
        # vh.save()

        return redirect('vendor')


def vendorlogin(request):

    if request.method == 'POST':
        vemail = request.POST['vemail']
        vpass = request.POST['vpass']

        user = authenticate(username=vemail, password=vpass)
        if user is not None:

            if user.groups.filter(name='vendor').exists():
                login(request, user)
                return redirect('vendor')
            else:
                return redirect('vendor-login')
        else:
            return redirect('vendor-login')

    return render(request, 'vendor/vendor_login.html')


def vendorregister(request):

    if request.method == "POST":
        fname = request.POST['vfname']
        lname = request.POST['vlname']
        city = request.POST['vcity']
        company = request.POST['vcompany']

        contact = request.POST['vcno']
        email = request.POST['vemail']
        vpass = request.POST['vpass']

        user = User.objects.create_user(email, email, vpass)
        user.save()

        ugroup = Group.objects.get(name='vendor')
        ugroup.user_set.add(user)

        profile = PackerProfile(user=user, first_name=fname,
                                last_name=lname, company=company, city=city, contact=contact)
        profile.save()

        return redirect('vendor-login')

    return redirect('vendor-login')
