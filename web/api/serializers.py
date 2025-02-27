from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Extra info added along access and refresh
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        return data