#!/usr/bin/env python3
import ipaddress
import sys

print('\n'.join(map(str,sorted(ipaddress.ip_network(line.rstrip()) for line in sys.stdin))))
