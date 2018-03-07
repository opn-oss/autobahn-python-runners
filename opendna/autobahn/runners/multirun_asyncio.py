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
import json
import signal

import txaio
from autobahn.asyncio.wamp import ApplicationRunner
from opendna.common.decorators import with_uvloop_if_possible

from opendna.autobahn.runners import (
    RunnerArgumentParser,
    get_class
)


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


@with_uvloop_if_possible
def run():
    parser = RunnerArgumentParser()
    parser.add_argument(
        '-c', '--component',
        action='append',
        dest='components',
        required=True,
        help='Fully-qualified path to a Component class. Can be used multiple times'
    )
    parser.add_argument(
        '-n',
        '--necromancy',
        action='store_true',
        default=False,
        help='Enable necromancy. Attempts to revive Components whose connection to the WAMP router has failed'
    )
    args = parser.parse_args()
    extras = {}
    serializers = None
    if args.extra_file is not None:
        extras = json.load(open(args.extra_file))
    if args.serializers is not None:
        serializers = [
            get_class(serializer)
            for serializer in args.serializers
        ]
    components__runners = [
        (
            get_class(component),
            ApplicationRunner(
                extra=extras.get(component),
                serializers=serializers,
                **{
                    key: value
                    for key, value in vars(args).items()
                    if key not in ('components', 'log_level', 'extra_file', 'serializers')
                }
            )
        )
        for component in args.components
    ]
    loop = asyncio.get_event_loop()
    txaio.use_asyncio()
    txaio.config.loop = loop
    coros = [
        runner.run(component, start_loop=False, log_level=args.log_level)
        for component, runner in components__runners
    ]
    results = loop.run_until_complete(asyncio.gather(*coros))

    if args.necromancy:
        async def checkpoint():
            nonlocal results, coros, components__runners, loop
            import asyncio
            while True:
                print('Taking a nap')
                await asyncio.sleep(10)
                print('Checking for life...')
                for (component, runner), (transport, protocol) in zip(components__runners, results):
                    if transport.is_closing():
                        print('Transport closing. Waiting...')
                        await asyncio.sleep(5)
                        print('Attempting CPR...')
                        asyncio.ensure_future(runner.run(component, start_loop=False, log_level=args.log_level), loop=loop)

        asyncio.ensure_future(checkpoint(), loop=loop)

    txaio.start_logging(level=args.log_level)

    try:
        loop.add_signal_handler(signal.SIGTERM, loop.stop)
    except NotImplementedError:
        # signals are not available on Windows
        pass

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        # wait until we send Goodbye if user hit ctrl-c
        # (done outside this except so SIGTERM gets the same handling)
        pass
    except Exception as e:
        pass
        raise

    coros = [
        loop.run_until_complete(protocol._session.leave())
        for tranport, protocol in results
        if protocol._session
    ]

    loop.close()


if __name__ == '__main__':
    run()
