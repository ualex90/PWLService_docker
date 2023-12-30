from rest_framework.pagination import PageNumberPagination


class PaymentPaginator(PageNumberPagination):
    page_size = 5
