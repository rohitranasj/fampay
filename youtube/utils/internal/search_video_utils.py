from settings.env_variables import YOUTUBE_INDEX_ALIAS
from youtube.builders.get_latest_video_response_builder import BaseResponseBuilder
from youtube.constants import ORDERING_MAP
from youtube.utils.internal.elastic_search_utils import ElasticSearchUtil


class SearchVideosUtils:

    @classmethod
    def search_video(cls, **kwargs):
        size = kwargs.get("size")
        page = kwargs.get("page")
        _from = (page - 1) * size
        pagination_dict = {"size": kwargs.get("size"), "_from": _from}
        sorting_list = cls.get_sorting_list(kwargs.get("order"))
        criteria = cls.get_query_dict(**kwargs)

        search_results, raw_query = ElasticSearchUtil().get_es_doc(index_name=YOUTUBE_INDEX_ALIAS,
                                                                   criteria=criteria, doc_type=None,
                                                                   sorting_list=sorting_list,
                                                                   pagination_dict=pagination_dict)
        response = search_results.to_dict()
        response = BaseResponseBuilder(response, pagination_dict=kwargs).get_video_list_response()

        return response

    @classmethod
    def get_sorting_list(cls, order):
        return [ORDERING_MAP.get(order)]

    @classmethod
    def get_query_dict(cls, **query_param):
        title = query_param.get("title")
        desc = query_param.get("desc")
        term = query_param.get("term")
        query_dict = {
            "title": {
                "match": {
                    "title": title
                }
            },
            "desc": {
                "match": {
                    "description": desc
                }
            },
            "term": {
                "multi_match": {
                    "query": term,
                    "fields": [
                        "title",
                        "description"
                    ]
                }
            }
        }
        criteria = {"query": {
            "bool": {
                "must": [
                ]
            }
        }}
        valid_key = ["title", "desc", "term"]
        for key, value in query_param.items():
            if key in valid_key and not isinstance(value, type(None)):
                query_dict = query_dict.get(key)
                criteria["query"]["bool"]["must"].append(query_dict)
        return criteria
