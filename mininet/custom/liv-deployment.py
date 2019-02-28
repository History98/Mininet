#!/usr/bin/python



from mininet.net import Mininet

from mininet.node import Controller, RemoteController, OVSController

from mininet.node import CPULimitedHost, Host, Node

from mininet.node import OVSKernelSwitch, UserSwitch

from mininet.node import IVSSwitch

from mininet.cli import CLI

from mininet.log import setLogLevel, info

from mininet.link import TCLink, Intf

from subprocess import call



def myNetwork():



    net = Mininet( topo=None,

                   build=False,

                   ipBase='10.0.0.0/8')



    info( '*** Adding controller\n' )

    c0=net.addController(name='c0',

                      controller=RemoteController,

                      ip="192.168.0.13",

                      protocol='tcp',

                      port=6633)



    info( '*** Add switches\n')

    s13 = net.addSwitch('s13', cls=OVSKernelSwitch)

    s19 = net.addSwitch('s19', cls=OVSKernelSwitch)

    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

    s22 = net.addSwitch('s22', cls=OVSKernelSwitch)

    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)

    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)

    s10 = net.addSwitch('s10', cls=OVSKernelSwitch)

    s17 = net.addSwitch('s17', cls=OVSKernelSwitch)

    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)

    s14 = net.addSwitch('s14', cls=OVSKernelSwitch)

    s11 = net.addSwitch('s11', cls=OVSKernelSwitch)

    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)

    s23 = net.addSwitch('s23', cls=OVSKernelSwitch)

    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)

    s18 = net.addSwitch('s18', cls=OVSKernelSwitch)

    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    s12 = net.addSwitch('s12', cls=OVSKernelSwitch)

    s21 = net.addSwitch('s21', cls=OVSKernelSwitch)

    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)

    s20 = net.addSwitch('s20', cls=OVSKernelSwitch)

    s16 = net.addSwitch('s16', cls=OVSKernelSwitch)

    s15 = net.addSwitch('s15', cls=OVSKernelSwitch)

    s9 = net.addSwitch('s9', cls=OVSKernelSwitch)



    info( '*** Add hosts\n')



    info( '*** Add links\n')

    net.addLink(s1, s4)

    net.addLink(s4, s5)

    net.addLink(s5, s10)

    net.addLink(s3, s6)

    net.addLink(s6, s7)

    net.addLink(s7, s8)

    net.addLink(s8, s9)

    net.addLink(s9, s15)

    net.addLink(s4, s7)

    net.addLink(s14, s15)

    net.addLink(s14, s16)

    net.addLink(s16, s19)

    net.addLink(s6, s11)

    net.addLink(s11, s12)

    net.addLink(s8, s12)

    net.addLink(s9, s18)

    net.addLink(s15, s17)

    net.addLink(s17, s18)

    net.addLink(s18, s2)

    net.addLink(s2, s13)

    net.addLink(s2, s23)

    net.addLink(s11, s13)



    info( '*** Starting network\n')

    net.build()

    info( '*** Starting controllers\n')

    for controller in net.controllers:

        controller.start()



    info( '*** Starting switches\n')

    net.get('s13').start([c0])

    net.get('s19').start([c0])

    net.get('s2').start([c0])

    net.get('s22').start([])

    net.get('s3').start([c0])

    net.get('s6').start([c0])

    net.get('s10').start([c0])

    net.get('s17').start([c0])

    net.get('s8').start([c0])

    net.get('s14').start([c0])

    net.get('s11').start([c0])

    net.get('s4').start([c0])

    net.get('s23').start([c0])

    net.get('s7').start([c0])

    net.get('s18').start([c0])

    net.get('s1').start([c0])

    net.get('s12').start([c0])

    net.get('s21').start([])

    net.get('s5').start([c0])

    net.get('s20').start([])

    net.get('s16').start([c0])

    net.get('s15').start([c0])

    net.get('s9').start([c0])



    info( '*** Post configure switches and hosts\n')



    CLI(net)

    net.stop()



if __name__ == '__main__':

    setLogLevel( 'info' )

    myNetwork()