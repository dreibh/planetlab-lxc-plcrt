#!/bin/bash

RTDIR=/usr/share/plcrt
${RTDIR}/callplcsh.py ${RTDIR}/getadmins.py admin | ${RTDIR}/adduserstort.pl priv -
