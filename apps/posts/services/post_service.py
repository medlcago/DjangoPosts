from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from pydantic import ValidationError as pdValidationError

from apps.posts.models import Post
from apps.posts.schemes import PostUpdateRequest
from apps.utils import set_attrs


class PostService:
    @staticmethod
    def check_post_author(user_id: int, author_id: int) -> bool:
        return user_id == author_id

    @staticmethod
    def get_post(pk: int) -> Post:
        return get_object_or_404(Post, pk=pk)

    def create_post(self):
        pass

    def update_post(self, user_id: int, **kwargs) -> JsonResponse:
        try:
            request_data = PostUpdateRequest(
                **kwargs
            )
        except pdValidationError:
            return JsonResponse(data={
                "message": "Bad request"
            },
                status=400
            )

        post = self.get_post(pk=request_data.pk)

        if not self.check_post_author(user_id, post.author.id):
            return JsonResponse(data={
                "message": "Access denied"
            },
                status=403
            )

        if errors := set_attrs(post, request_data.model_dump(exclude={"pk"})):
            return JsonResponse(data={
                "message": "Bad request",
                "errors": errors
            },
                status=400
            )

        post.save()
        return JsonResponse(data={
            "message": "Post successfully updated"
        },
            status=200
        )

    def delete_post(self, user_id: int, pk: int) -> JsonResponse:
        if pk is None:
            return JsonResponse(data={
                "message": "Bad request"
            },
                status=400
            )

        post = self.get_post(pk=pk)

        if not self.check_post_author(user_id, post.author.id):
            return JsonResponse(data={
                "message": "Access denied"
            },
                status=403
            )

        post.delete()
        return JsonResponse(data={
            "message": "Post successfully deleted"
        },
            status=200
        )


post_service = PostService()
