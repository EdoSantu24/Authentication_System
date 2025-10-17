#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.util import dumpNetConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class MyTopo(Topo):
      
    def __init__(self, **opts):
        Topo.__init__(self, **opts)

        switches = []
        hosts = []

        # Add 4 switches with OpenFlow 1.3 protocol
        for i in range(4):
            switches.append(self.addSwitch('s'+str(i + 1), cls=OVSSwitch, protocols='OpenFlow13'))
            
        # Add 4 hosts
        for i in range(4):
            hosts.append(self.addHost('h'+str(i + 1)))     

        # Connect switches in a mesh-like structure
        self.addLink(switches[0], switches[1], bw=100, max_queue_size=1000)
        self.addLink(switches[0], switches[3], bw=100, max_queue_size=1000)
        self.addLink(switches[1], switches[2], bw=100, max_queue_size=1000)

        # Connect each switch to one host
        self.addLink(switches[0], hosts[0], bw=100, max_queue_size=1000)  # h1
        self.addLink(switches[0], hosts[1], bw=100, max_queue_size=1000)  # h2
        self.addLink(switches[2], hosts[2], bw=100, max_queue_size=1000)  # h3
        self.addLink(switches[3], hosts[3], bw=100, max_queue_size=1000)  # h4

topos = {'mytopo': (lambda: MyTopo())}

class ONOSController(RemoteController):
    def __init__(self):
        RemoteController.__init__(self, 'ONOSController', '127.0.0.1', 6633)

controllers = {'onos': ONOSController}

def perfTest():
    topo = MyTopo()
    net = Mininet(topo=topo, controller=None, link=TCLink, listenPort=6634)
   
    # Add ONOS controller
    c0 = ONOSController()
    net.addController(c0)

    # Set custom MAC addresses
    hosts = net.hosts
    hosts[0].setMAC("00:00:00:00:00:01", intf='h1-eth0')
    hosts[1].setMAC("00:00:00:00:00:02", intf='h2-eth0')
    hosts[2].setMAC("00:00:00:00:00:03", intf='h3-eth0')
    hosts[3].setMAC("00:00:00:00:00:04", intf='h4-eth0')

    switches = net.switches
    switches[0].setMAC("00:00:00:01:00:01", intf='s1-eth1')
    switches[1].setMAC("00:00:00:02:00:01", intf='s2-eth1')
    switches[2].setMAC("00:00:00:03:00:01", intf='s3-eth1')
    switches[3].setMAC("00:00:00:04:00:01", intf='s4-eth1')

    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    #dumpNetConnections(net)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')   
    perfTest()
