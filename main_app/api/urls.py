from django.urls import path , include 
from .views import data_list

urlpatterns = [
    
    path('test', data_list , name='test'),
  
    
        
]


