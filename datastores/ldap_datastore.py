from django.core.mail import mail_admins
from django.conf import settings

from placard.connection import LDAPConnection

import base


class PersonalDataStore(base.PersonalDataStore):
    
    def create_new_user(self, data, hashed_password=None):
        return super(PersonalDataStore, self).create_new_user(data, hashed_password=None)

    def activate_user(self, person):
        person = super(PersonalDataStore, self).activate_user(person)

        attrs = {}
        attrs['uid'] = str(person.username)
        attrs['givenName'] = str(person.first_name)
        attrs['sn'] = str(person.last_name)
        attrs['telephoneNumber'] = str(person.telephone)
        attrs['mail'] = str(person.email)
        attrs['o'] = str(person.institute.name)
        attrs['userPassword'] = str(person.user.password)
        
        conn = LDAPConnection()
        conn.add_user(**attrs)
        person.save(update_datastore=False)

        return person

    def delete_user(self, person):
        super(PersonalDataStore, self).delete_user(person)

        conn = LDAPConnection()
        conn.delete_user(person.user.username)
        

    def update_user(self, person):
        super(PersonalDataStore, self).update_user(person)

        conn = LDAPConnection()
    
        conn.update_user(
            person.username,
            cn='%s %s' % (str(person.first_name), str(person.last_name)),
            givenName=str(person.first_name),
            sn=str(person.last_name),
            telephoneNumber=str(person.telephone),
            mail=str(person.email),
            o=str(person.institute.name),
            )

    def is_locked(self, person):
        super(PersonalDataStore, self).is_locked(person)

        conn = LDAPConnection()
        ldap_user = conn.get_user('uid=%s' % person.username)

        if hasattr(ldap_user, 'nsAccountLock'):
            return True

        return False


    def lock_user(self, person):
        super(PersonalDataStore, self).lock_user(person)
        
        conn = LDAPConnection()
        conn.update_user(
            person.username,
            nsRoleDN='cn=nsManagedDisabledRole,dc=vpac,dc=org',
            )

    def unlock_user(self, person):
        super(PersonalDataStore, self).unlock_user(person)
        
        conn = LDAPConnection()
        dn="uid=%s,%s" % (person.username, settings.LDAP_USER_BASE)
        old = {
            'nsRoleDN': 'cn=nsManagedDisabledRole,dc=vpac,dc=org',
            }
        new = {}
        conn.update_ldap(dn, old, new)
        


class AccountDataStore(base.AccountDataStore):

    def create_account(self, person, default_project):
        ua = super(AccountDataStore, self).create_account(person, default_project)
            
        conn = LDAPConnection()
        
        #TODO - Get generated attrs from ldap_attrs.py
        conn.update_user(
            person.username,
            gecos='%s %s (%s)' % (str(person.first_name), str(person.last_name), str(person.institute.name)),
            uidNumber=conn.get_new_uid(),
            gidNumber=str(person.institute.gid),
            homeDirectory='/home/%s' % str(person.username),
            loginShell='/bin/bash',
            objectClass=['top','person','organizationalPerson','inetOrgPerson', 'shadowAccount','posixAccount']
            )

        return ua


    def delete_account(self, ua):
        super(AccountDataStore, self).delete_account(ua)

        conn = LDAPConnection()

        #TODO - Get generated attrs from ldap_attrs.py

        conn.update_user(
            ua.username,
            gecos='', 
            uidNumber='',
            gidNumber='',
            homeDirectory='',
            loginShell='',
            objectClass=['top','person','organizationalPerson','inetOrgPerson', 'shadowAccount',]
            )


    def update_account(self, ua):

        super(AccountDataStore, self).update_account(ua)

        conn = LDAPConnection()

        conn.update_user(
            ua.user.username,
            gecos='%s %s (%s)' % ((ua.user.first_name), str(ua.user.last_name), str(ua.user.institute.name)),
            gidNumber=str(ua.user.institute.gid),
            )


    def lock_account(self, ua):
        super(AccountDataStore, self).lock_account(ua)

        conn = LDAPConnection()
        
        conn.update_user(
            ua.username,
            loginShell='/usr/local/sbin/insecure'
            )
        

    def unlock_account(self, ua):
        super(AccountDataStore, self).unlock_account(ua)

        conn = LDAPConnection()
        conn.update_user(ua.username, loginShell=settings.SHELLS[0][0])
        

