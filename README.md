<snippet>
  <content>

## Python.VxLAN.Cumulus

The scope of this project is to automate the deployment of vxlan's on Cumulus switches,
<br>and use evpn as a control-plane mechanism. But this time using the API for the Cumulus
<br>switches and using python (Python 2.7.17). This project only applies to leaf switches.  

## Usage

The project is made of 2 files. One with variables like: a list of vlans,
<br>the number of spines switches a leaf switch is attached to, clagid which in 
<br>my case is 1 but it can be a list and in this case the script needs to be changed a little bit.
<br>Also the id of the device which is used for ip's, AS number.
<br>The main python file contains a function for each task that is needed.
<br>Example: create_vlan, create_vxlan, create_evpn ...
<br>In case you want only to create a new vlan and it's corresponding vxlan on all the switches
<br> you can comment the other functions, like create_evpn, create_VTEPanycast, create_clagRole.
<br> If you want to run only on specific switches you need to edit the id list in the var.py file.  
  

## Files
Variables file : var.py
<br>Script: cumulus_api_VlanVxlanEvpn.py

## Update
03/03/2020
I've added a function(conf_pending) to capture the config that it's commited and save it in a file for each
<br> device. The file will aslo have the date/time when it was captured in it's name.

## Credits
This was written by Mihai Cziraki
</content>
</snippet>
