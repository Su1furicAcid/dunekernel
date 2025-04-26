import pygrading as gg
from pygrading.verdict import Verdict
import os


def run(job: gg.Job, testcase: gg.TestCases.SingleTestCase) -> dict:
    config = job.get_config()

    # 创建一个结果对象
    result = {'name': testcase.name, 'score': 0, 'verdict': Verdict.WrongAnswer}

    # 获取测试用例的输入和输出文件路径
    input_file = testcase.input_src
    output_file = testcase.output_src

    # 读取输入文件内容
    with open(input_file, 'r') as f:
        input_str = f.read()

    # 执行程序
    run_file = config['exec_src']
    run_result = gg.utils.exec(run_file, input_str=input_str)

    # 检查返回码
    if run_result.returncode != config['return_code']:
        result['verdict'] = Verdict.RuntimeError
        result['stderr'] = run_result.stderr
        result['return_code'] = run_result.returncode
        return result

    # 读取期望输出
    with open(output_file, 'r') as f:
        expected_output = f.read()

    # 比较输出
    if gg.utils.compare_str(expected_output, run_result.stdout):
        result['verdict'] = Verdict.Accept
        result['score'] = testcase.score
    else:
        result['verdict'] = Verdict.WrongAnswer
        result['score'] = 0

    return result