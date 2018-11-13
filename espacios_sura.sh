#!/bin/bash
export DB2HOME=/Users/coecogni/sqllib
export DYLD_LIBRARY_PATH="$DB2HOME/lib64:$ORACLE_HOME:$DYLD_LIBRARY_PATH"
export IBM_DB_HOME=/home/coecogni/sqllib
export DB2INSTANCE=coecogni
export DB2LIB=/home/coecogni/sqllib/lib
export DB2DIR=/opt/ibm/db2/V10.5
export LD_LIBRARY_PATH=/home/coecogni/espacios/lib:/usr/lib/oracle/11.2/client64/lib:/opt/ibm/db2/V10.5/lib64

cd /home/coecogni/
source espacios/bin/activate
/home/coecogni/espacios/bin/python /home/coecogni/espacios/run_espacios_sura.py

