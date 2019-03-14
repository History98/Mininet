#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import OVSKernelSwitch
from mininet.log import setLogLevel, info
from mininet.util import irange, quietRun, dumpNodeConnections
from mininet.link import TCLink
from mininet.cli import CLI
from functools import partial
import itertools

from subprocess import call

from time import sleep

runtimeMinutes = 20
runtimeSeconds =  runtimeMinutes * 60 
runtimeMS = runtimeSeconds * 1000
strRuntimeMS = str(runtimeMS)
n = 1

low_alpha = 0.01
mid_alpha = 0.03
high_alpha = 0.05

alpha = low_alpha
packets_per_second = str(alpha * 2000)

def startNetwork():
    addrPrefix = '127.0.0.'
    network = Mininet( topo = None, build = False, 
                    ipBase = '10.0.0.0/8')

    info('***Adding Switches and Hosts\n')

    #1mb simulation, each node genrates alpha * 1mb (bytes per second)

    numDevices = 19
    linkMatrix = {1:[4], 2:[13,18], 3:[6], 4:[5,7], 5:[10], 6:[7,11], 7:[8], 8:[9,12], 9:[16,18], 11:[12,13], 14:[15,16], 15:[17], 16:[19], 17:[18]}
    hosts = [network.addHost('h%s' % s) for s in irange(1, numDevices)]
    switches = [network.addSwitch('s%s' % s, cls=OVSKernelSwitch) for s in irange(1, numDevices)]
    #linkopts = dict(cls=TCLink, bw=n, delay='0.1ms', loss=5)
    [network.addLink(hosts[i], switches[i]) for i in range(numDevices)]
    
    [network.addLink(switches[i-1], switches[j-1]) for i in linkMatrix for j in linkMatrix[i]]
    

    info('***Hosts and Switches Added\n')

    homeIP = '192.168.0.13'
    currIP = '192.168.1.118'
    c0 = network.addController(name = 'c0', 
                              protocol='tcp',
                              controller=RemoteController,
                              ip=homeIP,
                              port=6633) 

    info('***Starting Network\n')


    network.start()
    
    #network.pingAll()

    #CLI(network)
  
    #h1 and h2 are the connected to the PoPs
    
    
    h1 = network.get('h1')
    #h10 = network.get('h10')

    xterm_recv_command = 'xterm ITGRecv &'
    xterm_send_command = 'ITGSend -T UDP -a 10.0.0.1 -c 500 -C '+ packets_per_second +'  -t ' + strRuntimeMS + ' -l sender.log -x receiver.log &'
    h1.cmd(xterm_recv_command); 
    
    #Wait for h1 to setup receiver
    sleep(5)

    for index, host in enumerate(hosts):
        if index >= 2:
            host.cmd(xterm_send_command)

    

    #for host in hosts:
    #    host.cmd(xterm_recv_command)     

    #print (result2)

   

    CLI(network)

    network.stop()






if __name__ == '__main__':
    setLogLevel('info')
    startNetwork()