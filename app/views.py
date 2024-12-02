from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app import metrics
import json

@login_required(login_url='login')
def home(request):
    inventory_metrics = metrics.get_inventory_metrics()
    brand_equipaments = metrics.get_brand_equipaments()
    status_equipaments = metrics.get_status_equipaments()
    sectors_equipaments = metrics.get_sectors_equipaments()
    daily_register = metrics.get_daily_register()

    context = {
        'inventory_metrics': inventory_metrics,
        'brand_equipaments': brand_equipaments,
        'status_equipaments': status_equipaments,
        'sectors_equipaments': sectors_equipaments,
        'daily_register': daily_register,
    }

    return render(request, 'home.html', context)