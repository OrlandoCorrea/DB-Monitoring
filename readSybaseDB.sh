#!/bin/bash

export FECHA=`/bin/date +%Y-%m-%d`
export ini=/home/coecogni/espacios/todos.sybase
FECHA="$FECHA 13:30:40"
RUTA_code="/home/coecogni/espacios/codes.isql"

while read line
do
    typedb=`echo $line | awk -F\, '{print $1}'`
    cliente=`echo $line | awk -F\, '{print $2}'`
    descripcion=`echo $line|awk -F\, '{print $3}'`
    user_unix=`echo $line|awk -F\, '{print $4}'`
    pass_unix=`echo $line|awk -F\, '{print $5}'`
    alias=`echo $line|awk -F\, '{print $6}'`
    sid=`echo $line|awk -F\, '{print $7}'`
    host=`echo $line|awk -F\, '{print $8}'`
    ip=`echo $line|awk -F\, '{print $9}'`
    userdb=`echo $line|awk -F\, '{print $10}'`
    passdb=`echo $line|awk -F\, '{print $11}'`
    echo "$typedb,$cliente,$descripcion,$user_unix,$pass_unix,$alias,$sid,$host,$ip,$userdb,$passdb"
 
    RUTE=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o ConnectTimeout=10 -o "StrictHostKeyChecking no" $user_unix@$ip "pwd") 2>&1 >/dev/null && status1="OK" || status1="FAIL";

    if [ "$status1" == "FAIL" ];then
    
	echo "ERROR CREDENCIALES EN EL SISTEMA $sid DEL CLIENTE $cliente, PORFAVOR REVISAR"
    
    else

	    SSHPASS=$pass_unix sshpass -e $pass scp -pr $RUTA_code $user_unix@$ip:$RUTE 

	    echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip << EOF
