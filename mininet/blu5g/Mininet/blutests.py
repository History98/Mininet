from blutopo import BluLivTopoOne, BluLivTopoTwo
from blutopoNew import BluLivTopo
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, CPULimitedHost
from mininet.util import irange, quietRun, dumpNodeConnections
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from functools import partial
from time import sleep
import os
import datetime

def perfTest():
  "Create network and run simple performance test"
  topo = BluLivTopoOne()
  OVSK13 = partial( OVSKernelSwitch, protocols='OpenFlow13' )
  LocalRController = partial( RemoteController, ip='127.0.0.1')
  net = Mininet( topo=topo, switch=OVSK13, host=CPULimitedHost, controller=LocalRController, link=TCLink, autoSetMacs=True )

  info('***Starting Network\n')
  net.start()
  print "Dumping host connections"
  dumpNodeConnections( net.hosts )
  print "Testing network connectivity"
  PingResults = '***New Tests starting at: %s\n' %datetime.datetime.now()
  PingResults += '***Testing Network Connectivity:\n%s\n' %net.pingAllFull()
  
  def iPerfTest(l4Type='TCP'):
    results = '***%s Tests\n' %l4Type  
    for h in net.hosts[:-1]:
      results += '***%s Results for %-3s : ' %(l4Type, h.name)
      results += '%s\n' %net.iperf( (h, net.hosts[-1]), seconds=8, l4Type=l4Type )
      sleep(2)
    return results + '\n'
  
  print "***Testing bandwidth between each host and remote server (h30)"
  iPerfResults = '***Testing bandwidth between each host and remote server (h30)\n'
  iPerfResults += iPerfTest()    
  print "***Testing jitter and loss between each host and server (h30)"
  iPerfResults += '***Testing jitter and loss between each host and server (h30)\n'
  iPerfResults += iPerfTest('UDP')

  net.stop()

  filename = '%s/Blu/TestResults/ping_iperf.txt' %os.path.expanduser('~')
  if not os.path.exists(os.path.dirname(filename)):
    os.makedirs(os.path.dirname(filename))
  with open(filename, 'a') as f:
    f.write('%s\n\n%s\n***Results of Tests finished at: %s\n\n\n' %(PingResults, iPerfResults, datetime.datetime.now()))

if __name__ == '__main__':
  setLogLevel( 'info' )
  perfTest()