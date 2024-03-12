import os
YOUTUBE_API_KEY_LIST = ['AIzaSyBg4Iuiopdof2-VzzUVCKcJJev07okKe94', 'AIzaSyCr5wK6lfD7NZesTmwlxXusowE7FyLwzus']
YOUTUBE_SEARCH_TERMS = ["football", "official"]
YOUTUBE_INDEX_ALIAS = "fam_pay_v1" # todo
ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST", 'localhost')
ELASTICSEARCH_PORT = int(os.environ.get("ELASTICSEARCH_PORT", 9200))
ELASTICSEARCH_USER = os.environ.get("ELASTICSEARCH_USER", 'elastic')
ELASTICSEARCH_PASS = os.environ.get("ELASTICSEARCH_PASS", 'YW03T5qHoHBgOKPcSPs7')


