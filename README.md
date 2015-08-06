# migrate-emails-from-cpanel-to-modoboa
A series of SSH commands executed via Python Fabric to generate import sheets for Modoboa Domains and Identities

## Commands

### get_imap_vhost_accounts_users
 * iterates through cpanel virtual hosts in /home directory to produce a list of virtual host paths.
 * iterates through the virtual host paths to identify and produce a list of email accounts
 * iterates through the email accounts to produce a list of email users
 * outputs data to imap_users.txt
 
### build_modoboa_account_list
 * creates two output files modoboa_identifiers.txt and modoboa_domains.txt to be used to with the bulk importer via modoboa.

Enjoy!
