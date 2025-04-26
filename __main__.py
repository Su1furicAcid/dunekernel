from postwork import postwork
from prework import prework
from run import run
import pygrading as gg
from utils import Env


if __name__ == '__main__':
    env = Env()
    env.load_config()
    job = gg.Job(prework=prework, run=run, postwork=postwork, config=env.config)
    job.start()
    job.print()
