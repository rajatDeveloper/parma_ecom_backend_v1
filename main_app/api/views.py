from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse



#contact us view with get list of contacts and post -> 

# class ContactUsView(generics.ListCreateAPIView):
#     queryset = ContactUs.objects.all()
#     serializer_class = ConatctUsSerializer
    
# #feedback view with get list of contacts and post -> 



def data_list(request):
    return JsonResponse({'server':"server is up !"})
