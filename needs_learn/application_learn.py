from learn_data_collect import LearnDataCollect
from learn_data_split import LearnDataSplit
from learn import Learn
from service_learn import ServiceLearn

ldc = LearnDataCollect()
lds = LearnDataSplit()
l = Learn()

service_learn = ServiceLearn(ldc, lds, l)
print(service_learn.execute())