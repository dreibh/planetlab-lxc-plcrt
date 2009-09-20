#!/bin/env plcsh

import sys

p = GetPersons(None, ['email', 'first_name', 'last_name', 'roles', 'site_ids'])

admins = filter(lambda x: sys.argv[1] in x['roles'], p)

for a in admins:
    if 'site_ids' in a:
        s = GetSites(a['site_ids'], ['name'])
        if len(s) > 0:
            organization = s[0]['name']
        else:
            organization = "Unknown"
    else:
        organization = "Unknown"

    a['name'] = organization
    print "%(email)s,%(first_name)s %(last_name)s,%(name)s" % a
