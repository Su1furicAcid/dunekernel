import pygrading as gg
from render import make_verdict, make_table, make_one_line_table
from verdict import Verdict

def verdict_color(verdict):
    if verdict == Verdict.Accept:
        return "#d4edda"
    elif verdict == Verdict.WrongAnswer:
        return "#f8d7da"
    elif verdict == Verdict.RuntimeError:
        return "#fff3cd"
    elif verdict == Verdict.CompileError:
        return "#d1ecf1"
    else:
        return "#f8f9fa"

def postwork(job: gg.Job):
    summary = job.get_summary()
    score = job.get_total_score()
    verdict = make_verdict([x['verdict'] for x in summary])
    job.verdict(verdict)
    job.score(score)

    # 美化表格
    table_html = '<style>table{border-collapse:collapse;}th,td{padding:8px 12px;}th{background:#eee;}tr[data-verdict]{transition:background 0.3s;}</style>'
    table_html += '<table border="1"><tr><th>测试点</th><th>结果</th><th>得分</th></tr>'
    for sum in summary:
        color = verdict_color(sum["verdict"])
        table_html += f'<tr data-verdict style="background:{color}"><td>{sum["name"]}</td><td>{sum["verdict"]}</td><td>{sum["score"]}</td></tr>'
    table_html += '</table>'

    # 总结信息
    summary_html = f'<div style="margin:10px 0;"><b>总分：</b>{score} / 100<br><b>总评：</b>{verdict}</div>'

    # 详细信息（可折叠）
    details = ""
    for sum in summary:
        if sum["verdict"] == Verdict.RE:
            details += f'''
<details>
<summary>测试点 {sum["name"]} 运行时错误详情</summary>
<pre>stderr: {sum.get("stderr", "")}
return_code: {sum.get("return_code", "")}</pre>
</details>
'''
    job.comment(summary_html + table_html)
    job.detail(details)