from pygrading.html import *
from verdict import Verdict

def make_table(data, summary):
    ans = table(border="1")
    # 创建表头
    thead = tr()
    for key in summary:
        thead << th().set_text(key)
    ans << thead

    # 创建表主体
    for test in data:
        # print(data)
        row = tr()
        for key in summary:
            row << td().set_text(str2html(str(test[key])))
        ans << row

    return str(ans)


def make_one_line_table(data, header):
    tab = table(border="1")
    tab << tr(th(colspan=str(len(header))).set_text(data['name']))
    thead = tr()
    for key in header:
        thead << th().set_text(key)
    tab << thead

    # 创建表主体
    row = tr()
    for key in header:
        row << td().set_text(str2html(str(data[key])))
    tab << row
    return str(tab)


# verdicts = ['Accept', 'Accept', 'Wrong Answer']
def make_verdict(verdicts: list):
    for x in verdicts:
        if x != Verdict.Accept:
            return x
    return Verdict.Accept
