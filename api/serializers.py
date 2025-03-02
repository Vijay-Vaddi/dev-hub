from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

 
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    # owner = ProfileSerializer(many=False)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    # this will connect to a profile and return owner field in project
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data