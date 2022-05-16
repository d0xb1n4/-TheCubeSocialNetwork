from rest_framework.response import Response
from rest_framework import status


class CustomResponse:
    def __init__(self, data: dict):
        self.data = data

    def bad(self) -> Response:
        data = {
            'status': 'ERR',
            'data': self.data
        }
        return Response(
            data=data,
            status=status.HTTP_400_BAD_REQUEST
        )

    def good(self) -> Response:
        data = {
            'status': 'OK',
            'data': self.data
        }
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )


class CustomErrors:
    def __init__(self, field: str):
        self.field = field

    def object_not_found_error(self) -> dict:
        return {self.field: ['Объекта не существует.']}

    def object_already_exists_error(self):
        return {self.field: ['Объект с такими параметрами уже существует.']}

    def no_permission_error(self):
        return {self.field: ['Недостаточно прав доступа.']}

