import argparse
import numpy
from threading import *
from socket import *

verbosity_level = 0
screen_lock = Semaphore(value = 1)
def conn_scan(target_host, target_ports):
    global verbosity_level
    target_ports = list(map(int, target_ports))
    for target_port in target_ports:
        message = ''
        s = socket(AF_INET,SOCK_STREAM)
        try:
            s.connect((target_host,target_port))
            message += '[+] %d/tcp open'%target_port
        except:
            if verbosity_level > 0:
                message += '[-] %d/tcp closed'%target_port
                screen_lock.acquire()
                print(message)
                screen_lock.release()
            s.close()
            continue
        try:
            s.send('ViolentPython\r\n'.encode())
            r = s.recv(100)
            message += '\n[+] %s'%r.decode()
        finally:
            if message:
                screen_lock.acquire()
                print(message)
                screen_lock.release()
            s.close()


def port_scan(target_host, target_ports, max_threads):
    try:
        target_ip = gethostbyname(target_host)
    except Exception as ex:
        print("[-] Cannot resolve '%s': Unknown Host" % target_host)
        return
    try:
        target_name = gethostbyaddr(target_ip)
        print('\n[+] Scan Results for: ' + target_name[0])
    except:
        print('\n[+] Scan Results for: ' + target_ip)
    setdefaulttimeout(1)

    threads = []

    port_chunks = numpy.array_split(target_ports,max_threads)

    for chunk in port_chunks:
        t = Thread(target=conn_scan, args=(target_host, chunk))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def main():
    global verbosity_level
    parser = argparse.ArgumentParser(description='Python based port scanner')
    parser.add_argument('-H', '--host', required=True, help='specify target host')
    parser.add_argument('-p', '--ports', required=True,
                        help='specify ports separated by a comma all ports with a or specify 0-1024 with t')
    parser.add_argument('-v', '--verbose', action='count', default=0, help="specify higher verbosity with more v's")
    parser.add_argument('-t', '--threads', default=16, type=int)

    args = parser.parse_args()

    verbosity_level = args.verbose

    if args.ports == 'a':
        tgt_ports = [i for i in range(65536)]
    elif args.ports == 't':
        tgt_ports = [i for i in range(1025)]
    else:
        tgt_ports = str(args.ports).split(',')

    port_scan(args.host, tgt_ports, args.threads)


if __name__ == "__main__":
    main()
