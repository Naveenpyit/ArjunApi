from rest_framework.serializers import ModelSerializer
from . import models

class UserSerializer(ModelSerializer):
    class Meta:
        model= models.User
        fields = '__all__'
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def create(self,data):
        password = data.pop('password')
        user = models.User(**data)
        user.set_password(password)
        user.save()
        return user