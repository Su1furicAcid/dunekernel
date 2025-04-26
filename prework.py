import pygrading as gg
import os
from exception import CG
from utils import Env
import json
import shutil
import pkgutil

@CG.catch
def prework(job: gg.Job):
    config = job.get_config()

    if len(os.listdir(config['submit_dir'])) == 0:
        raise CG.CompileError("No submit file")
    
    # 检查 opam 是否安装了 dune
    check_opam_cmd = "opam list --installed | grep dune"
    gg.utils.exec(check_opam_cmd)

    # 检查 dune 的安装路径
    find_dune_cmd = "find ~/.opam -name dune"
    gg.utils.exec(find_dune_cmd)

    # 手动添加 dune 的路径到 PATH
    dune_path = os.path.join(os.path.expanduser("~"), ".opam", "default", "bin")
    if dune_path not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + dune_path

    # 检查 dune 是否安装
    check_dune_cmd = "dune --version"
    check_dune_result = gg.utils.exec(check_dune_cmd)
    if check_dune_result.returncode != 0:
        raise CG.CompileError("Dune is not installed or not found in PATH")

    # 创建一个临时dune项目
    create_project_dir = os.path.join(config['exec_dir'], "dune_project")
    if not os.path.exists(create_project_dir):
        os.makedirs(create_project_dir)
    os.chdir(create_project_dir)
    create_dune_cmd = "dune init project {}".format(config["temp_proj_name"])
    create_dune_result = gg.utils.exec(create_dune_cmd)
    if create_dune_result.returncode != 0:
        raise CG.CompileError(create_dune_result.stdout + '\n' + create_dune_result.stderr)
    project_dir = os.path.join(create_project_dir, config["temp_proj_name"])

    # 使用 pkgutil.get_data 读取 config.json
    config_data = pkgutil.get_data(__name__, "dune_config/config.json")
    if not config_data:
        raise FileNotFoundError("Config file not found in the package: dune_config/config.json")

    # 解析 JSON 数据
    config_json = json.loads(config_data.decode("utf-8"))

    # 遍历并复制文件到项目目录
    for file_path in config_json["files"]:
        # 将路径数组拼接成文件路径
        relative_path = os.path.join(*file_path)
        file_data = pkgutil.get_data(__name__, f"dune_config/{relative_path}")

        if not file_data:
            raise FileNotFoundError(f"File not found in the package: dune_config/{relative_path}")
        
        # 目标路径
        dst = os.path.join(project_dir, relative_path)
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        
        # 写入文件
        with open(dst, "wb") as f:
            f.write(file_data)

    # 复制提交文件到项目的 /lib 目录
    for file in os.listdir(config["submit_dir"]):
        src = os.path.join(config["submit_dir"], file)
        dst = os.path.join(project_dir, "lib", file)
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        shutil.copy(src, dst)

    # 编译项目
    clean_cmd = f"dune clean --root {project_dir}"
    gg.utils.exec(clean_cmd)
    compile_cmd = f"dune build --root {project_dir}"
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