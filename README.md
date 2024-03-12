## Getting Started

1. clone the repository into your local machine.
2. cd into the project root folder.
3. Setting up Elasticsearch
    - run the command: `docker pull docker.elastic.co/elasticsearch/elasticsearch:8.12.2`
    - run the command: `docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.12.2`
    - The above command will pull the es image and build a continer from it.
    - copy the generated password visible on the terminal into the docker_env.env file 
4. Hit the below curl to create a es index which will be used in storing videos data. 
    Make sure to update the password with
your elastic user password.

```
curl --location --request PUT 'http://localhost:9200/fam_pay_v1' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic ZWxhc3RpYzphc2RmYXNkZg==' \
--data-raw '{
    "settings": {
        "number_of_shards": "3",
        "number_of_replicas": "1"
    },
    "mappings": {
        "dynamic": "false",
        "properties": {
            "@timestamp": {
                "type": "date"
            },
            "created_at": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss"
            },
            "publish_time": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss"
            },
            "video_id": {
                "type": "keyword"
            },
            "title": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "description": {
                "type": "text"
            },
            "thumbnail": {
                "properties": {
                    "default": {
                        "properties": {
                            "url": {
                                "type": "text"
                            },
                            "width": {
                                "type": "integer"
                            },
                            "height": {
                                "type": "integer"
                            }
                        }
                    }
                }
            }
        }
    }
}'
```

5. Building project 
    - from project root folder type: docker-compose up
    - this will setup redis, celery-beat, celery-worker and django container. 


## Stack Used:
Web Framework - Django
DB - ElasticSearch
Celery worker and beat for periodic task
Queue - Redis

## Flow Overview:
- Our Celery beat will make sure to send a task in redis queue after every 60s.
- This task will be picked up by celery worker which will call the youtube api to fetch videos uploaded in last 1 minute for a given terms
- This task also handles in indexing the required videos data into our elastic search index. 
- From this elastic search index we can get latest video uploaded or perform full text search. 


## Apis:
1. Get latest Videos: 
- endpoint: http://127.0.0.1:8000/yt/get-latest-videos/?page=1&size=10
- it support pagination you can pass page and size param to tweak the result obtained in a page. 

2. Search Video Api:
- endpoint: http://127.0.0.1:8000/yt/search-videos/?order=newest&page=1&size=5&term=ncaawomensbasketball smoke&title=football&desc=match
- Supports pagination, sorting and filtering with full text search capabilities. 

Query Param Meanings 
- order: possible values are (newest, oldest, title, -title)
- title: possible values are (space separted string to search in the title field of videos)
- desc: possible values are (space separted string to search in the description field of videos)
- term: possible values are (space separted string to search in the description and title field of videos)



## Other Features

1- Multipel api key support:
It support use of multiple api keys using api key rotation 
logic: whenever api key quota got exhuasted we will shift the index to use the next api key for subsequent request. 

2- Dashboard api for filtering , searching 
endpoint: http://127.0.0.1:8000/yt/search-videos/?order=newest&page=1&size=5&term=ncaawomensbasketball smoke&title=football&desc=match

3 - Full text search support i.e "title=football smoke" will match to all videos where title field contain either football or smoke
endpoint: http://127.0.0.1:8000/yt/search-videos/?order=newest&page=1&size=5&term=ncaawomensbasketball smoke&title=football&desc=match


