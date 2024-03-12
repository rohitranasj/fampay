from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Search

from settings.env_variables import ELASTICSEARCH_HOST, ELASTICSEARCH_USER, ELASTICSEARCH_PORT, ELASTICSEARCH_PASS


class QueryBuilder(object):

    def __init__(self, es_client, criteria):
        self.dsl_search = Search(using=es_client)
        self.criteria = criteria

    def search(self, index_name=None, doc_type=None):
        s = self.dsl_search.index(index_name).doc_type(doc_type).update_from_dict(self.criteria)
        return s

    @classmethod
    def sort_(cls, s, sorting_list):
        return s.sort(*sorting_list)

    @classmethod
    def pagination(cls, s, size, from_):
        size = size if isinstance(size, int) else 10
        from_ = from_ if from_ else 0
        return s.extra(size=size, from_=from_)


class ElasticSearchUtil:
    """
    Class for interacting with base Elasticsearh package.
    support searching and indexing of es document
    """

    def __new__(cls, *args, **kwargs):
        """creates only one instance of ElasticSearchUtil class"""
        if not hasattr(cls, 'es_client'):
            orig = super(ElasticSearchUtil, cls)
            cls._instance = orig.__new__(cls)
            cls.es_client = Elasticsearch(
                hosts=[{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT, 'scheme': 'http'}],
                http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASS),
                verify_certs=False
            )
            print("ping resp ", cls.es_client.ping())

        return cls._instance

    def get_es_doc(self, index_name, doc_type, criteria, sorting_list=None, pagination_dict=None):
        """
        Function for searching es doc
        """
        query_result_obj = QueryBuilder(es_client=self.es_client, criteria=criteria).search(
            index_name=index_name, doc_type=doc_type)
        size = pagination_dict.get('size') if pagination_dict else 10
        from_ = pagination_dict.get('_from') if pagination_dict else 0
        sorting_list = sorting_list or None
        query_result_obj = QueryBuilder.pagination(s=query_result_obj, size=size, from_=from_)
        if sorting_list:
            query_result_obj = QueryBuilder.sort_(s=query_result_obj, sorting_list=sorting_list)
        return query_result_obj.execute(), query_result_obj.to_dict()

    def create_bulk_document_list(self, document_list):
        documents_data_list = []
        for document in document_list:
            documents_data_list.append(
                {
                    "_index": document.get("index_name"),
                    "_id": document.get("document_id"),
                    "_op_type": document.get("event_type"),
                    "_source": document.get("es_document")

                }
            )
        return documents_data_list

    def populate_bulk_index(self, documents_data_list):
        """
        Function for indexing es documents.
        :param documents_data_list: Populate data with incoming json json list.
        """
        if not documents_data_list:
            return
        documents_data_list = self.create_bulk_document_list(documents_data_list)
        result = helpers.bulk(self.es_client, actions=documents_data_list)
        print("populate_bulk_index ", result)

    def create_es_index(self, index_name, mapping):
        # Create an Elasticsearch client instance
        self.es_client.indices.create(index=index_name, body=mapping)

