#!/usr/bin/python

from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import OVSController, OVSKernelSwitch, RemoteController
from mininet.util import dumpNodeConnections


def startNetwork():
    network = Mininet(topo=None)
    h1 = network.addHost('h1')
    h2 = network.addHost('h2')
    s1 = network.addSwitch('s1', cls=OVSKernelSwitch)
    
    c0 = network.addController('c0',
                            controller=RemoteController,
                            ip='192.168.0.13',
                            port=6633)


    network.addLink(h1, s1)
    network.addLink(h2, s1)

    network.start()

    CLI(network)

    network.stop()


if __name__ == '__main__':
    setLogLevel('info')
    startNetwork()