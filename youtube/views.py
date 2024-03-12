from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from youtube.utils.internal.elastic_search_utils import ElasticSearchUtil
from youtube.utils.internal.get_videos_utils import GetLatestVideosUtils
from youtube.utils.internal.search_video_utils import SearchVideosUtils


class GetLatestVideosView(APIView):

    def get(self, request):
        try:
            size = request.query_params.get("size") and int(request.query_params.get("size")) or 10
            page = request.query_params.get("page") and int(request.query_params.get("page")) or 1
            response = GetLatestVideosUtils.get_latest_video(size=size, page=page, request=request)
            return Response(data=response, status=HTTP_200_OK)
        except Exception as e:
            print("[GetLatestVideosView] Exception occurred ", e)
            return Response(data={"status": "error", "message": "Something went wrong"},
                            status=HTTP_400_BAD_REQUEST)


class SearchVideosView(APIView):

    def get(self, request):
        try:
            size = request.query_params.get("size") and int(request.query_params.get("size")) or 10
            page = request.query_params.get("page") and int(request.query_params.get("page")) or 1
            order = request.query_params.get("order")
            title = request.query_params.get("title")
            desc = request.query_params.get("desc")
            term = request.query_params.get("term")
            response = SearchVideosUtils.search_video(size=size, page=page, request=request,
                                                      order=order, title=title, desc=desc, term=term)
            return Response(data=response, status=HTTP_200_OK)
        except Exception as e:
            print("[SearchVideosView] Exception occurred ", e)
            return Response(data={"status": "error", "message": "Something went wrong"},
                            status=HTTP_400_BAD_REQUEST)


class CreateESIndexView(APIView):

    def post(self, request):
        try:
            index_name = request.data.get("index_name")
            mapping = request.data.get("mapping")
            ElasticSearchUtil().create_es_index(index_name=index_name, mapping=mapping)
            return Response(data={"message": "success"}, status=HTTP_200_OK)
        except Exception as e:
            print("[CreateESIndexView] Exception occurred ", e)
            return Response(data={"status": "error", "message": "Something went wrong"},
                            status=HTTP_400_BAD_REQUEST)
