import concurrent.futures as conc
import multiprocessing as mp
import netifaces

import pyshark
from robot.libraries.BuiltIn import BuiltIn

from pcap import HttpParser

QUEUE = mp.Queue(1)
FUTURE = None

def _sniffer_thread(dest_host, uri="/", protocol='http', iface='wlp4s0'):
    local_ip = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
    cap_filter = 'src host {} and dst host {}'.format(local_ip, dest_host)

    capture = pyshark.LiveCapture(interface=iface, display_filter=protocol, bpf_filter=cap_filter)

    for packet in capture.sniff_continuously():
        message = HttpParser.RequestMessage(payload(packet))
        BuiltIn().log_to_console(message.request_uri)
        if message.request_method == 'POST' and message.request_uri == uri:
            QUEUE.put(HttpParser.parse_url_encoding(message))
            return


def sniff(dest_host, uri="/", protocol='http', iface='wlp4s0'):
    # return _sniffer_thread(dest_host, uri, protocol, iface)

    # thread = threading.Thread(target=_sniffer_thread, args=(dest_host, uri, protocol, iface))
    # thread.start()

    mp.Process(target=_sniffer_thread, args=(dest_host, uri, protocol, iface)).start()

    # with conc.ProcessPoolExecutor(1) as executor:
    #     global Future
    #     Future = executor.submit(_sniffer_thread, dest_host, uri, protocol, iface)

def payload(pack):
    if 'tcp' in pack and 'payload' in pack.tcp.field_names:
        val = pack.tcp.payload.show
        val = ''.join(val.split(':'))

        return bytearray.fromhex(val).decode('ASCII')
    else:
        return ''

# def _sniff_handler(packet):
#     message = http_parser.RequestMessage(payload(packet))
#     if message.request_method == 'POST' and message.request_uri == '/Login':
#         print(message.body)
#         print(http_parser.parse_url_encoding(message))
#     print('request_method: ', message.request_method, ', request_uri: ', message.request_uri, ', body: ', parse_url_encoding(message),
#           end='\n')


# def get_payload(cap_file, display_filter='http'):
#     cap = pyshark.FileCapture(cap_file, display_filter)
#     for pack in cap:
#         if 'http' in pack:
#             if 'request_method' in pack.http.field_names and 'request_uri' in pack.http.field_names:
#                 if pack.http.request_uri == '/Login' and pack.http.request_method == 'POST':
#                     pl = payload(pack)
#                     message = RequestMessage(pl)
#                     print('body: ', message.body)
