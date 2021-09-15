import os
import textwrap
from argparse import ArgumentParser
from collections.abc import Iterable, Mapping

from jsonschema._utils import Unset
from prance import ResolvingParser
from prance_cli_error_parser.util import pretty_type, shorten

argparser = ArgumentParser()
argparser.add_argument(
        "target",
        type=str,
        help='openapi.yaml file path',
        )
argparser.add_argument(
        "--raw",
        action='store_true',
        )
argparser.add_argument(
        "--rows",
        type=int,
        default=1,
        help='Maximum rows per exception argument (a shortened string is displayed). Default 1'
        )
argparser.add_argument(
        "--width",
        type=int,
        help="Defaults to active terminal's width (run 'echo $COLUMNS' to view)"
        )
argparser.add_argument(
        "--max-depth",
        type=int,
        help="No depth limit by default"
        )
argparser.add_argument(
        "--backend",
        type=str,
        choices=['openapi-spec-validator', ],
        default='openapi-spec-validator',
        help='Default: openapi-spec-validator'
        )
argparser.add_argument(
        "--working-dir",
        type=str,
        default='.',
        help='Set script working directory'
        )

parsed_args = argparser.parse_args()
target = parsed_args.target
rows = parsed_args.rows
backend = parsed_args.backend
working_dir = parsed_args.working_dir
width = parsed_args.width
max_depth = parsed_args.max_depth
raw = parsed_args.raw

os.chdir(working_dir)

if not width:
    width = 10 * (int(os.get_terminal_size()[0]) // 10) - 5  # round down

if not max_depth:
    from math import inf
    
    max_depth = inf

try:
    from rich.traceback import install
    
    install(show_locals=True, width=width, word_wrap=True)
except ModuleNotFoundError:
    pass
indent = -1


def format_primitive(arg, *, idx, indent_size, prefix, tabs):
    short = shorten(str(arg), limit=(width - indent_size) * rows)
    wrapped = textwrap.fill(short, width=width - indent_size + prefix)
    joiner = f'\n{tabs}' + ' ' * prefix
    formatted = f'{idx} ' + joiner.join(wrapped.splitlines())
    return formatted


def print_error_args(args: Iterable):
    global indent
    if indent == max_depth:
        return
    indent += 1
    tabs = '\033[38;2;40;40;40m' + '· ' * indent + '\033[0m'
    for i, arg in enumerate(args):
        if not arg or arg is Unset or isinstance(arg, Unset):
            continue
        prefix = len(str(i)) + 4
        indent_size = 2 * indent + prefix  # including space
        idx = f'{tabs}\x1b[90m[{i}]\x1b[0m'
        typ = f'\x1b[90m{pretty_type(type(arg))}\x1b[0m'
        if isinstance(arg, Iterable) and not isinstance(arg, str) and not isinstance(arg, Mapping):
            print(idx, typ)
            print_error_args(arg)
        elif isinstance(arg, BaseException):
            print(idx, typ)
            print_error_args(arg.args)
        else:
            formatted = format_primitive(arg, idx=idx, indent_size=indent_size, prefix=prefix, tabs=tabs)
            print(formatted)
    else:
        indent -= 1


def main():
    try:
        parser = ResolvingParser(
                target,
                lazy=False,
                backend=backend
                )
    except Exception as e:
        if raw:
            raise
        print_error_args(e.args)
    else:
        print(f'Valid (no errors): {target}')


if __name__ == '__main__':
    main()
