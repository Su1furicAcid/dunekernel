## 希冀平台评测内核

这里是“程序语言原理和编译技术”的希冀评测机内核（使用 dune 构建项目），用于期末考试的评测。

### 项目结构

```
dune_config         --> 整个 dune 项目中不需要学生完成的部分
├── dune-project    --> dune 项目配置文件
├── bin             --> 可执行文件目录
    ├── dune        --> dune 可执行文件的构建配置
    ├── main.ml     --> 主程序 应当提前写好输入输出流 然后调用学生实现的函数
├── lib             --> 学生完成的代码会被放在这里 作为整个 dune 项目的一个模块（module）
    ├── dune        --> dune 可执行文件的构建配置
├── config.json     --> dune 项目文件注册 方便脚本进行复制

__main__.py         --> 评测脚本主程序
config.py           --> 评测脚本配置文件 存放一些常用的路径配置
exception.py        --> 评测脚本异常
postwork.py         --> 评测结果后处理，主要用于处理评测结果
render.py           --> 评测接过渲染，主要用于处理评测结果的输出
prework.py          --> 预处理，主要用于处理学生提交的代码（构建项目、编译）
run.py              --> 学生运行，主要用于获取和比较学生代码的运行结果
utils.py            --> 工具函数，主要用于处理环境
verdict.py          --> 评测结果，主要用于处理评测结果
```

### 构建一个新的评测机的流程

本评测机已经构建好了一个普通算法题的评测机内核，见 `dune_config` 目录和其他文件。你可以直接使用这个评测机内核来进行普通算法题的评测，但是如果想要构建一个更加复杂的评测机内核，比如一个编译器的评测机内核，或者一个解释器的评测机内核，那么你需要了解一下这个评测机的构建流程（就是怎么修改这个项目以适配实际需求）。

以构建一个普通算法题的评测机扩展内核为例：

##### 配置好一个 dune 项目

为了统一输入输出流（也为了不让学生再写一遍输入输出），我们需要首先构建好一个 dune 项目的配置：

学生实现的代码应该是一个函数。假设算法题是计算两数之和：

```ocaml
let add x y = x + y;;
```

那么我们需要在 `lib` 目录下创建一个 `add.mli` 文件，定义好函数签名：

```ocaml
(* test.mli *)
val add : int -> int -> int
```

然后在 `lib` 目录下写好 `dune` 文件，配置好 dune 项目：

```lisp
(library
 (name lib)
 (modules :standard))
```

假如学生上传了一个 `add.ml` 文件，这个文件就会被放置到 `lib` 目录下。`:standard` 会把所有的 `.ml` 文件都认为成以文件名命名的模块。

然后需要在 `bin` 目录下创建一个 `main.ml` 文件，这里是主程序，主要用于从标准输入读取数据，然后调用学生实现的函数，最后输出结果。

```ocaml
(* main.ml *)
open Lib.Test (* 这里假设学生上传的是test.ml 而不是 add.ml *)
let () =
  let a = read_int () in
  let b = read_int () in
  let result = add a b in
  Printf.printf "%d\n" result
```

然后在 `bin` 目录下写好 `dune` 文件，配置好 dune 项目：

```lisp
(executable
 (name main)
 (libraries lib))
```

最后编辑整个项目的 `dune-project` 文件，配置好 dune 项目。注意评测机的 `dune` 版本是 3.18。

```lisp
(lang dune 3.18)
(name test_project)
```

完成所有工作后，新建一个 `config.json` 文件，里面提到的所有文件都会在评测机新建一个空白 dune 项目后被复制到那个新项目中（在那之后你就在评测集上得到了一个你希望的 dune 项目）。

```json
{
    "name": "dune_config",
    "files": [
        ["dune-project"],
        ["bin", "dune"],
        ["bin", "main.ml"],
        ["lib", "dune"],
        ["lib", "test.mli"]
    ]
}
```

##### 修改脚本的 config.py 文件

脚本的 `config.py` 如下：

```python
import os
import tempfile

KERNEL_CONFIG = {
    'submit_dir': '/coursegrader/submit',
    'testcase_dir': '/coursegrader/testdata',
    'return_code': 0,
    "exec_dir": tempfile.mkdtemp(),
    "source_ext": ".ml",
    "exec_src": "",
    "temp_proj_name": "test_project"
}
```

你可能需要修改 `temp_proj_name` 的名字，方便和 `dune-project` 文件中的名字对应。


##### 打包成 zip 上传

把整个评测机内核打包成 zip 文件，上传到希冀平台的评测机内核中，命名为 `main.zip`。

```
zip -r main.zip .
```