isql -S'$sid' -U'$userdb' -P'$passdb' -X -w2000 -i'$RUTE/codes.isql' > $RUTE/output_file_sid;
EOF

	    DATABASE_SIZE_sid_log=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 4 { print \$5 } ' ")

	    if [ "$DATABASE_SIZE_sid_log" == "NULL" ];then
        	DATABASE_SIZE_sid=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 4 { print \$2 } ' ")
	        DATABASE_USED_sid=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 4 { print \$3 } ' ")
	        DATABASE_FREE_sid=$(awk '{print $1-$2}' <<<"$DATABASE_SIZE_sid $DATABASE_USED_sid");
	    else
	        DATABASE_SIZE_sid=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 4 { print \$2 } ' ")
	        DATABASE_USED_sid=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 4 { print \$3 } ' ")
	        DATABASE_FREE_sid_log=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 4 { print \$6 } ' ")
	        DATABASE_USED_sid_log=$(awk '{print $1-$2}' <<<"$DATABASE_SIZE_sid_log $DATABASE_FREE_sid_log");
	        DATABASE_USED_sid=$(awk '{print $1+$2}' <<<"$DATABASE_USED_sid_log $DATABASE_USED_sid");
	        DATABASE_SIZE_sid=$(awk '{print $1+$2}' <<<"$DATABASE_SIZE_sid_log $DATABASE_SIZE_sid");
		DATABASE_FREE_sid=$(awk '{print $1-$2}' <<<"$DATABASE_SIZE_sid $DATABASE_USED_sid");
	    fi


	    DATABASE_SIZE_master=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 5 { print \$2 } ' ")
	    DATABASE_USED_master=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 5 { print \$3 } ' ")
	    DATABASE_FREE_master=$(awk '{print $1-$2}' <<<"$DATABASE_SIZE_master $DATABASE_USED_master");


	    DATABASE_SIZE_model=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 6 { print \$2 } ' ")
	    DATABASE_USED_model=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 6 { print \$3 } ' ")
	    DATABASE_FREE_model=$(awk '{print $1-$2}' <<<"$DATABASE_SIZE_model $DATABASE_USED_model");

	    DATABASE_SIZE_saptools_log=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 7 { print \$5 } ' ")

	    if [ "$DATABASE_SIZE_saptools_log" == "NULL" ];then
	        DATABASE_SIZE_saptools=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 7 { print \$2 } ' ")
	        DATABASE_USED_saptools=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 7 { print \$3 } ' ")
	        DATABASE_FREE_saptools=$(awk '{print $1-$2}' <<<"$DATABASE_SIZE_saptools $DATABASE_USED_saptools");
	    else
	        DATABASE_SIZE_saptools=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 7 { print \$2 } ' ")
	        DATABASE_USED_saptools=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 7 { print \$3 } ' ")
	        DATABASE_FREE_saptools_log=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 7 { print \$6 } ' ")
	        DATABASE_USED_saptools_log=$(awk '{print $1-$2}' <<<"$DATABASE_SIZE_saptools_log $DATABASE_FREE_saptools_log");
	        DATABASE_USED_saptools=$(awk '{print $1+$2}' <<<"$DATABASE_USED_saptools_log $DATABASE_USED_saptools");
	        DATABASE_SIZE_saptools=$(awk '{print $1+$2}' <<<"$DATABASE_SIZE_saptools_log $DATABASE_SIZE_saptools");
	        DATABASE_FREE_saptools=$(awk '{print $1-$2}' <<<"$DATABASE_SIZE_saptools $DATABASE_USED_saptools");

	    fi

	    DATABASE_SIZE_sybmgmtdb=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 8 { print \$2 } ' ")
	    DATABASE_USED_sybmgmtdb=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 8 { print \$3 } ' ")
	    DATABASE_FREE_sybmgmtdb=$(awk '{print $1-$2}' <<<"$DATABASE_SIZE_sybmgmtdb $DATABASE_USED_sybmgmtdb");


	    DATABASE_SIZE_sybsystemdb=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 9 { print \$2 } ' ")
	    DATABASE_USED_sybsystemdb=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 9 { print \$3 } ' ")
	    DATABASE_FREE_sybsystemdb=$(awk '{print $1-$2}' <<<"$DATABASE_SIZE_sybsystemdb $DATABASE_USED_sybsystemdb");


	    DATABASE_SIZE_sybsystemprocs=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 10 { print \$2 } ' ")
	    DATABASE_USED_sybsystemprocs=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid | awk ' FNR == 10 { print \$3 } ' ")
	    DATABASE_FREE_sybsystemprocs=$(awk '{print $1-$2}' <<<"$DATABASE_SIZE_sybsystemprocs $DATABASE_USED_sybsystemprocs");
	

	    DATABASE_SIZE_sid=$(awk '{print $1*1000}' <<<"$DATABASE_SIZE_sid");
	    DATABASE_SIZE_master=$(awk '{print $1*1000}' <<<"$DATABASE_SIZE_master");
	    DATABASE_SIZE_model=$(awk '{print $1*1000}' <<<"$DATABASE_SIZE_model");
	    DATABASE_SIZE_saptools=$(awk '{print $1*1000}' <<<"$DATABASE_SIZE_saptools");
	    DATABASE_SIZE_sybmgmtdb=$(awk '{print $1*1000}' <<<"$DATABASE_SIZE_sybmgmtdb");
	    DATABASE_SIZE_sybsystemdb=$(awk '{print $1*1000}' <<<"$DATABASE_SIZE_sybsystemdb");
	    DATABASE_SIZE_sybsystemprocs=$(awk '{print $1*1000}' <<<"$DATABASE_SIZE_sybsystemprocs");
	    DATABASE_FREE_sid=$(awk '{print $1*1000}' <<<"$DATABASE_FREE_sid");
	    DATABASE_FREE_master=$(awk '{print $1*1000}' <<<"$DATABASE_FREE_master");
	    DATABASE_FREE_model=$(awk '{print $1*1000}' <<<"$DATABASE_FREE_model");
	    DATABASE_FREE_saptools=$(awk '{print $1*1000}' <<<"$DATABASE_FREE_saptools");
	    DATABASE_FREE_sybmgmtdb=$(awk '{print $1*1000}' <<<"$DATABASE_FREE_sybmgmtdb");
	    DATABASE_FREE_sybsystemdb=$(awk '{print $1*1000}' <<<"$DATABASE_FREE_sybsystemdb");
	    DATABASE_FREE_sybsystemprocs=$(awk '{print $1*1000}' <<<"$DATABASE_FREE_sybsystemprocs");
	    DATABASE_USED_sid=$(awk '{print $1*1000}' <<<"$DATABASE_USED_sid");
	    DATABASE_USED_master=$(awk '{print $1*1000}' <<<"$DATABASE_USED_master");
	    DATABASE_USED_model=$(awk '{print $1*1000}' <<<"$DATABASE_USED_model");
	    DATABASE_USED_saptools=$(awk '{print $1*1000}' <<<"$DATABASE_USED_saptools");
	    DATABASE_USED_sybmgmtdb=$(awk '{print $1*1000}' <<<"$DATABASE_USED_sybmgmtdb");
	    DATABASE_USED_sybsystemdb=$(awk '{print $1*1000}' <<<"$DATABASE_USED_sybsystemdb");
	    DATABASE_USED_sybsystemprocs=$(awk '{print $1*1000}' <<<"$DATABASE_USED_sybsystemprocs");

	    DATA_ALL=$(echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " cat $RUTE/output_file_sid ")
	    echo "Data Original"
	    echo "$DATA_ALL"
	    echo
	    echo "DATA YA TRADUCIDA: "
	    echo
	    echo "SIZE $sid : $DATABASE_SIZE_sid  USED : $DATABASE_USED_sid FREE: $DATABASE_FREE_sid"
	    echo "SIZE master : $DATABASE_SIZE_master  USED : $DATABASE_USED_master FREE: $DATABASE_FREE_master"
	    echo "SIZE model : $DATABASE_SIZE_model   USED : $DATABASE_USED_model FREE: $DATABASE_FREE_model"
	    echo "SIZE saptools : $DATABASE_SIZE_saptools  USED : $DATABASE_USED_saptools FREE: $DATABASE_FREE_saptools"
	    echo "SIZE sybmgmtdb : $DATABASE_SIZE_sybmgmtdb  USED : $DATABASE_USED_sybmgmtdb FREE: $DATABASE_FREE_sybmgmtdb"
	    echo "SIZE sybsystemdb : $DATABASE_SIZE_sybsystemdb  USED : $DATABASE_USED_sybsystemdb FREE: $DATABASE_FREE_sybsystemdb"
	    echo "SIZE sybsystemprocs : $DATABASE_SIZE_sybsystemprocs  USED : $DATABASE_USED_sybsystemprocs FREE: $DATABASE_FREE_sybsystemprocs"

	    echo $line | SSHPASS=$pass_unix sshpass -e $pass ssh -o "StrictHostKeyChecking no" $user_unix@$ip " rm -f $RUTE/output_file_sid $RUTE/codes.isql ";
	    echo $line | echo $cliente","$typedb","$FECHA","$sid","$descripcion","$sid","$DATABASE_SIZE_sid","$DATABASE_FREE_sid","$DATABASE_USED_sid > /home/coecogni/espacios/todos_sybase
	    echo $line | echo $cliente","$typedb","$FECHA","$sid","$descripcion","MASTER","$DATABASE_SIZE_master","$DATABASE_FREE_master","$DATABASE_USED_master >> /home/coecogni/espacios/todos_sybase
	    echo $line | echo $cliente","$typedb","$FECHA","$sid","$descripcion","MODEL","$DATABASE_SIZE_model","$DATABASE_FREE_model","$DATABASE_USED_model >> /home/coecogni/espacios/todos_sybase
	    echo $line | echo $cliente","$typedb","$FECHA","$sid","$descripcion","SAPTOOLS","$DATABASE_SIZE_saptools","$DATABASE_FREE_saptools","$DATABASE_USED_saptools >> /home/coecogni/espacios/todos_sybase
	    echo $line | echo $cliente","$typedb","$FECHA","$sid","$descripcion","SYBMGMTDB","$DATABASE_SIZE_sybmgmtdb","$DATABASE_FREE_sybmgmtdb","$DATABASE_USED_sybmgmtdb >> /home/coecogni/espacios/todos_sybase
	    echo $line | echo $cliente","$typedb","$FECHA","$sid","$descripcion","SYBSYSTEMDB","$DATABASE_SIZE_sybsystemdb","$DATABASE_FREE_sybsystemdb","$DATABASE_USED_sybsystemdb >> /home/coecogni/espacios/todos_sybase
	    echo $line | echo $cliente","$typedb","$FECHA","$sid","$descripcion","SYBSYSTEMPROCS","$DATABASE_SIZE_sybsystemprocs","$DATABASE_FREE_sybsystemprocs","$DATABASE_USED_sybsystemprocs >> /home/coecogni/espacios/todos_sybase

	cero="0"

        	if (( $(awk 'BEGIN {print ("'$DATABASE_SIZE_sid'" <= "'$cero'")}') )) || (( $(awk 'BEGIN {print ("'$DATABASE_SIZE_master'" <= "'$cero'")}') )) || (( $(awk 'BEGIN {print ("'$DATABASE_SIZE_model'" <= "'$cero'")}') )) || (( $(awk 'BEGIN {print ("'$DATABASE_SIZE_saptools'" <= "'$cero'")}') )) || (( $(awk 'BEGIN {print ("'$DATABASE_SIZE_sybmgmtdb'" <= "'$cero'")}') )) || (( $(awk 'BEGIN {print ("'$DATABASE_SIZE_sybsystemdb'" <= "'$cero'")}') )) || (( $(awk 'BEGIN {print ("'$DATABASE_SIZE_sybsystemprocs'" <= "'$cero'")}') )); then

                	echo "ERRORES DE LECTURA EN LA BASE DE DATOS SYBASE DE \"$cliente\" EN EL SISTEMA \"$descripcion\" CON SID \"$sid\""
	        else

/usr/bin/mysql --user=espacios --password=ibmsap2014 <<!
use espacios
load data local infile '/home/coecogni/espacios/todos_sybase' into table espacios_stats
FIELDS TERMINATED BY ','
( CLIENTE, TIPO_DB, FECHA , SID, DESCRIPCION, TABLESPACE, TAM_KBYTES, LIBRE_KBYTES, OCUPADO_KBYTES, MAX_BLOQUE_LIBRE, CREC_OCUPADO_DIARIO_KBYTES, EXTENTS, CREC_DIARIO_EXTENTS, MAX_CRECI_ULTIMOS_DIAS)
set FECHA = "$FECHA";
quit
!

	        fi
    fi
done < $ini

rm -f /home/coecogni/espacios/todos.sybase /home/coecogni/espacios/todos_sybase
