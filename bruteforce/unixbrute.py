import crypt
import argparse

def test_pass(crypt_pass, dict_file):
    salt = crypt_pass[0:2]
    dict_file = open(dict_file)
    for word in dict_file.readlines():
        word = word.strip('\n')
        crypt_word = crypt.crypt(word,salt)
        if(crypt_word == crypt_pass):
            print('[+] Found Password: {}'.format(crypt_pass))
            return
    print('[-] Password Not Found')
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',required=True,help='the file containing unix like passwords')
    parser.add_argument('-d','--dictionary',required=True,help='the file containing the password list')
    args = parser.parse_args()

    pass_file = open(args.file)
    for line in pass_file.readlines():
        if ':' in line:
            user = line.split(':')[0]
            crypt_pass = line.split(':')[1].strip('')
            print ('[*] Cracking password for user: {}'.format(user))
            test_pass(crypt_pass, args.dictionary)
if __name__=='__main__':
    main()
