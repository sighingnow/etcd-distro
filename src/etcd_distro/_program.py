#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 The etcd Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import subprocess
import sys

base_loc = os.path.join(os.path.dirname(__file__), 'etcdbin')


def _program(name, args):
    if os.name == 'nt':
        name = name + '.exe'
    prog = os.path.join(base_loc, name)
    if os.name == 'nt':
        try:
            return subprocess.call([prog] + args)
        except KeyboardInterrupt:
            return 0
    else:
        return os.execvp(prog, [prog] + args)


def etcd():
    raise SystemExit(_program('etcd', sys.argv[1:]))


def etcdctl():
    raise SystemExit(_program('etcdctl', sys.argv[1:]))


def etcdutl():
    raise SystemExit(_program('etcdutl', sys.argv[1:]))

