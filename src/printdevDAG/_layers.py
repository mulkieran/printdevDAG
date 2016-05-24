# -*- coding: utf-8 -*-
# Copyright (C) 2016  Red Hat, Inc.
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
    printdevDAG._layers
    ===================

    Do a breadth first search of DAG combining nodes into layers.

    .. moduleauthor::  mulhern <amulhern@redhat.com>
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import itertools

import pydevDAG

from printdevDAG._utils import GeneralUtils


class GraphLineArrangementsConfig(object):
    """
    Class that represents the configuration for LineArrangements methods.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, info_func, conversion_func, sort_key):
        """
        Initializer.

        :param info_func: a function that returns information for a node
        :type info_func: see LineInfo.info
        :param conversion_func: converts info_func values to str
        :type conversion_func: (str * object) -> str
        :param str sort_key: the key/column name to sort on
        """
        self.info_func = info_func
        self.conversion_func = conversion_func
        self.sort_key = sort_key


class GraphLineArrangements(object):
    """
    Sort out nodes and their relationship to each other in printing.
    """
    # pylint: disable=too-few-public-methods

    @classmethod
    def node_strings_from_graph(cls, config, graph):
        """
        Generates print information about nodes in graph.
        Starts from the roots of the graph.
        Yields a value for each level in the graph.

        :param LineArrangementsConfig: config
        :param `DiGraph` graph: the graph

        :returns: a table of information to be used for further display
        :rtype: tuple of int * (list of dict of str * object)

        """
        node_key_func = GeneralUtils.str_key_func_gen(
           lambda n: config.info_func(n, [config.sort_key])[config.sort_key]
        )
        nodes = pydevDAG.BreadthFirst.nodes(
           graph,
           key_func=node_key_func
        )

        levels = itertools.groupby(nodes, lambda x: x[0])

        def key_func(node):
            """
            The key for each node.

            :param str node: the node

            :returns: a key for the node
            :rtype: tuple of object * object * object
            """
            attrs = graph.node[node]
            return (
               pydevDAG.NodeGetters.NODETYPE.getter(attrs),
               pydevDAG.NodeGetters.DEVTYPE.getter(attrs),
               pydevDAG.NodeGetters.DMUUIDSUBSYSTEM.getter(attrs)
            )

        for (_, level_nodes) in levels:
            level_node_names = \
               sorted(set(x[1] for x in level_nodes), key=key_func)
            level_node_groups = itertools.groupby(level_node_names, key_func)

            for (desig, node_group) in level_node_groups:
                yield (
                   desig,
                   [
                      config.info_func(
                         n,
                         keys=None,
                         conv=config.conversion_func
                      ) for n in sorted(node_group, key=node_key_func)
                   ]
                )
