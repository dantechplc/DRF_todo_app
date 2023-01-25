from rest_framework import pagination


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'count'
    page_query_param = 'p'
    max_page_size = 5
