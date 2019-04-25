#!/usr/bin/env bash
# FIXME
sed -i -e ':a' -e 'N' -e '$!ba' -e 's/%}\n/%}/g' Makefile
sed -i -e ':a' -e 'N' -e '$!ba' -e 's/^\s*{%/{%/g' Makefile
#cat -s Makefile | tee Makefile >/dev/null
sed -i -e ':a' -e 'N' -e '$!ba' -e 's/%}\n/%}/g' setup.py
sed -i -e ':a' -e 'N' -e '$!ba' -e 's/^\s*{%/{%/g' setup.py
#cat -s setup.py | tee setup.py >/dev/null
