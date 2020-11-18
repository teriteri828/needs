from django.test import TestCase

from ..views.morphological_wrods import MorphologicalWords, BackDataMorphologicalWords
from ..views.search_dto import (
    SearchRequest,
    MorphologicalSearchWords,
    MorphologicalBackDataWords,
)
from ..views.search_repository import Knowledge


class TestMorphologicalWrods(TestCase):
    def test_文字列から名詞のみを抽出しリスト化して返却する(self):
        test_data = "私は人間です"
        target = MorphologicalWords()
        actual = target.create(SearchRequest(test_data))
        expect = MorphologicalSearchWords(["私", "人間"])

        self.assertEqual(actual, expect)

    def test_空白が混じった文字列から名詞のみを抽出しリスト化して返却する(self):
        test_data = "私　人間　"
        target = MorphologicalWords()
        actual = target.create(SearchRequest(test_data))
        expect = MorphologicalSearchWords(["私", "人間"])

        self.assertEqual(actual, expect)


class TestBackDataMorphologicalWords(TestCase):
    def test_文字列から名詞のみを抽出しリスト化して返却する(self):
        td1 = Knowledge(id=100, search_word="私は人間です",)
        td2 = Knowledge(id=1, search_word="私は車が好きです",)
        test_data = [td1, td2]
        target = BackDataMorphologicalWords()
        actual = target.create(test_data)
        expect = [
            MorphologicalBackDataWords(100, ["私 人間"]),
            MorphologicalBackDataWords(1, ["私 車 好き"]),
        ]

        self.assertEqual(actual, expect)
