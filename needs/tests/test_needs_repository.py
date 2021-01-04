from django.test import TestCase
import datetime
from needs.models import Needs
from needs.views.needs_repository import NeedsSelect
from needs.views.needs_dto import NeedsEntity


class TestNeedsRepository(TestCase):
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

    def test_DBに格納されているデータを全件抽出(self):
        td1 = Needs(
            id=1,
            sentence="test",
            date=datetime.datetime(2018, 2, 1, 12, 15, 30, 2000),
            label=0,
        )
        td2 = Needs(
            id=2,
            sentence="test2",
            date=datetime.datetime(2020, 2, 1, 12, 15, 30, 2000),
            label=1,
        )
        td1.save()
        td2.save()

        target = NeedsSelect()
        actual = target.all(Needs)

        ex1 = NeedsEntity(
            nid=1,
            sentence="test",
            date=datetime.datetime(2018, 2, 1, 12, 15, 30, 2000),
            label=0,
        )
        ex2 = NeedsEntity(
            nid=2,
            sentence="test2",
            date=datetime.datetime(2020, 2, 1, 12, 15, 30, 2000),
            label=1,
        )
        expect = [ex2, ex1]
        self.assertEqual(actual, expect)

    def test_DBに格納されているデータを100件抽出(self):
        td_list = []
        for i in range(101):
            i = i + 1
            if i % 2 == 0:
                td = Needs(
                    sentence="test" + str(i),
                    date=datetime.datetime(2018 + i, 2, 1, 12, 15, 30, 2000),
                    label=1,
                )
                td_list.append(
                    NeedsEntity(
                        nid=i,
                        sentence="test" + str(i),
                        date=datetime.datetime(2018 + i, 2, 1, 12, 15, 30, 2000),
                        label=1,
                    )
                )
            else:
                td = Needs(
                    sentence="test" + str(i),
                    date=datetime.datetime(2018 + i, 2, 1, 12, 15, 30, 2000),
                    label=0,
                )
            td.save()

        target = NeedsSelect()
        actual = target.top_limit(Needs)
        # 配列を反転
        expect = td_list[::-1]

        expect = expect[:100]
        self.assertEqual(actual, expect)
