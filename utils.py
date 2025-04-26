import sys
import os
import pygrading as gg
import re
from config import KERNEL_CONFIG


def Singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@Singleton
class Env:
    def __init__(self):
        self.is_debug = False
        self.config = KERNEL_CONFIG.copy()

    def load_config(self, config_src=None):
        if os.environ.get("CONFIG_SRC"):
            self.config.update(gg.load_config(os.environ.get("CONFIG_SRC")))
        if not config_src:
            config_src = os.path.join(self.config['testcase_dir'], "config.json")
        if os.path.exists(config_src):
            self.config.update(gg.load_config(config_src))
        self.is_debug = self.config.get("debug", False)
        if "testcase_num" not in self.config:
            self.config["testcase_num"] = count_testcase(self.config["testcase_dir"])
        self.config["exec_src"] = os.path.join(self.config["exec_dir"], "exec.out")

        loge(self.config)
        return self

    def __getitem__(self, item):
        return self.config[item]

    def __setitem__(self, key, value):
        self.config[key] = value


def loge(*args, **kwargs):
    if Env().is_debug:
        print(*args, file=sys.stderr, flush=True, **kwargs)


def count_testcase(input_dir: str):
    input_pattern = re.compile(r"input\d+\.txt")
    files = os.listdir(input_dir)
    testcase_num = len(list(filter(lambda x: input_pattern.match(x), files)))
    return testcase_num