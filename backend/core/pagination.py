from rest_framework.pagination import PageNumberPagination


class LimitPagePagination(PageNumberPagination):
    """
    Ограничивает количество элементов на странице,
        основаваясь на параметре запроса 'limit'.
    """
    page_size_query_param = 'limit'
