# -*- coding: utf-8 -*-
# Copyright (C) 2015  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Anne Mulhern <amulhern@redhat.com>

"""
    pydevDAG._graphs
    ================

    Tools to build graphs of various kinds.

    .. moduleauthor::  mulhern <amulhern@redhat.com>
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import itertools
import os

from collections import defaultdict

import networkx

from pydevDAG import ElementTypes

from . import _item_str
from . import _print
from . import _utils


class PrintGraph(object):
    """
    Print a textual representation of the graph.
    """
    # pylint: disable=too-few-public-methods

    @staticmethod
    def print_graph(out, graph):
        """
        Print a graph.

        :param `file` out: print destination
        :param `DiGraph` graph: the graph
        """
        justification = defaultdict(lambda: '<')
        justification['SIZE'] = '>'
        name_funcs = [
           _item_str.NodeGetters.DMNAME,
           _item_str.NodeGetters.DEVNAME,
           _item_str.NodeGetters.SYSNAME,
           _item_str.NodeGetters.IDENTIFIER
        ]
        path_funcs = [
           _item_str.NodeGetters.IDSASPATH,
           _item_str.NodeGetters.IDPATH
        ]
        line_info = _print.GraphLineInfo(
           graph,
           [
              'NAME',
              'DEVNAME',
              'SUBSYSTEM',
              'DEVTYPE',
              'DM_SUBSYSTEM',
              'ID_PATH',
              'SIZE'
           ],
           justification,
           {
              'NAME' : name_funcs,
              'DEVNAME' : [_item_str.NodeGetters.DEVNAME],
              'DEVTYPE': [_item_str.NodeGetters.DEVTYPE],
              'DM_SUBSYSTEM' : [_item_str.NodeGetters.DMUUIDSUBSYSTEM],
              'ID_PATH' : path_funcs,
              'SIZE': [_item_str.NodeGetters.SIZE],
              'SUBSYSTEM': [_item_str.NodeGetters.SUBSYSTEM]
           }
        )

        lines = _print.GraphLineArrangements.node_strings_from_graph(
           _print.GraphLineArrangementsConfig(
              line_info.info,
              lambda k, v: str(v),
              'NAME'
           ),
           graph
        )

        lines = list(_print.GraphXformLines.xform(line_info.keys, lines))
        lines = _print.Print.lines( # pylint: disable=redefined-variable-type
           line_info.keys,
           lines,
           2,
           line_info.alignment
        )
        for line in lines:
            print(line, end="\n", file=out)
