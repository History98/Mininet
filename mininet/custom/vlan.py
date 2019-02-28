#!/usr/bin/python

from mininet.node import Host, RemoteController
from mininet.topo import Topo
import apt

#package check (only works in ubunutu)

cache = apt.Cache()
if cache['vlan'].is_installed:
    print "vlan installed"
else:
    print "vlan not installed"
    exit(1)

class VLANHost( Host ):
    def config(self, vlan = 1, **params):
        """Configure VLANHost according to (optional) 
        parameters:  vlan: VLAN ID for default interface"""

        r = super(Host, self).config(**params)
        intf = self.defaultIntf()

#Remove IP from default, physical interface
        self.cmd('ifconfig %s inet 0' % intf)

#create VLAN interface
        self.cmd('vconfig add %s %d' % (intf , vlan) )

#Assign the hosts IP to the VLAN interface
        self.cmd('ifconfig %s.%d inet %s' % (intf, vlan, params['ip']))

#Update the intf name and hosts intf map
        newName = '%s.%d' % (intf, vlan)

#Update the mininet name to the VLAN interface name
        intf.name = newName

#Add VLAN name to the "Host Name to INTF" map
        self.nameToIntf[newName] = intf
        return r

class MyTopo( Topo ):
    "Simple Topology Example"

    def __init__( self ):
        "Create Custom Topo"

        #Initialize Topology
        Topo.__init__( self )

        #Add Hosts and Switches
        host1 = self.addHost('h1', cls=VLANHost, vlan = 100)
        host2 = self.addHost('h2', cls=VLANHost, vlan = 200)
        host3 = self.addHost('h3', cls=VLANHost, vlan = 100)
        host4 = self.addHost('h4', cls=VLANHost, vlan = 200)
        host5 = self.addHost('h5', cls=VLANHost, vlan = 100)
        host6 = self.addHost('h6', cls=VLANHost, vlan = 200)

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        self.addLink(s1, host1)
        self.addLink(s1, host2)
        self.addLink(s1,s2)

        self.addLink(s2, host3)
        self.addLink(s2, host4)
        self.addLink(s2,s3)

        self.addLink(s3, host5)
        self.addLink(s3, host6)

topos = {'simplevlan': (lambda : MyTopo()) }



        






