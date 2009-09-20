#!/bin/bash

D=/usr/share/plcrt/
for f in $D/cron.d/*.py ; do
	$f
done
