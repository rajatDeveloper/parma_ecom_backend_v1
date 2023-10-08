from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
import user_app.models 
from rest_framework.decorators import api_view




from rest_framework import status

@api_view(['POST'])
 # Allow anyone to access this view
def custom_auth_token(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'id': user.id,
            'email':user.email
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def  regisgration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {};
        if serializer.is_valid():
            
            account = serializer.save()
            #normal token
            token = Token.objects.get(user=account).key
            
            # print(token)
            data['token']  = token
            data['username'] = account.username 
            data['email'] = account.email
            data['id'] = account.id
            return Response(data , status=status.HTTP_201_CREATED) 
       
            
        else : 
            data = serializer.errors
            return Response(data , status=status.HTTP_400_BAD_REQUEST) 
         
        
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response( {
            "message" : "logout successfully"
            }, status=status.HTTP_200_OK)    
            
     