from settings.env_variables import YOUTUBE_INDEX_ALIAS
from youtube.utils.internal.elastic_search_utils import ElasticSearchUtil
from youtube.builders.get_latest_video_response_builder import BaseResponseBuilder


class GetLatestVideosUtils:

    @classmethod
    def get_latest_video(cls, **kwargs):
        size = kwargs.get("size")
        page = kwargs.get("page")
        _from = (page - 1) * size
        raw_query = {
            "query": {
                "match_all": {}
            },
            "sort": [
                {
                    "publish_time": {
                        "order": "desc"
                    }
                }
            ],
            "size": size,
            "from": _from
        }
        search_results, raw_query = ElasticSearchUtil().get_es_doc(index_name=YOUTUBE_INDEX_ALIAS,
                                                                   criteria=raw_query, doc_type=None)
        es_response = search_results.to_dict()
        response = BaseResponseBuilder(es_response, pagination_dict=kwargs).get_video_list_response()
        return response
