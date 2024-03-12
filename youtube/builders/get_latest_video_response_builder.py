from rest_framework.utils.urls import replace_query_param


class BaseResponseBuilder:
    """Base class for building get and search api response """

    def __init__(self, es_response_data=None, pagination_dict=None):
        super().__init__()
        self.es_response_data = es_response_data or {}
        self.es_doc_list = self.es_response_data.get("hits", {}).get("hits") or []
        self.total_count = self.es_response_data.get("hits", {}).get("total", {}).get("value")
        self.pagination_dict = pagination_dict or {}

    def get_next_link(self):
        """function for getting next url for pagination"""
        page = self.pagination_dict.get('page')
        size = self.pagination_dict.get('size')
        request = self.pagination_dict.get('request')
        if isinstance(page, int) and isinstance(size, int) and request:
            if (self.total_count - page * size) <= 0:
                return None
            url = request.build_absolute_uri()
            next_page_number = page + 1
            url = replace_query_param(url, 'size', size) if size else url
            return replace_query_param(url, 'page', next_page_number)
        return None

    def get_previous_link(self):
        page = self.pagination_dict.get('page')
        size = self.pagination_dict.get('size')
        request = self.pagination_dict.get('request')
        if isinstance(page, int) and isinstance(size, int) and request:
            if page <= 1:
                return None
            url = request.build_absolute_uri()
            next_page_number = page - 1
            return replace_query_param(url, 'page', next_page_number)
        return None

    def get_video_list_response(self):
        result_list = []
        for es_doc in self.es_doc_list:
            source = es_doc.get("_source")
            result_list.append(
                {
                    "video_id": source.get("video_id"),
                    "title": source.get("title"),
                    "description": source.get("description"),
                    "publish_time": source.get("publish_time"),
                }
            )

        response = {
            "total_count": self.total_count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": result_list
        }
        return response
