from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserUpdateSerializer  # ✅ Add this
from rest_framework import viewsets, permissions
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer
from .models import User, Course, Lesson, ForumThread, ForumReply, BlogPost, AIProject, Comment
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Enrollment
from .serializers import EnrollmentSerializer
from rest_framework import generics
from .serializers import (
    UserSerializer, CourseSerializer, LessonSerializer, ForumThreadSerializer,
    ForumReplySerializer, BlogPostSerializer, AIProjectSerializer, CommentSerializer
)
from .models import UserCourseProgress
from .serializers import UserCourseProgressSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_progress(request, course_id):
    try:
        progress = UserCourseProgress.objects.get(user=request.user, course_id=course_id)
        serializer = UserCourseProgressSerializer(progress)
        return Response(serializer.data)
    except UserCourseProgress.DoesNotExist:
        return Response({'progress': 0}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_lesson_complete(request, course_id, lesson_id):
    user = request.user
    try:
        course = Course.objects.get(pk=course_id)
        lesson = Lesson.objects.get(pk=lesson_id, course=course)
    except (Course.DoesNotExist, Lesson.DoesNotExist):
        return Response({'error': 'Course or lesson not found'}, status=404)

    progress, created = UserCourseProgress.objects.get_or_create(user=user, course=course)
    progress.completed_lessons.add(lesson)

    total_lessons = course.lessons.count()
    completed = progress.completed_lessons.count()
    progress.progress_percentage = round((completed / total_lessons) * 100, 2)
    progress.completed = (progress.progress_percentage == 100.0)
    progress.save()

    return Response({'message': 'Lesson marked complete', 'progress': progress.progress_percentage})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    data = [CourseSerializer(e.course).data for e in enrollments]
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_course(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    Enrollment.objects.get_or_create(user=request.user, course=course)
    return Response({'message': 'Enrolled successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_enrolled(request, pk):
    enrolled = Enrollment.objects.filter(user=request.user, course_id=pk).exists()
    return Response({"enrolled": enrolled})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_data(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        'role': user.role
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def enrolled_users(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=404)

    if request.user.role != 'admin':
        return Response({'error': 'Unauthorized'}, status=403)

    users = Enrollment.objects.filter(course=course).select_related('user')
    data = [
        {
            'id': e.user.id,
            'username': e.user.username,
            'email': e.user.email
        } for e in users
    ]
    return Response(data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course)
        data = serializer.data

        user = request.user
        is_enrolled = Enrollment.objects.filter(user=user, course=course).exists()

        if is_enrolled or user.role in ['admin', 'staff']:
            data['lessons'] = LessonSerializer(course.lessons.all(), many=True).data
        else:
            data['lessons'] = []  # hide lessons if not enrolled

        return Response(data)

    def perform_create(self, serializer):
        if self.request.user.role not in ['admin', 'staff']:
            raise PermissionDenied("Only staff/admin can create courses.")
        serializer.save(instructor=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role not in ['admin', 'staff']:
            raise PermissionDenied("Only instructors or admins can create lessons.")
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user.role not in ['admin', 'staff']:
            raise PermissionDenied("Only instructors or admins can update lessons.")
        serializer.save()

class ForumThreadViewSet(viewsets.ModelViewSet):
    queryset = ForumThread.objects.all()
    serializer_class = ForumThreadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ForumReplyViewSet(viewsets.ModelViewSet):
    queryset = ForumReply.objects.all()
    serializer_class = ForumReplySerializer
    permission_classes = [IsAuthenticated]

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AIProjectViewSet(viewsets.ModelViewSet):
    queryset = AIProject.objects.all()
    serializer_class = AIProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
        }
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class EnrollCourseView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
