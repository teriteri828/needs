from dataclasses import dataclass
import pandas as pd
import glob
from const import LEARNING_DATA_DIR

@dataclass
class LearnDataCollect:
    def execute(self,):
        file_path_list = glob.glob(LEARNING_DATA_DIR)
        df_learn = pd.DataFrame()
        df_temp = pd.DataFrame()
        for file_path in file_path_list:
            if "temp" in file_path:
                continue
            df_temp = pd.read_csv(file_path)
            df_temp = df_temp.rename(columns={"tweet": "text"})
            df_learn = pd.concat([df_learn, df_temp], axis=0)

        df_learn = df_learn.reset_index()[["text", "needs"]]
        # 空白のレコードは、USEのエンコーダーでエラーになる
        df_learn = df_learn.dropna()
        # tweetで重複を削除。削除するときは、最新をほう残す
        df_learn.drop_duplicates(subset="text", keep="last", inplace=True)
        return df_learn
