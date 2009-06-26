#!/bin/bash

RTDIR=/usr/share/plcrt
${RTDIR}/getadmins.py | ${RTDIR}/adduserstort.pl priv -
