#!/bin/bash

D=/usr/share/plcrt/
for f in $D/cron.d/*.sh ; do
	bash -c "$f"
done
