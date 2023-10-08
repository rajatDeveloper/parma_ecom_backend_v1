from rest_framework import serializers
from main_app.models import Product , Address , User  , Order , CartProduct

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'
        
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        
class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False)
    
    
    partial = True  
    class Meta:
        model = CartProduct
        fields = '__all__'   
        
class CartProductCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()    
    user_id = serializers.IntegerField()     
        
class OrderCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    address_id = serializers.IntegerField()
    cart_product_ids = serializers.ListField(child=serializers.IntegerField())
    payment_id = serializers.CharField(required=False)  # Make payment_id optional
      # Use the Order's choices
    total = serializers.IntegerField()
             
        
               

class OrderSerializer(serializers.ModelSerializer):
    cart_products = CartProductSerializer(many=True)
    address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_address(self, obj):
        # Customize how the "address" field is serialized
        address = obj.address
        return {
            "id": address.id,
            "address": address.address,
            "city": address.city,
            "state": address.state,
            "zipCode": address.zipCode,
            "phone": address.phone,
            "email": address.email,
            # Add other address fields as needed
        }              


        
        
        