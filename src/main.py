#!/usr/bin/env python
import sys

from pcap import Pcap
from pcap.Pcap import sniff

if __name__ == '__main__':
    sniff(*sys.argv[1:])
    print(Pcap.QUEUE.get())

