from rest_framework import serializers
from travelled.models import Travelled

class TravelledSerializer(serializers.ModelSerializer):
    '''serializer class for main serializer app'''
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    

    def validate_image(self, value):
        '''make sure uploaded image does not exceed size'''
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image larger than 2MB! Reduce'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px reduce'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px reduce'
            )
        return value

    def get_is_owner(self, obj):
        '''check user is owner'''
        request = self.context['request']
        return request.user == obj.owner


    class Meta:
        '''fields we want to display'''
        model = Travelled
        fields = [
            'city', 'country', 'date_created', 'id', 'image', 'owner', 
            'owner_id', 'profile_image', 'is_owner', 'profile_id',
        ]
