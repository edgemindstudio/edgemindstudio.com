# api/serializer.py

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import UserCourseProgress
from .models import User, Course, Lesson, ForumThread, ForumReply, BlogPost, AIProject, Comment, Enrollment

# ---------- USER ----------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'profile_picture']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture']

# ---------- COURSES ----------
class CourseSerializer(serializers.ModelSerializer):
    instructor_username = serializers.CharField(source='instructor.username', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'instructor',
            'instructor_username',
            'price',
            'access_type',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

# ---------- LESSON ----------
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

# ---------- OTHER MODELS ----------
class ForumThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumThread
        fields = '__all__'

class ForumReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumReply
        fields = '__all__'

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'

class AIProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIProject
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'


class UserCourseProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourseProgress
        fields = '__all__'
