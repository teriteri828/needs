from dataclasses import dataclass
from needs.views.needs_dto import NeedsEntity


@dataclass
class NeedsSelect:
    def all(self, models):
        needs_data_list = models.objects.all().order_by("-id")
        ret = []
        for needs in needs_data_list:
            ret.append(
                NeedsEntity(
                    nid=needs.id,
                    sentence=needs.sentence,
                    date=needs.date.replace(tzinfo=None),
                    label=needs.label,
                )
            )
        return ret

    def top_limit(self, models):
        needs_data_list = models.objects.all().order_by("-id")[:100]
        ret = []
        for needs in needs_data_list:
            ret.append(
                NeedsEntity(
                    nid=needs.id,
                    sentence=needs.sentence,
                    date=needs.date.replace(tzinfo=None),
                    label=needs.label,
                )
            )
        return ret

    def learn_data_get(self, models):
        needs_data_list = models.objects.all().order_by("-id")[:20]
        ret = []
        for needs in needs_data_list:
            ret.append(
                NeedsEntity(
                    nid=needs.id,
                    sentence=needs.sentence,
                    date=needs.date.replace(tzinfo=None),
                    label=needs.label,
                )
            )
        return ret
