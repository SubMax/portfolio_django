from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ticker_list'),
    path(r'about', views.about, name='about'),
    path(r'<slug:ticker>', views.descriptionticker, name='ticker_info'),
    path(r'<slug:ticker>/<str:text>/<slug:period>/<slug:interval>/', views.descriptionticker, name='chart'),
    path(r'<slug:ticker>/<str:text>/<str:ystart>/<str:mstart>/<str:dstart>/'
         r'<str:yend>/<str:mend>/<str:dend>/<slug:interval>/',
         views.descriptionticker,
         name='chartdate'),
]
