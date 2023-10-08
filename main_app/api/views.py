from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse 
from rest_framework.response import Response
from main_app.models import Product , Address , User  , Order , CartProduct
from main_app.api.serializers import AddressSerializer , OrderSerializer , ProductSerializer , CartProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status


class ProductView(generics.ListCreateAPIView):        
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
class ProductGetUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):        
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  


class AddressListUpdateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        return Address.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        request.data['user'] = user.id
        serializer = AddressSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     
    

class CartProductListCreateView(generics.ListCreateAPIView):
    serializer_class = CartProductSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        return CartProduct.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        request.data['user'] = user.id
        serializer = CartProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
        
    

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        return Order.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        request.data['user'] = user.id
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     

class CartProductDeleteView(generics.DestroyAPIView):
    queryset = CartProduct.objects.all()  # All cart products
    lookup_url_kwarg = 'cart_product_id'  # URL parameter for cart product id

    def destroy(self, request, *args, **kwargs):
        cart_product = get_object_or_404(self.get_queryset(), id=self.kwargs[self.lookup_url_kwarg])
        cart_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def data_list(request):
    return JsonResponse({'server':"server is up !"})
