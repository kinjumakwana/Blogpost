from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from collections import OrderedDict
# from cursor_pagination import CursorPaginator

class Mycustompagination(CursorPagination):
    page_size=2
    ordering = '-created'
    page_size_query_param = 'page_size'
    max_page_size = 50
    cursor_query_param='cu'  

    # def get_paginated_response(self, data):
    #     response = Response(data)
    #     response['count'] = self.page.paginator.count
    #     response['next'] = self.get_next_link()
    #     response['previous'] = self.get_previous_link()
    #     return response