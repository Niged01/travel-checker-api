from rest_framework import serializers
from likes.models import Like
from travelled.models import Travelled

class TravelledSerializer(serializers.ModelSerializer):
    '''serializer class for main serializer app'''
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()

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

    def get_like_id(self, obj):
        '''owner can unlike the achievement'''
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        '''fields we want to display'''
        model = Travelled
        fields = [
            'id', 'owner', 'date_created', 'title', 'content',
            'image', 'is_owner', 'profile_id', 'profile_image',
            'like_id', 'likes_count', 'comments_count',
        ]
