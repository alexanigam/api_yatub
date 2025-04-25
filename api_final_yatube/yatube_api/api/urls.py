from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register('groups', views.GroupsViewSet)
router.register('posts', views.PostsViewSet)
router.register('follow', views.FollowsApiView, basename='follow')
router.register(
    r'posts/(?P<post_pk>\d+)/comments',
    views.CommentsViewSet,
    basename='comments')

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls))
]
