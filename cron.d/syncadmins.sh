#!/bin/bash

RTDIR=/usr/share/plcrt
${RTDIR}/callplcsh.py ${RTDIR}/getpersons.py admin | ${RTDIR}/adduserstort.pl priv -
