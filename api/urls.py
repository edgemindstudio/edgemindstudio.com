# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, CustomTokenObtainPairView, user_data,
    enroll_course, is_enrolled, enrolled_users,
    mark_lesson_complete, my_courses, course_progress,
    UserViewSet, CourseViewSet, LessonViewSet,
    ForumThreadViewSet, ForumReplyViewSet,
    BlogPostViewSet, AIProjectViewSet, CommentViewSet,
    EnrollCourseView, UserProfileUpdateView
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

# Merge router + custom endpoints
urlpatterns = [
    path('', include(router.urls)),  # <- this adds /api/courses/

    # 🔐 Auth endpoints
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),

    # 👤 User
    path('user-data/', user_data),
    path('profile/', UserProfileUpdateView.as_view(), name='user-profile'),

    # 🎓 Enrollment
    path('enroll/', EnrollCourseView.as_view(), name='enroll-course'),
    path('courses/<int:pk>/enroll/', enroll_course),
    path('courses/<int:pk>/enrolled/', is_enrolled),
    path('courses/<int:pk>/enrolled-users/', enrolled_users),
    path('my-courses/', my_courses),

    # ✅ Progress
    path('courses/<int:course_id>/lessons/<int:lesson_id>/complete/', mark_lesson_complete),
    path('courses/<int:course_id>/progress/', course_progress),
]
