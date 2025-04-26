import pygrading as gg
from render import make_verdict, make_table, make_one_line_table
from verdict import Verdict


def postwork(job: gg.Job):
    summary = job.get_summary()
    score = job.get_total_score()
    verdict = make_verdict([x['verdict'] for x in summary])
    job.verdict(verdict)
    job.score(score)
    rank = job.get_total_time() if score == 100 else 0
    job.rank({"rank": rank})

    job.comment(make_table(summary, ['name', 'verdict', 'score']))
    details = ""
    for sum in summary:
        if sum["verdict"] == Verdict.RE:
            details += make_one_line_table(sum, ["stderr", "return_code"])
    job.detail(details)