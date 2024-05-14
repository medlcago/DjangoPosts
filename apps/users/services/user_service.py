from django.http import HttpRequest, JsonResponse, QueryDict

from apps.users.forms import UpdateProfilePhotoForm
from apps.users.models import Profile


class UserService:
    @staticmethod
    def validate_update_profile_photo_form(request: HttpRequest, profile: Profile) -> UpdateProfilePhotoForm | None:
        form = UpdateProfilePhotoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            return form

    def update_photo(self, profile: Profile, files: QueryDict, request: HttpRequest) -> JsonResponse:
        if files:
            profile.avatar = files["file"]
            if form := self.validate_update_profile_photo_form(request, profile):
                form.save()
                return JsonResponse(data={
                    "message": "Photo successfully updated"
                },
                    status=200
                )
        return JsonResponse(data={
            "message": "Bad request"
        },
            status=400
        )

    def update_status(self, profile: Profile, status: str) -> JsonResponse:
        if status is None:
            return JsonResponse(data={
                "message": "Bad request"
            },
                status=400
            )

        profile.status = status
        profile.save()
        return JsonResponse(data={
            "message": "Status successfully updated"
        },
            status=200
        )


user_service = UserService()
