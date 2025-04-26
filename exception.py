import pygrading as gg
import pygrading.html as html
from verdict import Verdict


class CG:
    class Exception(Exception):
        def __init__(self, verdict: str, comment: str):
            self.verdict = verdict
            self.comment = comment

    class RuntimeError(Exception):
        def __init__(self, comment: str):
            CG.Exception.__init__(self, Verdict.RE, comment)

    class CompileError(Exception):
        def __init__(self, comment: str):
            CG.Exception.__init__(self, Verdict.CE, comment)

    class WrongAnswer(Exception):
        def __init__(self, comment: str):
            CG.Exception.__init__(self, Verdict.WA, comment)

    class UnknownError(Exception):
        def __init__(self, comment: str):
            CG.Exception.__init__(self, Verdict.UE, comment)

    @staticmethod
    def catch(fun):
        def wrapper(job: gg.Job, *args, **kwargs):
            try:
                return fun(job, *args, **kwargs)
            except CG.Exception as e:
                job.verdict(e.verdict)
                job.comment(html.str2html(e.comment))
                job.score(0)
                job.rank({"rank": "-1"})
                job.is_terminate = True
        return wrapper
