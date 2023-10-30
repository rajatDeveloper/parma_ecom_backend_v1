from django.urls import path , include 
from .views import data_list , ProductView , ProductGetUpdateDeleteView , AddressListUpdateView , CartProductListView , OrderListView ,  CartProductRetrieveUpdateDeleteView , AddressDetailView , OrderCreateView , CartProductCreateView

urlpatterns = [
        
    path('test/', data_list , name='test'),
    #get all products and add new product to list
    path('products/' ,ProductView.as_view() , name='products' )  , 
    #get single product and update delete 
    path('product/<int:pk>/' , ProductGetUpdateDeleteView.as_view() , name='product') , 
       
       
    path('users/<int:user_id>/addresses/', AddressListUpdateView.as_view(), name='address-list-update'), 
    path('address/<int:pk>/', AddressDetailView.as_view(), name='address-detail'), 
      
    #create product cart for user
    
    path('users/<int:user_id>/cart-products/', CartProductListView.as_view(), name='cart-product-list'),
     path('cart-product/create/', CartProductCreateView.as_view(), name='cart-product-create'),

    # update the product cart data using id of product cart and pass quality and user id 
    path('cart-products/<int:pk>/', CartProductRetrieveUpdateDeleteView.as_view(), name='cart-product-retrieve-update-delete'),
    
    
    path('users/<int:user_id>/orders/', OrderListView.as_view(), name='order-list'),
    
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    
    
    
    
 
        
]


