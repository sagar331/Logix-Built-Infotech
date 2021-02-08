from django.shortcuts import render
from registerapp.models import *
from rest_framework.response import Response
from rest_framework import viewsets,status
from django.contrib.auth import authenticate
import traceback
from django.utils.timezone import now, timedelta
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
#Send_mail
from django.core.mail import send_mail
def send_email_display():
    send_mail(
            'testing mail',
            'Here is the message.',
            'sagar.innotical@gmail.com',
            ['sagarsmn331@gmail.com'],
            fail_silently=False,
            )
    return send_email_display

class RegisterView(viewsets.ViewSet):
    def create(self,request):
        mobile=request.data.get('mobile')
        if not mobile:
            return Response('please enter the mobile no:')
        phone_object=PhoneNumber()
        phone_object.phone=mobile
        phone_object.save()
        try:
            email=request.data.get('email')
            user_email=MyUser.objects.filter(email=email)
            if  user_email:
                return Response('already register email')

            myuser=MyUser()
            myuser.save()
            myuser.mobile.add(phone_object)
            myuser.email=request.data.get('email')
            myuser.first_name=request.data.get('first_name')
            myuser.last_name=request.data.get('last_name')
            myuser.date_of_birth=request.data.get('dob')
            myuser.gender=request.data.get('gender')
            myuser.role=request.data.get('role')
            myuser.set_password(request.data.get('password'))
            myuser.mobile.add(phone_object)
            myuser.is_active=True
            myuser.save()
            app = Application.objects.create(user=myuser)
            token = generate_token()
            refresh_token = generate_token()
            expires = now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
            scope = "read write"
            access_token = AccessToken.objects.create(user=myuser,
                                                application=app,
                                                expires=expires,
                                                token=token,
                                                scope=scope,
                                                )
            print("access token ------->", access_token)
            RefreshToken.objects.create(user=myuser,
                                        application=app,
                                        token=refresh_token,
                                        access_token=access_token
                                        )
            response = {
                'access_token': access_token.token,
                'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
                'token_type': 'Bearer',
                'refresh_token': access_token.refresh_token.token,
                'client_id': app.client_id,
                'client_secret': app.client_secret
                }
            
            return Response({'response':'you are sign up successfull ','message':True,'status':status.HTTP_200_OK})
        except Exception as error:
            traceback.print_exc()
            return Response({'response':str(error),'message':False,'status':status.HTTP_200_OK})
  


class LoginView(viewsets.ViewSet):
    # permission_classes = [TokenHasReadWriteScope]
    def create(self,request):
        try:
            email=request.data.get('email')
            password=request.data.get('password')

            user=authenticate(email=email,password=password)
            send_email_display()

            if user is not None:
                app = Application.objects.get(user=user)  
                # token = get_access_token(user)
                token = generate_token()
                refresh_token = generate_token()
                expires = now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
                scope = "read write"
                access_token = AccessToken.objects.create(user=user,
                                                        application=app,
                                                        expires=expires,
                                                        token=token,
                                                        scope=scope,
                                                        )
                    
                RefreshToken.objects.create(user=user,
                                        application=app,
                                        token=refresh_token,
                                        access_token=access_token
                                        )

            

                response = {
                    'name':user.first_name,
                    'access_token': access_token.token,
                    'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,                    'token_type': 'Bearer',
                    'refresh_token': access_token.refresh_token.token,
                    'client_id': app.client_id,
                    'client_secret': app.client_secret
                    }
                
                
                return Response({'response':response,'message':True,'status':status.HTTP_200_OK})

            else:
                email=MyUser.objects.filter(email=email)
                if not email:
                    return Response({'response':'email is not valid plz enter valid email id','message':False,'status':status.HTTP_200_OK})
                password=MyUser.objects.filter(password=password)
                if not password:
                    return Response({'response':'password is not valid plz enter valid paasword id','message':False,'status':status.HTTP_200_OK})
        except Exception as error:
            traceback.print_exc()
            return Response({'response':str(error),'message':False,'status':status.HTTP_200_OK})
  


class JobViewSet(viewsets.ViewSet):
    def list(self,request):

        job_obj=Job.objects.filter(user__role='Welder')
        job_list=[]
        for job_obj in job_obj:
            job_list.append({
                'welder':job_obj.user.role,
                'title':job_obj.title,
                'description':job_obj.description,
                'salary':job_obj.salary,
            })
        return Response({'response':job_list})

    def create(self,request):
        id=int(request.data.get('id'))
       
        user_obj=MyUser.objects.get(id=id)
        
        if user_obj.role == "Welder":
            return Response('you are not authorided')
        else:
        
            job=Job()
            job.user=user_obj
            job.title=request.data.get('title')
            job.description=request.data.get('description')
            job.salary=request.data.get('salary')
            job.save()
            return Response('Saved')
            

        

    