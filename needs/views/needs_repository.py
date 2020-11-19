from dataclasses import dataclass
from needs.views.needs_dto import NeedsEntity


@dataclass
class NeedsSelect:
    def all(self, models):
        needs_data_list = models.objects.all()
        ret = []
        for needs in needs_data_list:
            ret.append(
                NeedsEntity(
                    nid=needs.id,
                    sentence=needs.sentence,
                    date=needs.date.replace(tzinfo=None),
                )
            )
        return ret
