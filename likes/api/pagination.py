from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

__all__ = (
    'MetaResponsePagination',
)


class MetaResponsePagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'meta': {
                'count': self.page.paginator.count,
                'page': self.page.number,
                'perPage': self.get_page_size(self.request)
            },
            'data': data
        })
