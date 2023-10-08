from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse 
from rest_framework.response import Response
from main_app.models import Product , Address , User  , Order , CartProduct
from main_app.api.serializers import AddressSerializer , OrderSerializer , ProductSerializer , CartProductSerializer ,OrderCreateSerializer , CartProductCreateSerializer
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

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer    

     
    

class CartProductListView(generics.ListAPIView):
    serializer_class = CartProductSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        return CartProduct.objects.filter(user=user)
    
class CartProductCreateView(generics.CreateAPIView):
    serializer_class = CartProductCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            
            # Check if the product exists and if the quantity is less than or equal to the available stock
            try:
                product = Product.objects.get(id=product_id)
                if quantity <= product.stock:
                    # Create the cart product
                    cart_product = CartProduct.objects.create(
                    
                        product=product,
                        quantity=quantity,
                        user_id=user_id  # Assuming you have a user associated with the request
                    )
                    return Response(CartProductSerializer(cart_product).data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Quantity exceeds available stock"}, status=status.HTTP_400_BAD_REQUEST)
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    
    
class CartProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            new_quantity = serializer.validated_data.get('quantity', instance.quantity)
            
            # Check if the new quantity is greater than the available stock
            product = instance.product
            if new_quantity > product.stock:
                return Response({"error": "Quantity exceeds available stock"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
           
    

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        return Order.objects.filter(user=user)
    
    
class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            address_id = serializer.validated_data['address_id']
            cart_product_ids = serializer.validated_data['cart_product_ids']
            payment_id = serializer.validated_data.get('payment_id')  # Payment ID is optional
            
            total = serializer.validated_data['total']
            
            # Fetch the cart products and calculate the total
            cart_products = CartProduct.objects.filter(id__in=cart_product_ids)
            calculated_total = sum(cart_product.product.afterDiscountPrice * cart_product.quantity for cart_product in cart_products)
            
            if total != calculated_total:
                return Response({"error": "Total amount does not match the calculated total"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create the order for the specified user and address
            order = Order.objects.create(
                user_id=user_id,
                address_id=address_id,
                total=total,
                dilveryStatus="pending",
                payment_id=payment_id,
            )
            
            # Associate the selected cart products with the order
            order.cart_products.set(cart_products)  # Use the set() method
            
            # Update the product stock
            for cart_product in cart_products:
                product = cart_product.product
                if product.stock >= cart_product.quantity:
                    product.stock -= cart_product.quantity
                    product.save()
                else:
                    # Handle insufficient stock error
                    return Response({"error": "Insufficient stock for one or more products"}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def data_list(request):
    return JsonResponse({'server':"server is up !"})
