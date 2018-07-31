#!/bin/bash

ip=$1
user=$2
pass=$3
cliente=$4
typedb=$5
sid=$6
descripcion=$7

export FECHA=`/bin/date +%Y-%m-%d`
FECHA="$FECHA 13:30:40"

. /home/coecogni/espacios/recolect_data.sh $ip $user $pass | tee outt.log

type_mode=$(cat outt.log | egrep '0 reservado|activo|agrup' | wc -l)

if [ $type_mode -eq 1 ];then

data_space_available=$(cat outt.log | sed -n 's/.*% ASP sistema utilizado://p')
cien="100"
data_space_available=$(awk '{print $1/$2}' <<<"$data_space_available $cien")
data_space_total=$(cat outt.log | sed -n 's/.*ASP del sistema  . . . ://p')

echo "$data_space_total" > data.log
type_data=$(cat data.log | awk ' { print $2 } ' | tr -d $'\r')
data_space_total=$(cat data.log | awk ' { print $1 } ' | tr -d $'\r')

if [ "$type_data" == "G" ];then
millon="1000000"
data_space_total=$(awk '{print $1*$2}' <<<"$data_space_total $millon")
fi

if [ "$type_data" == "M" ];then
mil="1000"
data_space_total=$(awk '{print $1*$2}' <<<"$data_space_total $mil")
fi

data_space_used=$(awk '{print $1*$2}' <<<"$data_space_available $data_space_total")
data_space_free=$(awk '{print $1-$2}' <<<"$data_space_total $data_space_used")

else

data_space_available=$(cat outt.log | sed -n 's/.*System storage used  . . . . . . . . . . . . . . . . . . ://p')
cien="100"
data_space_available=$(awk '{print $1/$2}' <<<"$data_space_available $cien")
data_space_total=$(cat outt.log | sed -n 's/.*System storage (in 1,000,000 bytes)  . . . . . . . . . . ://p')

pormil="1000"
data_space_total=$(awk '{print $1*$2}' <<<"$data_space_total $pormil")
data_space_used=$(awk '{print $1*$2}' <<<"$data_space_available $data_space_total")
data_space_free=$(awk '{print $1-$2}' <<<"$data_space_total $data_space_used")

fi

rm -f data.log outt.log

echo $cliente","$typedb","$FECHA","$sid","$descripcion","DATABASE SYSTEM","$data_space_total","$data_space_free","$data_space_used > /home/coecogni/espacios/todos_as400

if [ "$data_space_total" == "0" ] && [ "$data_space_used" == "0" ] && [ "$data_space_free" == "0" ];then

echo "Error de lectura en los datos, revisar"

else

/usr/bin/mysql --user=espacios --password=ibmsap2014 <<!
use espacios
load data local infile '/home/coecogni/espacios/todos_as400' into table espacios_test
FIELDS TERMINATED BY ','
( CLIENTE, TIPO_DB, FECHA , SID, DESCRIPCION, TABLESPACE, TAM_KBYTES, LIBRE_KBYTES, OCUPADO_KBYTES, MAX_BLOQUE_LIBRE, CREC_OCUPADO_DIARIO_KBYTES, EXTENTS, CREC_DIARIO_EXTENTS, MAX_CRECI_ULTIMOS_DIAS)
set FECHA = "$FECHA";
quit
!

fi

rm -f todos_as400
echo -e \\033c
