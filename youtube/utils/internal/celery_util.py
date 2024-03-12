from settings.env_variables import YOUTUBE_SEARCH_TERMS, YOUTUBE_INDEX_ALIAS
from youtube.utils.internal.elastic_search_utils import ElasticSearchUtil
from datetime import datetime, timedelta


class SyncLatestYtVideo:

    @classmethod
    def sync_video(cls):
        """
        todo: try except , looping
        """
        current_time = datetime.now()
        published_before = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        previous_job_time = current_time - timedelta(minutes=1)  # last job running time
        published_after = previous_job_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        field = "nextPageToken,items(id(videoId),snippet(publishedAt,title,description,thumbnails))"
        response_list = []
        for terms in YOUTUBE_SEARCH_TERMS:
            q = terms
            from youtube.utils.external.youtube_api_utils import YoutubeApiClient
            try:
                response = YoutubeApiClient().search(part="id,snippet", type='video', max_results=50, q=q, field=field,
                                                     published_after=published_after, published_before=published_before,
                                                     event_type="completed")
            except Exception as e:
                print(e)
                continue
            response_list.append(response)
        es_doc_list = cls.build_es_doc(response_list)
        ElasticSearchUtil().populate_bulk_index(es_doc_list)

    @classmethod
    def build_es_doc(cls, response_list):
        """
        Function for building es doc structure data from youtube api response.
        """
        es_doc_list = []
        for response in response_list:
            items_list = response.get("items") or []
            for data in items_list:
                video_id = data.get("id", {}).get("videoId")
                snippet = data.get("snippet")
                publish_time = snippet.get("publishedAt")

                # Parse the timestamp string using strptime() and specify the format
                publish_time_obj = datetime.strptime(publish_time, '%Y-%m-%dT%H:%M:%SZ')
                # Format the datetime object as per the desired format
                formatted_published_timestamp = publish_time_obj.strftime('%Y-%m-%d %H:%M:%S')

                current_datetime = datetime.now().replace(microsecond=0)
                current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

                es_doc = {
                    "video_id": video_id,
                    "publish_time": formatted_published_timestamp,
                    "title": snippet.get("title"),
                    "description": snippet.get("description"),
                    "created_at": current_datetime,
                    "thumbnails": snippet.get("thumbnails")
                }
                es_doc_list.append({
                    "index_name": YOUTUBE_INDEX_ALIAS,
                    "document_id": video_id,
                    "event_type": "index",
                    "es_document": es_doc
                })
        return es_doc_list

