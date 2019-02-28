#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.util import irange, quietRun
from mininet.link import TCLink
from functools import partial

class BluLivTopo(Topo):
  def build(self):
    linkMatrix = {1:[4], 2:[13,18], 3:[6], 4:[5,7], 5:[10], 6:[7,11], 7:[8], 8:[9,12], 9:[16,18], 11:[12,13], 14:[15,16], 15:[17], 16:[19], 17:[18]}
    hosts = [self.addHost('h%s' % s) for s in irange(1, 19)]
    switches = [self.addSwitch('s%s' % s) for s in irange(1, 19)]
    [self.addLink(hosts[i], switches[i]) for i in range(19)]
    [self.addLink(switches[i-1], switches[j-1]) for i in linkMatrix for j in linkMatrix[i]]
    #[self.addLink(switches[i-i]), switches[j-1]) for i in linkMatrix for j in linkMatrix[i]]

topos = { 'blutopo': ( lambda: BluLivTopo() ) }

# use: sudo mn --custom blutopo.py --topo blutopo