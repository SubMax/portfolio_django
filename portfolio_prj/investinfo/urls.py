from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ticker_list'),
    path(r'<slug:ticker>', views.descriptionTicker, name='ticker_info'),
    path(r'<slug:ticker>/<str:text>/', views.descriptionTicker, name='chart'),
    path(r'<slug:ticker>/<str:text>/<str:ystart>/<str:mstart>/<str:dstart>/<str:yend>/<str:mend>/<str:dend>/<slug'
         r':interval>/', views.descriptionTicker, name='chart'),
]
