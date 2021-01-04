from django.test import TestCase
from needs.views.needs_topic import TopicDocumentsAndDictionaryAndCorpus
from needs.views.needs_dto import NeedsTopicDocument
import gensim


class TestTopicDocumentsAndDictionaryAndCorpus(TestCase):
    # テストクラスが初期化される際に一度だけ呼ばれる (python2.7以上)
    @classmethod
    def setUpClass(cls):
        pass

    # テストクラスが解放される際に一度だけ呼ばれる (python2.7以上)
    @classmethod
    def tearDownClass(cls):
        pass

    # テストメソッドを実行するたびに呼ばれる
    def setUp(self):
        pass

    # テストメソッドの実行が終わるたびに呼ばれる
    def tearDown(self):
        pass

    def test_形態素解析して動詞_名詞_形容詞の語幹を抽出する(self):
        td1 = NeedsTopicDocument("私は人間です。きつくない。遊びます")
        td2 = NeedsTopicDocument("テストです。")

        test_data = [td1, td2]

        target = TopicDocumentsAndDictionaryAndCorpus()
        actual = target._documents_create(test_data)

        expect = [["人間", "きつい", "遊ぶ"], ["テスト"]]
        self.assertEqual(actual, expect)

    def test_アルファベット_記号_数字は削除(self):
        td1 = NeedsTopicDocument("私は人間です。きつくない。遊びます。test 123 !\"#$%&'()\\=")
        td2 = NeedsTopicDocument("テストです。")

        test_data = [td1, td2]
        target = TopicDocumentsAndDictionaryAndCorpus()
        actual = target._documents_create(test_data)

        expect = [["人間", "きつい", "遊ぶ"], ["テスト"]]
        self.assertEqual(actual, expect)

    def test_英数字記号を削除(self):
        test_data = "私は人間です。きつくない。遊びます。test 123 !\"#$%&'()\\="
        target = TopicDocumentsAndDictionaryAndCorpus()
        actual = target._format_text(test_data)

        expect = "私は人間です。きつくない。遊びます。  "
        self.assertEqual(actual, expect)

    def test_トピックモデル用の辞書とコーパスを作成(self):
        td1 = NeedsTopicDocument("私は人間です。きつくない。遊びます")
        td2 = NeedsTopicDocument("テストです。")

        test_data = [td1, td2]
        target = TopicDocumentsAndDictionaryAndCorpus()
        actual_dcuments, actual_dictionary, actual_corpus = target.create(test_data)
        actual = [actual_dcuments, type(actual_dictionary), type(actual_corpus)]
        expect = [
            [["人間", "きつい", "遊ぶ"], ["テスト"]],
            gensim.corpora.dictionary.Dictionary,
            gensim.interfaces.TransformedCorpus,
        ]
        self.assertEqual(actual, expect)
