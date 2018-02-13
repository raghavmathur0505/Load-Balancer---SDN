#import libraries and packages
from pox.lib.revent import event_cont,EventHalt
import pox.openflow.libopenflow_01 as of
from pox.core import core
from pox.lib.addresses import IPAddr,EthAddr,parse_cidr
from pox.lib.util import dpidToStr
import sys
import random

log = core.getLogger()

#global variables

#ip and mac for load balancer
load_balancer_hardcoded_ip = IPAddr("10.0.0.5")
virtual_mac = EthAddr("00:00:00:00:00:05")


#assigning ip and weights for the other 3 servers
topology_server = {}
topology_server[0] = {'ip':IPAddr("10.0.0.2"), 'mac':EthAddr("00:00:00:00:00:02"), 'outport': 2,'weight':int(3)}
topology_server[1] = {'ip':IPAddr("10.0.0.3"), 'mac':EthAddr("00:00:00:00:00:03"), 'outport': 3,'weight':int(2)}
topology_server[2] = {'ip':IPAddr("10.0.0.4"), 'mac':EthAddr("00:00:00:00:00:04"), 'outport': 4,'weight':int(1)}
server_no = len(topology_server)

server_no = 0 


#handling packets received from clients

def packet_handler (event):
    global server_no 
    packet = event.parsed

    # Only handle traffic destined to virtual IP
    if (not event.parsed.find("ipv4")):
        return event_cont

    message = of.ofp_flow_mod()
    message.match = of.ofp_match.from_packet(packet)

     # Handing requests routed to the Load Balancer Ip
    if (message.match.nw_dst != load_balancer_hardcoded_ip):
        return event_cont

    # Random selection of servers
    iterator = random.randint(0,server_no-1)
    print iterator
    serverip = topology_server[iterator]['ip']
    selected_server_mac = topology_server[iterator]['mac']
    server_output = topology_server[iterator]['outport']

     # Route followed to server
    message.buffer_id = event.ofp.buffer_id
    message.in_port = event.port

    message.actions.append(of.ofp_action_dl_addr(of.OFPAT_SET_DL_DST, selected_server_mac))
    message.actions.append(of.ofp_action_nw_addr(of.OFPAT_SET_NW_DST, serverip))
    message.actions.append(of.ofp_action_output(port = server_output))
    event.connection.send(message)

   # Route from server to load balancer
    reply = of.ofp_flow_mod()
    reply.buffer_id = None
    reply.in_port = server_output

    reply.match = of.ofp_match()
    reply.match.dl_src = selected_server_mac
    reply.match.nw_src = serverip
    reply.match.tp_src = message.match.tp_dst

    reply.match.dl_dst = message.match.dl_src
    reply.match.nw_dst = message.match.nw_src
    reply.match.tp_dst = message.match.tp_src

    reply.actions.append(of.ofp_action_dl_addr(of.OFPAT_SET_DL_SRC, virtual_mac))
    reply.actions.append(of.ofp_action_nw_addr(of.OFPAT_SET_NW_SRC, load_balancer_hardcoded_ip))
    reply.actions.append(of.ofp_action_output(port = message.in_port))
    event.connection.send(reply)

    return EventHalt

def launch ():
    # To intercept packets before the learning switch
    core.openflow.addListenerByName("PacketIn", server_no, priority=2)

    log.info("Stateless LB running.")
