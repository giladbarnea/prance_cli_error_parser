import re

OBJ_RE = re.compile(r'<(?:[\w\d<>]+\.)*([\w\d]+) object at (0x[\w\d]{12})>')
TYPE_RE = re.compile(r"<class '(?:[\w\d<>]+\.)*([\w\d]+)'>")
WHITESPACE_RE = re.compile(r'\s+')


def pretty_type(t) -> str:
    try:
        return TYPE_RE.sub(lambda match: match.groups()[0], t)
    except TypeError as e:
        return TYPE_RE.sub(lambda match: match.groups()[0], str(t))


def shorten(s, limit=120):
    if not s:
        return s
    length = len(s)
    if length > limit - 3:
        try:
            left_cutoff = max(s.index('\033[0m') + 4, limit // 2)
            right_cutoff = min((length - s.rindex('\033')) + 4, limit // 2)
        except ValueError:
            left_cutoff = (limit // 2) - 3
            right_cutoff = (limit // 2) + 3
        beginning = s[:left_cutoff]
        end = s[-right_cutoff:]
        return WHITESPACE_RE.sub(' ', f'{beginning} ... {end}')
    return s
