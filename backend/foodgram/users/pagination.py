from rest_framework.pagination import PageNumberPagination

class PaginationLimit(PageNumberPagination):
    page_size_query_param = 'limit'