import urllib.parse as urlparse
from urllib.parse import parse_qs, urlencode, quote_plus
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from rest_framework.exceptions import NotFound


class LargePagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 1000


class DefaultPagination(PageNumberPagination):
    """
    Default pagination class.
    in case of invalid page, empty list will be returned.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def paginate_queryset(self, queryset, request, view=None):
        """Checking NotFound exception"""
        try:
            return super(DefaultPagination, self).paginate_queryset(queryset, request, view=view)
        except NotFound:  # intercept NotFound exception
            return list()

    def get_paginated_response(self, data):
        """Avoid case when self does not have page properties for empty list"""
        if hasattr(self, 'page') and self.page is not None:
            return Response(OrderedDict([
                ('count', self.page.paginator.count),
                ('next', self.get_next_link()),
                ('pages', self.page.paginator.num_pages),
                ('previous', self.get_previous_link()),
                ('results', data)
            ]))
        else:
            return Response(OrderedDict([
                ('count', None),
                ('next', None),
                ('previous', None),
                ('results', data)
            ]))


# Custom Pagination
def parse_and_update_url(request, url, page_counter):
    """this will get existing value of page"""
    uri = request.build_absolute_uri("")
    parsed = urlparse.urlparse(url)
    page = parse_qs(parsed.query)
    page['page'] = str(page_counter)
    result = urlencode(page, doseq=True)
    return "{}?{}".format(uri, result)


def generate_pagination(response, request):
    """Here to generate pagination for event list, generate url"""
    page = int(request.GET.get("page", "1"))
    url = request.build_absolute_uri()
    page_increment = page + 1
    page_decrement = page - 1
    per_page = 10
    reminder = (len(response) % per_page)
    if reminder > 0:
        total_pages = int((len(response) / per_page) + 1)
    else:
        total_pages = int((len(response) / per_page))
    page_range = range(1, total_pages + 1)
    next_page = parse_and_update_url(request, url, page_increment) if page_increment in page_range else None
    prev_page = parse_and_update_url(request, url, page_decrement) if page_decrement in page_range else None
    offset = (page * per_page) - per_page
    limit = offset + per_page
    entry_list = response[offset:limit]
    context = {"count": len(response), "next": next_page, "previous": prev_page, "pages": total_pages, "results": entry_list}
    return context
