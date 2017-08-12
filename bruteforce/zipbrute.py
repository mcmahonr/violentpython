import zipfile
import argparse
import os
import sys
from threading import Thread

def extract_file(zip_file, password, verbosity=0):
    try:
        if verbosity > 0:
            print('Trying password {}'.format(password))
        zip_file.extractall(pwd=password)
        print ('[+] Found password {}\n'.format(password))
    except Exception as e:
        print(str(e))
        if verbosity > 0:
            print('[-] Incorrect password')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help='the zip file to try to extract')
    parser.add_argument('-d', '--dictionary', required=True, help='the list of passwords to try against the zip file')
    parser.add_argument('-v', '--verbosity', action='count', help='increase the output verbosity level', default=0) 
    args = parser.parse_args()
    
    if not os.path.isfile(args.file):
        print ('The zip file {} does not exist'.format(args.file))
        parser.print_help()
        sys.exit(1)
    if not os.path.isfile(args.dictionary):
        print ('The dictionary file {} does not exist'.format(args.dictionary))
        parser.print_help()
        sys.exit(2)

    zip_file = zipfile.ZipFile(args.file)
    pass_file = open(args.dictionary)
    threads = []
    for line in pass_file.readlines():
        password = line.strip('\n').encode('utf-8')
        t = Thread(target=extract_file, args=(zip_file, password, args.verbosity))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

if __name__=='__main__':
    main()
    


    

