#!/bin/env plcsh

p = GetPersons(None, ['email', 'first_name', 'last_name', 'roles', 'site_ids'])

admins = filter(lambda x: 'admin' in x['roles'], p)

for a in admins:
	s = GetSites(a['site_ids'], ['name'])
	if len(s) > 0:
		organization = s[0]['name']
	else:
		organization = "Unknown"
	a['name'] = organization
	print "%(email)s,%(first_name)s %(last_name)s,%(name)s" % a
