import os

LEARNING_DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/learn_data/*.csv"
USE_URL = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"
NUM_CLASSES = 2

SAVE_MODEL_PATH = (
    os.path.dirname(os.path.abspath(__file__)) + "/../needs_get/model/get_needs.h5"
)
