"""Custom pagination."""
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """Custom pagination that returns structured pagination metadata."""
    page = 1
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('code', 200),
            ('message', 'success'),
            ('data', OrderedDict([
                ('list', data),
                ('pagination', OrderedDict([
                    ('page', self.page.number),
                    ('page_size', self.page.paginator.per_page),
                    ('total', self.page.paginator.count),
                    ('total_pages', self.page.paginator.num_pages),
                    ('has_next', self.page.has_next()),
                    ('has_prev', self.page.has_previous()),
                ])),
            ])),
        ]))
