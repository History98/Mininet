from blutopoNew import BluLivTopo
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch, CPULimitedHost
from mininet.util import irange, quietRun, dumpNodeConnections
from mininet.link import TCLink
from mininet.log import setLogLevel, info, output
from mininet.cli import CLI
from functools import partial
from time import time, sleep
import random
import os

resultDir = '%s/Blu/TestResults/ITG' %os.path.expanduser('~')
if not os.path.exists(resultDir):
  os.makedirs(resultDir)

#Ip Addresses
osxBridgeIP = '192.168.0.13'


#Assuming Mb = 1000Kb...
BWlist = [800, 2000, 4000]
divBW = 50.0
pktSize = 800
#pktFreq = lambda bw: bw * 1000**2 / (pktSize * 8 * divBW)
simBW = [(lambda bw: '-O %s' %(bw * 1000**2 / (pktSize * 8 * divBW))) (x) for x in BWlist] #packet frequency args for simulated bandwidth
mdic = dict(low=simBW[0], mid=simBW[1], high=simBW[2], mixed = lambda: random.choice(simBW), bursty = '-B O 950 O 50')

def CreateNet():
  topo = BluLivTopo(4000/divBW) #n=10)
  OVSK13 = partial( OVSKernelSwitch, protocols='OpenFlow13' )
  LocalRController = partial( RemoteController, ip=osxBridgeIP)
  net = Mininet( topo=topo, switch=OVSK13, controller=LocalRController,  autoSetMacs=True )
  info('***Starting Network\n')
  net.start()
  info('***Dumping host connections\n')
  dumpNodeConnections( net.hosts )
  info('***Testing network connectivity\n')
  sleep(2)
  net.pingAllFull()
  return net

def ITGTest(time = 20, pt = 'TCP', mode = 'low'):
  mode = mode if mode in mdic else 'low'
  server = net['h30']
  server.cmd('pkill -9 ITG')

  output('Starting %s test for %s load\n' %(pt, mode))
  fsuffix = '_%s_%s.log' %(pt, mode)
  server.sendCmd('ITGRecv -l %s/%s%s' %(resultDir, 'receiver', fsuffix))
  sleep(2)
  hostCmd = lambda a: 'ITGSend -l %s -a %s -m rttm -t %s -d 5000 -T %s -u %s %s %s' %('%s/%s%s' %(resultDir, a, fsuffix), server.IP(), time*1000, pt, pktSize*0.7, pktSize*1.3, mdic[mode]() if mode=='mixed' else mdic[mode] )
  [h.sendCmd(hostCmd(h.name)) for h in net.hosts[:-1]]
  output('Let\'s wait a bit to complete\n')
  sleep(time+10)
  [(h.sendInt(), h.waitOutput()) for h in net.hosts]
  output('Completed test\n\n')
  sleep(2)

if __name__ == '__main__':
  setLogLevel( 'info' )
  net = CreateNet()
  [ITGTest(pt = i, mode = j) for i in ['TCP', 'UDP'] for j in mdic]
  CLI(net)
  net.stop()
