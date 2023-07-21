from django.contrib.auth.models import User


class EmailBackend:
    def authenticate(self, request, auth_field=None, password=None):
        try:
            return self.check_user(auth_field, password, 'username')

        except User.DoesNotExist:
            
            try: 
                return self.check_user(auth_field, password, 'email')
            
            except User.DoesNotExist:
                return None

        
    def check_user(self, auth_field, password, by='username'):
        user = None

        if by == 'username':
            user = User.objects.get(username=auth_field)

        elif by == 'email':
            user = User.objects.get(email=auth_field)
  
        if user.check_password(password):
            return user

        return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
                

                
