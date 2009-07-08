#!/bin/bash

RTDIR=/usr/share/plcrt
for f in /etc/rt3/conf.d/*.pl ; do 
	$RTDIR/addwatchers.pl --action insert --dba postgres --datafile $f
done
