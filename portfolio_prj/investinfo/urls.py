from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ticker_list'),
    path(r'about', views.about, name='about'),
    path(r'<slug:ticker>', views.description_ticker, name='ticker_info'),
    path(r'<slug:ticker>/<str:text>/<slug:period>/<slug:interval>/', views.stock_data_ticker, name='chart_period'),
    path(r'<slug:ticker>/<str:text>/<int:ystart>/<int:mstart>/<int:dstart>/'
         r'<int:yend>/<int:mend>/<int:dend>/<slug:interval>/',
         views.stock_data_ticker,
         name='chart_date'),
]
