#!/bin/bash

# Set access for python script to use port 80
setcap 'cap_net_bind_service=+ep' /usr/bin/python3.10

# Remove access for python script to use port 80
#setcap -r /usr/bin/python3.10
