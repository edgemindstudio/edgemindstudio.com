from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet, CourseViewSet, LessonViewSet, ForumThreadViewSet,
    ForumReplyViewSet, BlogPostViewSet, AIProjectViewSet, CommentViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'forum-threads', ForumThreadViewSet)
router.register(r'forum-replies', ForumReplyViewSet)
router.register(r'blog-posts', BlogPostViewSet)
router.register(r'ai-projects', AIProjectViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
]
