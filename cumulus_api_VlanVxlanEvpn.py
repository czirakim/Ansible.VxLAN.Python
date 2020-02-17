import requests 
from var import vlans,id,clagid,spinenumber
#suppressing ssl warnings
requests.packages.urllib3.disable_warnings() 


# http headers
httpheaders = {'Content-Type': 'application/json',
           'Authorization': 'Basic Y3VtdWx1czpDdW11bHVzTGludXgh' }


def post(com,dev_id):
      command = com
      api_url = "https://10.0.0.%i:8080/nclu/v1/rpc" % (dev_id)
      payload = '{"cmd": %s}' % (command)
      request = requests.post(api_url,headers=httpheaders,data = payload,verify=False)
#      r_url = request.text
#      print("reply is:%s"%r_url)


def create_vlan(b):
    for m in vlans:
      c = vlans.index(m) + 20
      n = hex(c).lstrip("0x")
      command = '"add vlan %i"' % (m)
      post(command,b)
      command = '"add vlan %i ip address 192.168.%i.24%i/24"' % (m,m,b)
      post(command,b)
      command = '"add bond bond%i bridge trunk vlans %i"' % (clagid,m)
      post(command,b)
      command = '"add vlan %i ip address-virtual 00:00:5e:00:01:%s 192.168.%i.254/24"'   % (m,n,m)
      post(command,b)
      print("vlan %i has been created on device %i" ) % (m,b)

def create_vxlan(b):
      for m in vlans:
            command = '"add vxlan vni%i vxlan id %i "' % (m,m)
            post(command,b)
            command = '"add vxlan vni%i bridge access %i"' % (m,m)
            post(command,b)
            command = '"add vxlan vni%i bridge learning off"' % (m)
            post(command,b)
            command = '"add vxlan vni%i stp bpduguard"' % (m)
            post(command,b)
            command = '"add vxlan vni%i stp portbpdufilter"' % (m)
            post(command,b)
            command = '"add vxlan vni%i vxlan local-tunnelip 10.1.1.%i"' % (m,b)
            post(command,b)
            command = '"add vxlan vni%i bridge arp-nd-suppress on"' % (m)
            post(command,b)
            print("vxlan %i has been created on device %i" ) % (m,b)


def create_evpn(b):
          command = '"add loopback lo ip address 10.1.1.%i/32 "' % (b)
          post(command,b)
          command = '"add bgp autonomous-system 6500%i"' % (b)
          post(command,b)
          command = '"add bgp neighbor swp1-%i interface remote-as external"' % (spinenumber)
          post(command,b)
          command = '"add bgp l2vpn evpn neighbor swp1-%i activate"' % (spinenumber)
          post(command,b)
          command = '"add bgp l2vpn evpn advertise-all-vni"'
          post(command,b)
          command = '"add bgp network 10.1.1.%i/32"' % (b)
          post(command,b)
          print("BGP eVPN  is done on device %i " ) % (b)

def create_VTEPanycast(b):
       y = b+1
       if b%2 == 0:
          command = '"add loopback lo clag vxlan-anycast-ip 10.10.10.%i"' % (b)
          post(command,b)
          command = '"add bgp network 10.10.10.%i/32 "' % (b)
          post(command,b) 
       else:
          command = '"add loopback lo clag vxlan-anycast-ip 10.10.10.%i"' % (y)
          post(command,b)
          command = '"add bgp network 10.10.10.%i/32 "' % (y)
          post(command,b) 
       print("VTEP anycast  is done on device %i " ) % (b)

def create_clagRole(b):
       if b%2 == 0:
          command = '"add clag peer sys-mac 44:38:39:FF:01:01 interface swp5-6 secondary"' 
          post(command,b)
       else:
          command = '"add clag peer sys-mac 44:38:39:FF:01:01 interface swp5-6 primary"'
          post(command,b)


for dev in id:
    command = '"add clag port bond bond%i interface swp3 clag-id %i"' % (clagid,clagid)
    post(command,dev) 
    create_clagRole(dev)
    create_vlan(dev)
    create_vxlan(dev)
    create_evpn(dev)
    create_VTEPanycast(dev)
    command = '"commit"' 
    post(command,dev) 
    print("config commited on device %i") % (dev) 
