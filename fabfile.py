#!/bin/python
'''
A series of SSH commands executed via Python Fabric to generate 
import sheets for Modoboa Domains and Identities
'''
from fabric.api import *
from progressbar import ProgressBar
import os
import hashlib
import uuid

pbar = ProgressBar()

def host_local():
    env.hosts = ['localhost']
    return env

def host_ws1():
    env.hosts = ['example.domain.com']
    env.user = 'superuser'
    env.passwords = {'superuser@example.domain.com': 'password'}
    env.key_filename = 'your-ssh-key'
    return env

def host_srv1():
    env.hosts = ['srv1.awebmail.net.au']
    env.user = 'admin'
    env.passwords = {'superuser@example.domain.com': 'password'}
    env.key_filename = 'your-ssh-key'
    return env


# Commands
def local_uname():
    local('uname -a')

def remote_uname():
    run('uname -a')

def output_clean(o):
    accounts = []
    o = o.split("\r\n")

    for i in o:
        i.strip("'")
        accounts.append(i)

def file_to_list(n):
    with open(n) as f:
        list = f.read().splitlines()
    return list

def list_to_file(l,n):
    if not os.path.exists(n):
        file(n, 'w').close()

    with open(n,'w') as f:
        f.write('\n'.join(l))

def get_imap_vhosts():
    vhosts = run('for D in /home/*; do if [ -d "${D}/mail/" ]; then echo ${D} | rev | cut -d "/" -f1 | rev;  fi; done')
    return vhosts

def get_imap_vhosts_path():
    vhosts = run('for D in /home/*; do if [ -d "${D}/mail/" ]; then echo ${D};  fi; done')
    return vhosts

def get_imap_vhost_accounts():
    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only=True
        ):
        vhosts = get_imap_vhosts_path()
        vhosts = vhosts.split()
        accounts = []
        for i in pbar(vhosts):
            account = run("find %s/mail/ -mindepth 1 -maxdepth 1 -type d -name '[a-z]*.*'" % (i))
            account = account.split("\r\n")

            for i in account:
                i.strip("'")
                accounts.append(i)

            accounts = filter(None, accounts)

    return accounts

def get_imap_vhost_accounts_users():
    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only=True
        ):

        accounts = get_imap_vhost_accounts()
        users = []

        for i in accounts:
            user = run("find %s -mindepth 1 -maxdepth 1 -type d" % (i))
            user = user.split("\r\n")

            for i in user:
                i.strip("'")
                users.append(i)

            users = filter(None, users)

    list_to_file(users,'imap_users.txt')

    return

def get_imap_accounts(user, fqdn):
    '''
    Useage Example
    fab host_ws1 get_imap_accounts:user=codeberg,fqdn=codeberg.com.au
    '''
    fqdn_path = run('find /home/%s/mail/ -type d -name %s' % (user, fqdn))
    account = run('find %s -mindepth 1 -maxdepth 1 -type d | rev | cut -d "/" -f1 | rev' % (fqdn_path))
    accounts = account.split()
    return accounts

def get_imap_accounts_path(user, fqdn):
    '''
    Useage Example
    fab host_ws1 get_imap_accounts:user=codeberg,fqdn=codeberg.com.au
    '''
    fqdn_path = run('find /home/%s/mail/ -type d -name %s' % (user, fqdn))
    account = run('find %s -mindepth 1 -maxdepth 1 -type d' % (fqdn_path))
    accounts = account.split()
    return accounts

def pack_imap_accounts(user):
    with settings(sudo_user='root', password='qq12angela'):
        sudo('tar -zcvf ../%s %s.tgz' % (user, user))


def make_imap_destination(accounts):
    with settings(sudo_user='root', password='qq12angela'):
        for user in accounts:
            sudo('mkdir /home/vmail/%s/%s/Maildir' % (fqdn, user))

def build_email_list():
    emails = []
    admins = []
    paths = file_to_list('imap_users.txt')
    for i in paths:
        delimiter = i.count('/')
        output = i.split('/', delimiter )
        emails.append('admin@' + output[-2] + ',' + output[-1] + "@" + output[-2])
        admins.append('admin@' + output[-2] + ',' + 'admin@' + output[-2])

    admins = list(set(admins))
    list_to_file(emails, 'email_list.txt')
    list_to_file(admins, 'admin_list.txt')

def build_modoboa_account_list():
    admins = file_to_list('admin_list.txt')
    emails = file_to_list('email_list.txt')




    modoboa = []
    modoboa_emails = []
    modoboa_admins = []
    modoboa_domains = []

    for i in emails:
        # generate salt, random password and encrypt
        #s = uuid.uuid4().hex
        p = uuid.uuid4().hex
        #password = hashlib.sha512( s + p ).hexdigest()
        delimiter = i.count('@')
        domain = i.split('@', delimiter )

        delimiter = i.count(',')
        e = i.split(',', delimiter )

        modoboa_emails.append('account,' + e[1] + ',' + p + ',' + ',' + ',' + 'True,' + 'SimpleUsers,' + e[1] + ',4000,' +  domain[-1])

    for i in admins:
        delimiter = i.count('@')
        domain = i.split('@', delimiter )

        # generate salt, random password and encrypt
        #s = uuid.uuid4().hex
        p = uuid.uuid4().hex
        #password = hashlib.sha512( s + p ).hexdigest()
        modoboa_admins.append('account,' + e[1] + p + ',' + ',' + ',' + 'True,' + 'DomainAdmins,' + e[1] + ',4000,' + domain[-1])
        modoboa_domains.append('domain,' + domain[-1] + ',4000,' + 'True' )


    all_emails = modoboa_admins + modoboa_emails
    all_emails = sorted(all_emails)

    modoboa_domains = list(set(modoboa_domains))

    list_to_file(all_emails, 'modoboa_identifiers.txt')
    list_to_file(modoboa_domains, 'modoboa_domains.txt')


def be_root():
    with settings(sudo_user='root', password='qq12angela'):
        sudo('whoami')



