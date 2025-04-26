import os
import tempfile

KERNEL_CONFIG = {
    'submit_dir': '/coursegrader/submit',
    'testcase_dir': '/coursegrader/testdata',
    'return_code': 0,
    "exec_dir": tempfile.mkdtemp(),
    "source_ext": ".ml",
    "exec_src": ""
}