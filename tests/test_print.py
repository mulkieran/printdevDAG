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
    tests.test_print
    ================

    Tests string representation of graph.

    .. moduleauthor:: mulhern <amulhern@redhat.com>
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict

import printdevDAG

from ._constants import GRAPH

class TestGraphPrint(object):
    """
    Test aspects of string representation of graphs.
    """
    # pylint: disable=too-few-public-methods


    def test_num_string(self):
        """
        Verify that the number of strings is at least a node's out-degree.
        """
        line_info = printdevDAG.GraphLineInfo(
           GRAPH,
           ['NAME'],
           defaultdict(lambda: '<'),
           {'NAME' : [printdevDAG.NodeGetters.DEVNAME]}
        )
        lines = printdevDAG.GraphLineArrangements.node_strings_from_graph(
           printdevDAG.GraphLineArrangementsConfig(
              line_info.info,
              lambda k, v: str(v),
              'NAME'
           ),
           GRAPH
        )
        assert len(list(lines)) >= len(GRAPH)
