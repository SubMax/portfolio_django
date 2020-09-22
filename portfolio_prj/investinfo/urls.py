from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ticker_list'),
    path(r'<slug:ticker>', views.descriptionTicker, name='ticker_info'),
]
