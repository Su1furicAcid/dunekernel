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

def verdict_badge(verdict):
    color = {
        Verdict.Accept: "#28a745",
        Verdict.WrongAnswer: "#dc3545",
        Verdict.RuntimeError: "#ffc107",
        Verdict.CompileError: "#17a2b8"
    }.get(verdict, "#6c757d")
    return f'<span style="display:inline-block;padding:2px 10px;border-radius:12px;font-weight:bold;background:{color};color:#fff;">{verdict}</span>'

def postwork(job: gg.Job):
    summary = job.get_summary()
    score = job.get_total_score()
    verdict = make_verdict([x['verdict'] for x in summary])
    job.verdict(verdict)
    job.score(score)

    # 表格
    table_html = '''
    <style>
    table.judge-table{border-collapse:separate;border-spacing:0 4px;box-shadow:0 2px 8px #eee;border-radius:8px;overflow:hidden;}
    table.judge-table th,table.judge-table td{padding:10px 18px;}
    table.judge-table th{background:#f5f5f5;}
    table.judge-table tr[data-verdict]:hover{filter:brightness(0.97);}
    </style>
    '''
    table_html += '<table class="judge-table" border="0"><tr><th>测试点</th><th>结果</th><th>得分</th></tr>'
    for sum in summary:
        color = verdict_color(sum["verdict"])
        badge = verdict_badge(sum["verdict"])
        table_html += f'<tr data-verdict style="background:{color}"><td>{sum["name"]}</td><td>{badge}</td><td>{sum["score"]}</td></tr>'
    table_html += '</table>'

    # 总结信息
    summary_html = f'''
    <div style="margin:18px 0 12px 0;padding:12px 18px;background:#f8f9fa;border-radius:8px;box-shadow:0 1px 4px #eee;">
      <span style="font-size:1.2em;font-weight:bold;">总分：</span>
      <span style="font-size:1.2em;color:#007bff;font-weight:bold;">{score} / 100</span>
      <span style="margin-left:24px;font-size:1.2em;font-weight:bold;">总评：</span>
      {verdict_badge(verdict)}
    </div>
    '''

    # 详细信息（可折叠）
    details = ""
    for sum in summary:
        if sum["verdict"] == Verdict.RE:
            details += f'''
<details style="margin:8px 0;">
<summary style="font-weight:bold;color:#dc3545;">测试点 {sum["name"]} 运行时错误详情</summary>
<pre style="background:#f8f9fa;border-radius:6px;padding:10px 14px;">stderr: {sum.get("stderr", "")}
return_code: {sum.get("return_code", "")}</pre>
</details>
'''

    job.comment(summary_html + table_html)
    job.detail(details)