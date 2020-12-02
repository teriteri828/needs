from const import MYSITE_DIR, MYSITE_NAME
from dataclasses import dataclass
import sys
import os
import django

sys.path.append(MYSITE_DIR)
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", MYSITE_NAME + ".settings"
)  # 自分のsettings.py
django.setup()

from needs.models import Needs
from typing import List
from needs_get_dto import TweetsDto


@dataclass
class DataInsert:
    def execute(self, needs_list: List[TweetsDto]):
        for needs in needs_list:
            n = Needs(sentence=needs.text, date=needs.datetime_jst, label=needs.label)
            n.save()
        return True
