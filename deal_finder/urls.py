from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('properties/', views.property_list),
    path('properties/<id>', views.property_detail),
]