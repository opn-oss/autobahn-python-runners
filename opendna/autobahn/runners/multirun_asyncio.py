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
import asyncio
import signal

import txaio
from autobahn.asyncio.wamp import ApplicationRunner
from autobahn.wamp.protocol import ApplicationSession

from opendna.autobahn.runners import generate_parser, get_class


async def multi_run(loop, runner, components):
    """

    :param loop:
    :type loop asyncio.AbstractEventLoop
    :param runner:
    :type runner autobahn.wamp.protocol.ApplicationSession:
    :param components:
    :type components list:
    :return:
    """
    awaitables = [
        runner.run(make=get_class(component), start_loop=False)
        for component in components
    ]
    results = await asyncio.gather(*awaitables)
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    for transport, protocol in results:
        loop.run_until_complete(protocol._session.leave())

    loop.close()


def main():
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        print('uvloop will be used')
    except ImportError:
        print('uvloop unavailable')
    parser = generate_parser()
    parser._remove_action(parser._option_string_actions['-e'])
    parser.add_argument(
        '-c', '--component',
        action='append',
        dest='components',
        required=True,
        help='Fully-qualified path to a Component class. Can be used multiple times'
    )
    args = parser.parse_args()
    runner = ApplicationRunner(**{
        key: value
        for key, value in vars(args).items()
        if key not in ('components', 'log_level')
    })
    loop = asyncio.get_event_loop()
    try:
        loop.add_signal_handler(signal.SIGTERM, loop.stop)
    except NotImplementedError:
        # signals are not available on Windows
        pass
    txaio.use_asyncio()
    txaio.config.loop = loop
    txaio.start_logging(level=args.log_level)
    loop.run_until_complete(multi_run(loop, runner, args.components))

if __name__ == '__main__':
    main()
