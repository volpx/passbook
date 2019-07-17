#!/usr/bin/env python3
version='1.0'
author='Filippo Volpe'
email='filippovolpe98@gmail.com'

vault_filen='/home/volpe/Documents/passbook_vault.yeet'
clear_keys=['id','name','username']

import argparse
import getpass
import json
import hashlib
from Crypto.Cipher import AES
import random
import struct

def main():
    parser=argparse.ArgumentParser(
        description='Shitty password manager',
        )

    # subparsers
    subparsers=parser.add_subparsers(title='subcommands',dest='sub')
    #
    parser_add=subparsers.add_parser('init',help='init vault')
    #
    parser_add=subparsers.add_parser('add',help='add record')
    parser_add.add_argument('-n','--name',help='record name',metavar='NAME')
    parser_add.add_argument('-u','--username',help='username',metavar='USERNAME')
    parser_add.add_argument('-d','--description',help='additional clear description',metavar='DESCR')
    parser_add.add_argument('-p','--no-password',help='don\'t ask a password',action='store_true')
    #
    parser_rm=subparsers.add_parser('rm',help='rm record')
    parser_rm.add_argument('id',help='id to remove',metavar='ID')
    #
    parser_show=subparsers.add_parser('sh',help='show record')
    parser_show.add_argument('-a','--all',help='show everything',action='store_true')
    parser_show.add_argument('-i','--id',help='id to show',metavar='ID')

    # parse
    args=parser.parse_args()

    # handle
    if args.sub is None:
        pass
    elif args.sub == 'add':
        add(args)
        pass
    elif args.sub == 'rm':
        rm(args)
    elif args.sub == 'sh':
        show(args)
    elif args.sub == 'init':
        init()

def encrypt(datas,filen,p):
    # initialization cryptor
    iv = ''.join(chr(random.randint(0x20, 0x7E)) for i in range(16)).encode('utf-8')
    cryptor = AES.new(p, AES.MODE_CBC, iv)
    # write
    with open(filen,'wb') as f:
        f.write(struct.pack('<Q',len(datas))+iv)
        datas=datas+' '.encode('utf-8')*(16-len(datas)%16)
        f.write(cryptor.encrypt(datas))
def decrypt(filen,p):
    with open(filen,'rb') as f:
        # create decryptor
        size=struct.unpack('<Q',f.read(struct.calcsize('Q')))[0]
        iv=f.read(16)
        cryptor=AES.new(p,AES.MODE_CBC,iv)
        # read the vault
        datas=cryptor.decrypt(f.read())[:size]
        return datas

def init():
    empty_vault={'last_id':0,'recs':[]}
    # ask new master pass
    p = hashlib.sha256(getpass.getpass(prompt='New master pass:').encode('utf-8')).digest()
    p1 = hashlib.sha256(getpass.getpass(prompt='Retype master pass:').encode('utf-8')).digest()
    if p != p1:
        print('Does not match')
        return
    vault_string=json.dumps(empty_vault).encode('utf-8')
    encrypt(vault_string,vault_filen,p)

def add(args):
    def get_new_id(vault):
        vault['last_id']+=1
        return vault['last_id']

    # Create empty element
    rec={}
    # Add the fields
    if args.name is not None:
        rec['name']=args.name
    if args.description is not None:
        rec['description']=args.description
    if args.username is not None:
        rec['username']=args.username
    if not args.no_password:
        rec['password']=getpass.getpass(prompt='Pass:')

    p = hashlib.sha256(getpass.getpass(prompt='Master pass:').encode('utf-8')).digest()

    vault=json.loads(decrypt(vault_filen,p))
    rec['id']=get_new_id(vault)
    vault['recs'].append(rec)

    #recrypt
    encrypt(json.dumps(vault).encode('utf-8'),vault_filen,p)

def rm(args):
    p = hashlib.sha256(getpass.getpass(prompt='Master pass:').encode('utf-8')).digest()
    vault=json.loads(decrypt(vault_filen,p))
    for el in vault['recs']:
        if el['id'] == args.id:
            vault['rec'].remove(el)
            break
    #recrypt
    encrypt(json.dumps(vault).encrypt('utf-8'),vault_filen,p)

def show(args):
    p = hashlib.sha256(getpass.getpass(prompt='Master pass:').encode('utf-8')).digest()
    vault=json.loads(decrypt(vault_filen,p))
    for el in vault['recs']:
        if args.id is not None:
            if el['id'] != args.id:
                break
        if args.all:
            print(el)
        else:
            tmpdic={}
            for key,value in el.items():
                if key in clear_keys:
                    tmpdic={**tmpdic,key:value}
            print(tmpdic)

if __name__=='__main__':
    main()
