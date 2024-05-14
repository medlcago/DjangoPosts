from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from pydantic import ValidationError as pdValidationError

from apps.posts.models import Post
from apps.posts.schemes import PostUpdateRequest


class PostService:
    def set_attrs(self, post: Post, data: dict, validate: bool = True) -> dict | None:
        for key, value in data.items():
            setattr(post, key, value)
        if validate:
            return self.full_clean(post)

    @staticmethod
    def check_post_author(user_id: int, author_id: int) -> bool:
        return user_id == author_id

    @staticmethod
    def get_post(pk: int) -> Post:
        return get_object_or_404(Post, pk=pk)

    @staticmethod
    def full_clean(post: Post) -> dict | None:
        try:
            post.full_clean()
        except ValidationError as ex:
            error_dict = ex.message_dict
            errors = {field: messages for field, messages in error_dict.items()}
            return errors

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

        if errors := self.set_attrs(post, request_data.model_dump(exclude={"pk"})):
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
