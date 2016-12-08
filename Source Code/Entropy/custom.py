"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.

Source : Mininet Walkthrough
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        host1 = self.addHost( 'h1' )
        host2 = self.addHost( 'h2' )
        switch = self.addSwitch( 's1' )

        # Add links
        self.addLink( host1, switch )
        self.addLink( host2, switch )

topos = { 'mytopo': ( lambda: MyTopo() ) }
