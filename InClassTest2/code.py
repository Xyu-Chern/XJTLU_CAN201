from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Host
from mininet.node import OVSKernelSwitch
from mininet.log import setLogLevel, info


def myTopo():
    net = Mininet(topo=None, autoSetMacs=False, build=False, ipBase='10.21.156.0/24')

    h1 = net.addHost('h1', cls=Host, defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, defaultRoute=None)

    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')

    # Add links
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    net.addLink(h1, s2)
    net.addLink(h2, s2)

    net.addLink(h1, s3)
    net.addLink(h2, s3)
    net.build()

    # Assign IP addresses to interfaces of hosts
    h1.setIP(intf="h1-eth0", ip="10.21.156.11/24")
    h1.setIP(intf="h1-eth1", ip="10.21.156.22/24")
    h1.setIP(intf="h1-eth2", ip="10.21.156.33/24")

    h2.setIP(intf="h2-eth0", ip="10.21.156.111/24")
    h2.setIP(intf="h2-eth1", ip="10.21.156.112/24")
    h2.setIP(intf="h2-eth2", ip="10.21.156.113/24")

    # Network build and start
    net.start()

    # CLI mode running
    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    myTopo()