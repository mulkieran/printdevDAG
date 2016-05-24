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

from collections import defaultdict

import pydevDAG

from . import _breadth
from . import _depth
from . import _layers
from . import _print


class PrintGraph(object):
    """
    Print a textual representation of the graph.
    """
    # pylint: disable=too-few-public-methods

    @staticmethod
    def line_info(graph):
        """
        Get a line info object.

        :param DiGraph graph: the graph

        :returns: a line info object
        :rtype: GraphLineInfo
        """
        justification = defaultdict(lambda: '<')
        justification['SIZE'] = '>'
        name_funcs = [
           pydevDAG.NodeGetters.DMNAME,
           pydevDAG.NodeGetters.DEVNAME,
           pydevDAG.NodeGetters.SYSNAME,
           pydevDAG.NodeGetters.IDENTIFIER
        ]
        path_funcs = [
           pydevDAG.NodeGetters.IDSASPATH,
           pydevDAG.NodeGetters.IDPATH
        ]
        return _print.GraphLineInfo(
           graph,
           [
              'NAME',
              'NODETYPE',
              'DEVNAME',
              'SUBSYSTEM',
              'DEVTYPE',
              'DM_SUBSYSTEM',
              'ID_PATH',
              'MAJOR',
              'SIZE'
           ],
           justification,
           {
              'NAME' : name_funcs,
              'NODETYPE' : [pydevDAG.NodeGetters.NODETYPE],
              'DEVNAME' : [pydevDAG.NodeGetters.DEVNAME],
              'DEVTYPE': [pydevDAG.NodeGetters.DEVTYPE],
              'DM_SUBSYSTEM' : [pydevDAG.NodeGetters.DMUUIDSUBSYSTEM],
              'ID_PATH' : path_funcs,
              'MAJOR': [pydevDAG.NodeGetters.MAJOR],
              'SIZE': [pydevDAG.NodeGetters.SIZE],
              'SUBSYSTEM': [pydevDAG.NodeGetters.SUBSYSTEM]
           }
        )

    @staticmethod
    def depth_first(graph, line_info):
        """
        Yield lines for depth first output.

        :param DiGraph graph: the graph
        :param GraphLineInfo line_info: the line info object

        :returns: generates lines as str
        :rtype: a generator of str
        """
        infos = _depth.GraphLineArrangements.node_strings_from_graph(
           _depth.GraphLineArrangementsConfig(
              line_info.info,
              lambda k, v: str(v),
              'NAME'
           ),
           graph
        )

        items = list(_depth.GraphXformLines.xform(line_info.keys, infos))
        return _print.Print.lines(
           line_info.keys,
           items,
           2,
           line_info.alignment
        )

    @staticmethod
    def layers(graph, line_info):
        """
        Yield data for a layered view of the storage stack.

        :param DiGraph graph: the graph
        :param GraphLineInfo line_info: the line info object
        """
        infos = _layers.GraphLineArrangements.node_strings_from_graph(
           _layers.GraphLineArrangementsConfig(
              line_info.info,
              lambda k, v: str(v),
              'NAME'
           ),
           graph
        )

        for ((node_type, dev_type, dm_subsystem), items) in infos:
            yield ""

            fmt_str = "".join([
               '%(dm)s',
               '%(dm_space)s',
               '%(devtype)s',
               '%(devtype_space)s',
               '%(nodetype)s',
               's'
            ])

            value = {
               'dm' : dm_subsystem if dm_subsystem is not None else '',
               'dm_space' : ' ' if dm_subsystem is not None else '',
               'devtype' : dev_type if dev_type is not None else '',
               'devtype_space' : ' ' if dev_type is not None else '',
               'nodetype' : node_type
            }

            yield fmt_str % value

            lines = _print.Print.lines(
              line_info.keys,
              items,
              2,
              line_info.alignment
            )
            for line in lines:
                yield line

    @staticmethod
    def breadth_first(graph, line_info):
        """
        Yield data for a breadth first search
        """
        infos = _breadth.GraphLineArrangements.node_strings_from_graph(
           _breadth.GraphLineArrangementsConfig(
              line_info.info,
              lambda k, v: str(v),
              'NAME'
           ),
           graph
        )

        for (level, items) in infos:
            yield ""
            yield "Level: %s" % level
            lines = _print.Print.lines(
              line_info.keys,
              items,
              2,
              line_info.alignment
            )
            for line in lines:
                yield line

    @classmethod
    def print_graph(cls, out, graph, traversal):
        """
        Print a graph.

        :param `file` out: print destination
        :param `DiGraph` graph: the graph
        :param str traversal: the type of graph to print
        """
        line_info = cls.line_info(graph)

        if traversal == 'depth_first':
            func = cls.depth_first
        elif traversal == 'breadth_first':
            func = cls.breadth_first
        elif traversal == 'layers':
            func = cls.layers
        else:
            assert False

        for line in func(graph, line_info):
            print(line, end="\n", file=out)
