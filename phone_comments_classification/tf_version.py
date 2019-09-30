import os
from tensorflow.python.client import device_lib
import tensorflow as tf

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "99"

if __name__ == "__main__":
    print(tf.__version__)
    print(device_lib.list_local_devices())




