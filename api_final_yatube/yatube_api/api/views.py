from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework import viewsets, mixins, filters

from .serializers import (PostSerializer,
                          CommentSerializer,
                          GroupSerializer,
                          FollowSerializer)
from .permissions import OnlyOwnerCanModify

from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class GroupsViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class PostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        OnlyOwnerCanModify
    )
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def paginate_queryset(self, queryset):
        if 'limit' in self.request.query_params \
                or 'offset' in self.request.query_params:
            self.pagination_class = LimitOffsetPagination

        return super().paginate_queryset(queryset)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, OnlyOwnerCanModify)

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise NotFound('Category not found')
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)


class FollowsApiView(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            following = User.objects.get(
                username=self.request.data['following']
            )
            if self.request.user == following:
                raise ValidationError('You cant follow to yourself')
            serializer.save(user=self.request.user, following=following)
        except User.DoesNotExist:
            raise NotFound('User not found')
        except IntegrityError:
            raise ValidationError('Already following')
