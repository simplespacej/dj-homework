from django.contrib.auth.models import User
from rest_framework import serializers
from advertisements.models import Advertisement

class AdvertisementSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'status', 'creator', 'created_at', 'updated_at')

    def validate(self, data):
        if self.instance is None:
            user_ads = Advertisement.objects.filter(creator=self.context['request'].user, status='OPEN').count()
            if user_ads >= 10:
                raise serializers.ValidationError("You can't have more than 10 open advertisements")
        return data
