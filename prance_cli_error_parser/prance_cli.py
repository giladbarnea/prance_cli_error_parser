import os
import textwrap
from argparse import ArgumentParser
from collections.abc import Iterable, Mapping

from jsonschema._utils import Unset
from prance import ResolvingParser

from prance_cli_error_parser.util import pretty_type, shorten

indent = -1


def print_error_args(args: Iterable, *, limit, rows):
    global indent
    indent += 1
    tabs = '\033[38;2;40;40;40m' + '· ' * indent + '\033[0m'
    for i, arg in enumerate(args):
        if not arg or arg is Unset or isinstance(arg, Unset):
            continue
        prefix = len(str(i)) + 4
        indent_size = 2 * indent + prefix  # including space
        idx = f'{tabs}\x1b[90m[{i}]\x1b[0m'
        typ = f'\x1b[90m{pretty_type(type(arg))}\x1b[0m'
        if isinstance(arg, Mapping):
            # not implemented
            print(idx, typ)
            print(arg)
        elif isinstance(arg, Iterable) and not isinstance(arg, str):
            print(idx, typ)
            print_error_args(arg, limit=limit, rows=rows)
        elif isinstance(arg, BaseException):
            print(idx, typ)
            print_error_args(arg.args, limit=limit, rows=rows)
        else:
            width = limit - indent_size
            short = shorten(str(arg), limit=width * rows)
            wrapped = textwrap.fill(short, width=width + prefix)
            joiner = f'\n{tabs}' + ' ' * prefix
            print(f'{idx} ' + joiner.join(wrapped.splitlines()))
    else:
        indent -= 1


def main():
    argparser = ArgumentParser()
    argparser.add_argument(
            "target",
            type=str,
            help='openapi.yaml file path',
            )
    argparser.add_argument(
            "--rows",
            dest="rows",
            type=int,
            default=1,
            help='Maximum rows per exception argument (a shortened string is displayed). Default 1'
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
    os.chdir(working_dir)
    
    limit = 10 * (int(os.get_terminal_size()[0]) // 10)  # round down
    
    try:
        parser = ResolvingParser(
                target,
                lazy=False,
                backend=backend
                )
    except Exception as e:
        print_error_args(e.args, limit=limit, rows=rows)
    else:
        print(f'Valid (no errors): {target}')


if __name__ == '__main__':
    main()
