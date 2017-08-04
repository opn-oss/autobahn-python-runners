# coding=utf-8
################################################################################
# MIT License
#
# Copyright (c) 2017 OpenDNA Ltd.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
################################################################################
from __future__ import unicode_literals, absolute_import

import json
from argparse import ArgumentParser, HelpFormatter
from importlib import import_module
from os import environ

__author__ = 'Adam Jorgensen <adam.jorgensen.za@gmail.com>'


class RunnerArgumentParser(ArgumentParser):
    """
    An argument parser pre-configured for use within the Component-runner context
    """
    def __init__(self, prog=None, usage=None, description=None, epilog=None,
                 parents=[], formatter_class=HelpFormatter, prefix_chars='-',
                 fromfile_prefix_chars=None, argument_default=None,
                 conflict_handler='resolve', add_help=True, allow_abbrev=True):
        super(RunnerArgumentParser, self).__init__(
            prog, usage, description, epilog, parents, formatter_class,
            prefix_chars, fromfile_prefix_chars, argument_default,
            conflict_handler, add_help, allow_abbrev
        )
        self.add_argument(
            '-c', '--component',
            default=environ.get('WAMP_COMPONENT'),
            help='Fully-qualified path to a Component class'
        )
        self.add_argument(
            '-u', '--url',
            default=environ.get('WAMP_URL'),
            help='WAMP Router URL'
        )
        self.add_argument(
            '-r', '--realm',
            default=environ.get('WAMP_REALM'),
            help='WAMP Realm'
        )
        self.add_argument(
            '-e', '--extra-file',
            default=environ.get('WAMP_EXTRAS_FILE'),
            help='Path to JSON file of data to be supplied to the '
                 'Component via the config __init__ parameter'
        )
        self.add_argument(
            '-s', '--use-ssl', dest='ssl', type=bool,
            default=environ.get('WAMP_USE_SSL', False),
            help='Specify whether to use SSL'
        )
        self.add_argument(
            '-l', '--loglevel', dest='log_level',
            default=environ.get('WAMP_LOG_LEVEL', 'info'),
            help='Specify log level'
        )
        self.add_argument(
            '--serializers',
            default=None,
            action='append',
            help='Fully-qualified path to a Serializer. Multiple items may be specified'
        )


def get_class(fully_qualified_class_path):
    """
    Returns a class given an input fully-qualified class path E.g.
    a.b.c.d.ClassName

    :param fully_qualified_class_path:
    :return:
    """
    module_name, class_name = fully_qualified_class_path.rsplit('.', 1)
    imported_module = import_module(module_name)
    return getattr(imported_module, class_name)


def build_application_runner(application_runner_class):
    """
    Given an input CrossBar ApplicationRunner class, runs a Component
    defined using input from either the command-line or environment variables
    with parameters determined by said input.

    :param application_runner_class:
    :return:
    :rtype: tuple
    """
    parser = RunnerArgumentParser()
    args = parser.parse_args()
    component = get_class(args.component)
    extra = serializers = None
    if args.extra_file is not None:
        extra = json.load(open(args.extra_file))
    if args.serializers is not None:
        serializers = [
            get_class(serializer)
            for serializer in args.serializers
        ]
    runner = application_runner_class(extra=extra, serializers=serializers, **{
        key: value
        for key, value in vars(args).items()
        if key not in ('component', 'extra_file', 'log_level', 'serializers')
    })
    return component, runner, args.log_level.lower()
