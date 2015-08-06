# migrate-emails-from-cpanel-to-modoboa
A series of SSH commands executed via Python Fabric to generate import sheets for Modoboa Domains and Identities

Uses Python Fabric. For more information on how to use Fabirc please visit http://www.fabfile.org/

## Commands

### get_imap_vhost_accounts_users
 * iterates through cpanel virtual hosts in /home directory to produce a list of virtual host paths.
 * iterates through the virtual host paths to identify and produce a list of email accounts
 * iterates through the email accounts to produce a list of email users
 * outputs data to imap_users.txt
 
### build_modoboa_account_list
 * creates two output files modoboa_identifiers.txt and modoboa_domains.txt to be used to with the bulk importer via modoboa.

## Useage example

 * $ fab host_ws1 get_imap_vhost_accounts_users
 * $ fab host_local build_modoboa_account_list

