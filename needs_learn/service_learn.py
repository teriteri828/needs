from dataclasses import dataclass
from learn_data_collect import LearnDataCollect
from learn_data_split import LearnDataSplit
from learn import Learn

@dataclass
class ServiceLearn:
    learn_data_collect: LearnDataCollect
    learn_data_split: LearnDataSplit
    lean: Learn
    def execute(self):
        ldc = self.learn_data_collect.execute()
        X_train, X_test, y_train, y_test = self.learn_data_split.execute(ldc)
        status = self.lean.execute(X_train, X_test, y_train, y_test)
        return status