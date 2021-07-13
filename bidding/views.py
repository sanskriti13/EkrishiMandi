from django.shortcuts import render,redirect,HttpResponse
from datetime import datetime,timedelta
from django.utils import timezone
from .forms import FarmerRegister
from pgeocode import GeoDistance
from accounts.models import *
from .models import *
from accounts.views import *
# Create your views here.
def index(request):
    if 'user' in request.session:
        if request.session['role']=='Farmer':
            fm = FarmerRegister()
            if request.method == 'POST':
                fm = FarmerRegister(request.POST)
                if fm.is_valid():
                    fm.save()
                return redirect('index')
            else :
                context={
                    'form' : fm,
                    'user': request.session['user']
                }
                return render(request,'index.html',context)
        else :
            return redirect('bid')
    else:
        return redirect('login')

def bid(request):
    if 'user' in request.session:
        if request.session['role'] == 'Trader':
            far = trade.objects.select_related('crop','farmer').values('farmer__zipcode','farmer__name','crop__cname','farmer__entrytime','id','crop__cimage')
            email=request.session['user']
            trader_pincode= User.objects.filter(email=email).values()
            trader_pincode=trader_pincode[0]
            trader_pincode=trader_pincode['pincode']
            l=[]
            for fa in far:
                farmer_zipcode = fa['farmer__zipcode']
                dist = GeoDistance('in')
                calculate_dist = dist.query_postal_code(trader_pincode,farmer_zipcode)
                calculate_dist=round(calculate_dist,2)
                fa['dist']=calculate_dist
                l.append(fa)
            context={
                'farmer':l,
                'user': request.session['user']
            }
            return render(request,'bidTrader.html',context)
        else :
            return redirect('index')
    else :
        return redirect('login')

def updatebid(request,id):
    lastbid = trade.objects.values('lastBid').get(pk=id)
    if request.method =='POST':
        bid = request.POST['updatebid']
        bid  = int(bid)
        if bid > lastbid['lastBid']:
            trade.objects.filter(pk=id).update(lastBid=bid)
            return HttpResponse('SUCCESS')
        else:
            return render(request,'error.html')
    else:
        et = trade.objects.select_related('farmer').values('farmer__entrytime').get(pk=id)
        et1 = et['farmer__entrytime'] + timedelta(minutes=120)

        if et1 >= timezone.now():
            a = trade.objects.select_related('farmer','trader','crop').values('farmer__name','crop__cname','farmer__qty','lastBid','id').get(pk=id)
            context = {'farmername': a['farmer__name'], 'cropname': a['crop__cname'] ,'cqty': a['farmer__qty'], 'lastbid': a['lastBid'] , 'traderid': a['id']}
            return render(request,'update.html',context)
        else:
            a = trade.objects.select_related('farmer','crop','trader').values('farmer__name','crop__cname','farmer__qty','trader__name','lastBid').get(pk=id)
            context = {'farmername':a['farmer__name'] , 'cropname': a['crop__cname'], 'cqty':a['farmer__qty'], 'tradername': a['trader__name'] , 'lastbid': a['lastBid']}
            return render(request,'update.html',context)


def mspchart(request):
    c = crops.objects.all()
    return render(request,'mspchart.html',{'crop':c})

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'aboutus.html')
