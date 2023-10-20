
from django.urls import path , include
from user_app.api.views import regisgration_view  , logout_view , custom_auth_token

urlpatterns = [
    path('login/' , custom_auth_token , name='login'),
    path('register/' , regisgration_view , name='register') , 
    path('logout/' , logout_view , name='logout'),
    
# {
#     "username":"rajat34" , 
#     "password":"rajat@123" , 
#     "password2":"rajat@123" , 
#     "email":"rajat34@gmail.com"
# }


# {
#     "username":"rajat_dhiman" , 
#     "password" : "Rajat@12345"
# }
    
]