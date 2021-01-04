from dataclasses import dataclass
from needs.views.needs_repository import NeedsSelect
from needs.views.needs_topic import (
    TopicDocumentsAndDictionaryAndCorpus,
    TopicNumberConsiderGraph,
    TopicModel,
)
from needs.models import Needs


@dataclass
class ServiceTopicNumberConsiderGraph:
    needs_select: NeedsSelect
    topic_documents_dictionary_corpus: TopicDocumentsAndDictionaryAndCorpus
    topic_number_consider_graph: TopicNumberConsiderGraph

    def execute(self):
        needs_data_list = self.needs_select.topic_data(Needs)
        documents, dictionary, corpus = self.topic_documents_dictionary_corpus.create(
            needs_data_list
        )
        graph = self.topic_number_consider_graph.create(documents, dictionary, corpus)
        return graph


@dataclass
class ServiceTopicClassify:
    topic_number: int
    needs_select: NeedsSelect
    topic_documents_dictionary_corpus: TopicDocumentsAndDictionaryAndCorpus
    topic_model: TopicModel

    def execute(self):
        needs_data_list = self.needs_select.topic_data(Needs)
        (
            dictionary,
            corpus,
        ) = self.topic_documents_dictionary_corpus.dictionary_corpus_only_create(
            needs_data_list
        )

        topics = self.topic_model.present(self.topic_number, dictionary, corpus)
        return topics
