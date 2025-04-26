import pygrading as gg
import os
from exception import CG
from utils import Env
import json
import shutil

@CG.catch
def prework(job: gg.Job):
    config = job.get_config()

    if len(os.listdir(config['submit_dir'])) == 0:
        raise CG.CompileError("No submit file")
    
    # 创建一个临时dune项目
    project_dir = os.path.join(config['exec_dir'], "dune_project")
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
    os.chdir(project_dir)
    create_dune_cmd = "dune init project test_project"
    create_dune_result = gg.utils.exec(create_dune_cmd)
    if create_dune_result.returncode != 0:
        raise CG.CompileError(create_dune_result.stdout + '\n' + create_dune_result.stderr)
    
    # 把当前 python 文件夹路径下 dune_config 里对应的文件复制到项目目录
    with open(os.path.join("dune_config", "config.json"), "r") as f:
        config_json = json.load(f)
        for file in config_json["files"]:
            src = os.path.join("dune_config", file)
            dst = os.path.join(project_dir, file)
            if not os.path.exists(os.path.dirname(dst)):
                os.makedirs(os.path.dirname(dst))
            shutil.copy(src, dst)

    # 复制提交文件到项目的 /lib 目录
    for file in os.listdir(config["submit_dir"]):
        src = os.path.join(config["submit_dir"], file)
        dst = os.path.join(project_dir, "lib", file)
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        shutil.copy(src, dst)

    # 编译项目
    compile_cmd = "dune build"
    compile_result = gg.utils.exec(compile_cmd)
    if compile_result.returncode != 0:
        raise CG.CompileError(compile_result.stdout + '\n' + compile_result.stderr)
    
    # 获取编译后的可执行文件路径
    exec_src = os.path.join(project_dir, "_build", "default", "bin", "main.exe")
    if not os.path.exists(exec_src):
        raise CG.CompileError("Executable file not found")
    config["exec_src"] = exec_src

    # 计算测试用例数量
    testcase_dir = Env()["testcase_dir"]
    if "testcase_num" not in config or config["testcase_num"] == 0:
        config["testcase_num"] = len([f for f in os.listdir(testcase_dir) if f.startswith("input") and f.endswith(".txt")])

    if config['testcase_num'] == 0:
        raise CG.UnknownError("No test case file")

    # 创建测试用例
    testcases = gg.create_testcase(config['testcase_num'])
    for i in range(1, config['testcase_num'] + 1):
        input_file = os.path.join(testcase_dir, f"input{i}.txt")
        output_file = os.path.join(testcase_dir, f"output{i}.txt")
        if not os.path.exists(input_file):
            raise IOError(f"Input file not found: {input_file}")
        if not os.path.exists(output_file):
            raise IOError(f"Output file not found: {output_file}")
        testcases.append(
            name=str(i),
            input_src=input_file,
            output_src=output_file,
            score=100 / config['testcase_num']
        )
    job.set_testcases(testcases)