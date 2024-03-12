import googleapiclient.discovery
from settings.env_variables import YOUTUBE_API_KEY_LIST


# List of YouTube API keys
API_KEYS = YOUTUBE_API_KEY_LIST

api_service_name = "youtube"
api_version = "v3"
key_index = 0  # global variable so that it's value will be preserved for subsequent call


class YoutubeApiClient:
    global key_index

    def __init__(self):
        self.current_key_index = key_index

    def get_service(self):
        # Select the current API key
        api_key = API_KEYS[self.current_key_index]

        # Create a YouTube service object
        youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
        return youtube

    def execute_request(self, request):
        try:
            # Execute the request
            response = request.execute()
            return response
        except Exception as e:
            # If quota is exceeded or other errors occur, switch to the next API key and retry
            if 'quotaExceeded' in str(e):
                self.rotate_key()
                return self.execute_request(request)
            else:
                # Handle other errors here
                raise

    def rotate_key(self):
        # Rotate to the next API key
        global key_index
        key_index = (key_index + 1) % len(API_KEYS)
        self.current_key_index = key_index

    def search(self, part, type=None, q=None, max_results=None, field=None, published_after=None,
               published_before=None, event_type=None):
        youtube_api_handler = YoutubeApiClient()
        youtube_client = youtube_api_handler.get_service()

        request = youtube_client.search().list(
            part=part, type=type, q=q,
            maxResults=max_results, publishedAfter=published_after, fields=field, publishedBefore=published_before,
            eventType=event_type,
        )
        response = youtube_api_handler.execute_request(request)
        return response
