from mininet.topo import Topo
from mininet.node import CPULimitedHost, OVSBridge
from mininet.util import irange, quietRun
from mininet.link import TCLink

class BluLivTopo(Topo):
  def build(self, n = 80):
    linkMatrix = {1:[4], 2:[13,18,23], 3:[6], 4:[5,7], 5:[10], 6:[7,11], 7:[8], 8:[9,12], 9:[16,18], 11:[12,13], 14:[15,16], 15:[17], 16:[19], 17:[18]}
    indices = [i for i in irange(1, 19)+[23]]
    linkopts = dict(cls=TCLink, bw=n, delay='0.1ms', loss=5)
    hosts = {s:self.addHost('h%s' % s, cls= CPULimitedHost, cpu=.6/20) for s in indices}
    switches = {s:self.addSwitch('s%s' % s) for s in indices}
    [self.addLink(switches[i], switches[j], **linkopts) for i in linkMatrix for j in linkMatrix[i]]
    [self.addLink(hosts[i], switches[i]) for i in indices]
    
    rhost = self.addHost('h30')
    gswitch = self.addSwitch('s30')
    [self.addLink(i, gswitch) for i in [switches[1], switches[2], rhost]]

topos = { 'blutopo': ( lambda: BluLivTopo() ) }

# use: sudo mn --custom blutopo.py --topo blutopo