###  AUTORES: ORLANDO CORREA y DAVID BURBANO
##   FECHA: 08-05-2018

import json,collections
import mysql.connector #Driver for MySQL
from mysql.connector import errorcode #Error management
import cx_Oracle  #Driver for Oracle
import ibm_db #Driver for DB2
from threading import Thread
import datetime
from datetime import datetime as dt
import sys
import traceback
import time
import requests
import json
import os
from operator import itemgetter
from statistics import mean
from datetime import timedelta
import threading

# DECLARACION DE VARIABLES #
list_name1_client,list_name1_tablespace,list_name1_descripcion,list_tablespace_freespace,list_name1_ip,list_name1_hostname,list_name1_user,list_name1_typedb,list_name1_alias,list_name1_password,list_name1_sid,list_name1_ocupado,list_name1_total=[],[],[],[],[],[],[],[],[],[],[],[],[]
count,promedio,inserts,used1,used1_1,used2, used2_1, used3, used3_1, used4, used4_1, used5, deltaused1, deltaused2, deltaused3,deltaused4, clientes= 0,0,[],0,0,0,0,0,0,0,0,0,0,0,0,0,''
count2,count3,promedio_delta_used,bandera1, bandera2, bandera3, bandera4,bandera5, bandera1_1, bandera2_1, bandera3_1,bandera4_1,typedb=0,0,0,0,0,0,0,0,0,0,0,0,''
list_name_client,tablespace_ready_used,cliente_ready_used,descripcion_ready_used=[],[],[],[]
list_tablespace_freespace,cliente_ready_used_null,descripcion_ready_used_null,tablespace_ready_used_null=[],[],[],[]
list_complete_tablespace,tamaño_ready,tipo_db_ready,ocupado_ready=[],[],[],[]
list_time_for_fullspace,list_name_sid,list_name_ip,list_name_hostname,list_name_user,list_name_pass,list_name_alias=[],[],[],[],[],[],[]
list_promedio,list_promedio_final,list_name_tablespace,list_name_descripcion,list_max_delta,list_time_for_fullspace_null,cliente_ready,descripcion_ready,tablespace_ready,libre_ready,list_tablespace_readys,list_time_for_fullspace_complete,list_IP_2,list_HOSTNAME_2,list_USER_2,list_CLAVE_2,list_ALIAS_2=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
promedio_final_delta,promedio_delta_used=0,0
max_delta=0.0
time_for_fullspace=0.0
time_for_fullspace_negativo,cliente_ready_used_negativo,descripcion_ready_used_negativo,tablespace_ready_used_negativo,list_time_for_fullspace_negativo=0.0,[],[],[],[]
new_delta,time_last_date,bandera_delta_sum=0,0,0

# IMPORTANDO LA FECHA ACTUAL
d = datetime.date.today()  # Today
t = dt.now()   # Now
time_i=time.strftime('%Y-%m-%d') +' '+ '13:30:40';
todayok=dt.now().strftime('%Y-%m-%d %H:%M:%S')
list_connection_fail=[]
bandera_delta_min=0

def connect_db2():
        for (dbtype, customer, dbname, dbuser, dbpass, dbalias, sid, hostname, dbport, usertunn, hostunn, portunn, umbralert,ip) in data_sql_db2:
                print(dbtype,customer,dbalias,ip)
                if customer[:1]!='#':
                        try:
                # Create connection to remote DB2
                                con = ibm_db.connect("DATABASE="+sid+";HOSTNAME="+hostname+";PROTOCOL=TCPIP;UID="+dbuser+";PWD="+dbpass+";PORT="+dbport,"","")
                        except:
                # Connection error handling
                                data_error=traceback.format_exc().splitlines()
                                list_connection_fail.append({"CLIENTE":customer,"ALIAS":dbalias,"SID":sid,"ERROR":str(data_error[-1])})
                # TODO make error handling for connection
                        else:
                                try:
                        # Execute query to get space
                                        stmt = ibm_db.exec_immediate(con, "select DB_STORAGE_PATH,FS_TOTAL_SIZE,STO_PATH_FREE_SIZE,FS_USED_SIZE from sysibmadm.SNAPSTORAGE_PATHS")
                                except:
                        # Query error handling
                                        data_error=traceback.format_exc().splitlines()
                                        list_connection_fail.append({"CLIENTE":customer,"ALIAS":dbalias,"SID":sid,"ERROR":str(data_error[-1])})
                        # TODO make error handling for query
                                else:
                        # Fetch first result
                                        result = ibm_db.fetch_tuple(stmt)
                                        inserts = []
                                        while (result):
                                # TODO whatever needed with the result
                                                inserts.append("('"+customer+"','"+dbtype+"','"+time_i+"','"+sid+"','"+dbname+"','"+str(result[0])+"',"+str(float(result[1])/1000.0)+","+str(float(result[2])/1000.0)+","+str(float(result[3])/1000.0)+",0,0,0,0,0)")
                                                result = ibm_db.fetch_tuple(stmt)

                                        stm = "INSERT INTO espacios_stats values " + ','.join(inserts) + ";"
                                        cur_sql_db2.execute(stm)
                                        cnx_1.commit()
        return

def connect_oracle():
        for (dbtype, customer, dbname, dbuser, dbpass, dbalias, sid, hostname, dbport, usertunn, hostunn, portunn, umbralert,ip) in data_sql_ora:
                print(dbtype,customer,dbalias,ip)
                try:
                        if customer[:1]!='#':
                                inserts=[];
                                if portunn[:1]=='1':
                                        a=os.system('sh /home/coecogni/espacios/tunnel.sh'+' '+str(umbralert)+' '+portunn+' '+hostname+' '+dbport+' '+usertunn+' '+hostunn)
                                        dsn=cx_Oracle.makedsn(host="localhost", sid=sid, port=portunn)
                                else:
                                        dsn=cx_Oracle.makedsn(host=hostname, sid=sid, port=dbport)
                                con=cx_Oracle.connect(user=dbuser, password=dbpass, dsn=dsn)
                                cur=con.cursor()
                                sql=open('/home/coecogni/espacios/trae_data_limpio_finally.sql',"r")
                                data=sql.read();
                                cur_out=cur.var(cx_Oracle.STRING);
                                cur.execute(data,cur_out=cur_out)
                                data_out=cur_out.getvalue();
                                data_split=data_out.split('|')
                                data_split2 = [x for x in data_split if x]
                                for i in data_split2:
                                        data_split3=i.split(',')
                                        c_tablespace=data_split3[0]
                                        c_tamaño=data_split3[1]
                                        c_libre=data_split3[2]
                                        c_ocupado=data_split3[3]
                                        c_maxbloqlibre=data_split3[4]
                                        c_crecidia=data_split3[5]
                                        c_extends=data_split3[6]
                                        c_crecidiaext=data_split3[7]
                                        c_creciultimosdia=data_split3[8]
                                        sql = "INSERT INTO espacios_stats (CLIENTE,TIPO_DB,FECHA,SID,DESCRIPCION,TABLESPACE,TAM_KBYTES,LIBRE_KBYTES,OCUPADO_KBYTES,MAX_BLOQUE_LIBRE,CREC_OCUPADO_DIARIO_KBYTES,EXTENTS,CREC_DIARIO_EXTENTS,MAX_CRECI_ULTIMOS_DIAS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                        cur_sql_ora.execute(sql,(customer,dbtype,time_i,sid,dbname,c_tablespace,c_tamaño,c_libre,c_ocupado,c_maxbloqlibre,c_crecidia,c_extends,c_crecidiaext,c_creciultimosdia))
                                        cnx_1.commit()
                                cur.close()
                                con.close()
                except:
                        data_error=traceback.format_exc().splitlines()
                        list_connection_fail.append({"CLIENTE":customer,"ALIAS":dbalias,"SID":sid,"ERROR":str(data_error[-1])})
        return

def connect_sybase():
        for (dbtype, customer, dbname, dbuser, dbpass, dbalias, sid, hostname, dbport, usertunn, hostunn, portunn, umbralert,ip) in data_sql_syb:
                if customer[:1]!='#':
                        with open("/home/coecogni/espacios/todos.sybase","w") as sybase:
                                sybase.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (dbtype,customer,dbname,dbuser,dbpass,dbalias,sid,hostname,ip,usertunn,umbralert,portunn))
                        try:
                                syb=os.system('sh /home/coecogni/espacios/readSybaseDB.sh')
                        except:
                                data_error=traceback.format_exc().splitlines()
                                list_connection_fail.append({"CLIENTE":customer,"ALIAS":dbalias,"SID":sid,"ERROR":str(data_error[-1])})
        return

t1 = time.time();
cnx_1=mysql.connector.connect(user='espacios', password='ibmsap2014', database='espacios');
cur_sql_ora=cnx_1.cursor(buffered=True);
cur_sql_syb=cnx_1.cursor(buffered=True);
cur_sql_db2=cnx_1.cursor(buffered=True);
cur_sql_ora.execute ("select dbtype, customer, dbname, dbuser, dbpass, dbalias, sid, hostname, dbport, usertunn, hostunn, portunn, umbralert,ip from espacios_ini where dbtype='ORA' and customer <> 'SURAMERICANA'");
cur_sql_syb.execute ("select dbtype, customer, dbname, dbuser, dbpass, dbalias, sid, hostname, dbport, usertunn, hostunn, portunn, umbralert,ip from espacios_ini where dbtype='SYB'");
cur_sql_db2.execute ("select dbtype, customer, dbname, dbuser, dbpass, dbalias, sid, hostname, dbport, usertunn, hostunn, portunn, umbralert,ip from espacios_ini where dbtype='DB2'");
data_sql_ora = cur_sql_ora.fetchall ()
data_sql_syb = cur_sql_syb.fetchall ()
data_sql_db2 = cur_sql_db2.fetchall ()
data_sql_ora.sort();
data_sql_syb.sort();
data_sql_db2.sort();

try:
        connect_oracle();
        connect_db2();
        connect_sybase();

except:
        data_error=traceback.format_exc().splitlines()
        list_connection_fail.append({"ERROR":str(data_error[-1])})


for errores in range(len(list_connection_fail)):
        print(list_connection_fail[errores])


# Headers for request get and post
proxies = {
  'http': 'http://129.39.183.196:8080',
  'https': 'http://129.39.183.196:8080'
}
headers = {'content-type': 'application/json'}
r=requests.post("https://watson-advisor.mybluemix.net/slack/spaces",data=json.dumps(list_connection_fail),headers=headers,proxies=proxies)
cur_sql_ora.close()
cur_sql_syb.close()
cur_sql_db2.close()
cnx_1.close()

# CREACION DELTA DE DIAS
onelastday= d - timedelta(days=1)
twolastday= d - timedelta(days=2)
threelastday= d - timedelta(days=3)
fourlastday= d - timedelta(days=4)
onelastday= onelastday.strftime('%Y-%m-%d') +' '+ '13:30:40';
threelastday= threelastday.strftime('%Y-%m-%d') +' '+ '13:30:40';
twolastday= twolastday.strftime('%Y-%m-%d') +' '+ '13:30:40';
fourlastday= fourlastday.strftime('%Y-%m-%d') +' '+ '13:30:40';
today= d.strftime('%Y-%m-%d') +' '+ '13:30:40'

###### LOGICA DE EXTRACION DE ESPACIOS, SIENDO FILTRADAS POR LOS PARAMETROS CLIENTE-DESCRIPCION-TABLESPACE-FECHA----ASEGURANDO ASI LOS DATOS CORRECTOS ############

cnx=mysql.connector.connect(user='espacios', password='ibmsap2014', database='espacios');
cur_sql=cnx.cursor();
query=("select CLIENTE, TIPO_DB, DESCRIPCION, SID, TABLESPACE, OCUPADO_KBYTES,LIBRE_KBYTES,FECHA,TAM_KBYTES from espacios_stats where FECHA between  %s and %s ");
cur_sql.execute(query,(fourlastday,today));
data_sql = cur_sql.fetchall ()
data_sql.sort(key = itemgetter(7))
data_sql.sort(key = itemgetter(4))
data_sql.sort(key = itemgetter(2))
data_sql.sort(key = itemgetter(0))
query_delete=("DELETE FROM tablespace_by_client_copy")
cur3_delete=cnx.cursor()
cur3_delete.execute(query_delete)
cur4_data_today=cnx.cursor()
query_data_today=("select CLIENTE, TIPO_DB, DESCRIPCION, SID, TABLESPACE, OCUPADO_KBYTES,LIBRE_KBYTES,FECHA,TAM_KBYTES from espacios_stats where FECHA between  %s and %s ");
cur4_data_today.execute(query_data_today,(today,today))
data_today=cur4_data_today.fetchall ()

cur_sql_f=cnx.cursor();
cur_sql_f.execute ("select dbtype, customer, dbname, dbuser, dbpass, dbalias, sid, hostname,ip from espacios_ini");
data_sql_f = cur_sql_f.fetchall ()
data_sql_f.sort();
list_IP,list_HOSTNAME,list_USER,list_CLAVE,list_ALIAS=[],[],[],[],[]
count_f=-1

# ACTUALIZACION TABLA DE LOS CLIENTES LEIDOS EL DIA DE HOY
for (CLIENTE, TIPO_DB, DESCRIPCION, SID, TABLESPACE,OCUPADO_KBYTES,LIBRE_KBYTES,FECHA,TAM_KBYTES) in data_today:
        for(dbtype, customer, dbname, dbuser, dbpass, dbalias, sid, hostname, ip) in data_sql_f:
                if CLIENTE==customer:
                        if DESCRIPCION==dbname:
                                count_f=count_f+1
                                list_IP.append(ip)
                                list_HOSTNAME.append(hostname)
                                list_USER.append(dbuser)
                                list_CLAVE.append(dbpass)
                                list_ALIAS.append(dbalias)
                                sql = "INSERT INTO tablespace_by_client_copy (CLIENTE,TIPO_DB,SID,TABLESPACE,DESCRIPCION,ALIAS,HOSTNAME,IP,OCUPADO_KBYTES,LIBRE_KBYTES,TAMAÑO_KBYTES,USER,PASSWORD) VALUES (%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"
                                cur_sql.execute(sql,(CLIENTE,TIPO_DB,SID,TABLESPACE,DESCRIPCION,list_ALIAS[count_f],list_HOSTNAME[count_f],list_IP[count_f],OCUPADO_KBYTES,LIBRE_KBYTES,TAM_KBYTES,list_USER[count_f],list_CLAVE[count_f]))
                                cnx.commit()
count_f_2=-1
count_f=-1
cur2_sql=cnx.cursor();
query2=("select CLIENTE,TIPO_DB,SID,TABLESPACE,DESCRIPCION,ALIAS,HOSTNAME,IP, OCUPADO_KBYTES,LIBRE_KBYTES,TAMAÑO_KBYTES,USER,PASSWORD from tablespace_by_client_copy");
cur2_sql.execute(query2)
data2_sql= cur2_sql.fetchall ()

# FILTRO Y SEPARACION DE CLIENTES CON SUS RESPECTIVOS TABLESPACES, QUE SON LOS QUE SE VAN ANALIZAR:
for (CLIENTE,TIPO_DB,SID,TABLESPACE,DESCRIPCION,ALIAS,HOSTNAME,IP,OCUPADO_KBYTES,LIBRE_KBYTES,TAMAÑO_KBYTES,USER,PASSWORD) in data2_sql:
        list_complete_tablespace.append(CLIENTE+"|"+DESCRIPCION+"|"+TIPO_DB+"|"+TABLESPACE+"|"+str(OCUPADO_KBYTES)+"|"+str(LIBRE_KBYTES)+"|"+str(TAMAÑO_KBYTES)+"|"+ALIAS+"|"+HOSTNAME+"|"+IP+"|"+USER+"|"+PASSWORD+"|"+SID)
for k in (list_complete_tablespace):
        list_split=k.split('|')
        list_name1_client.append(list_split[0])
        list_name1_tablespace.append(list_split[3])
        list_name1_descripcion.append(list_split[1])
        list_tablespace_freespace.append(float(list_split[5]))
        list_name1_ip.append(list_split[9])
        list_name1_hostname.append(list_split[8])
        list_name1_user.append(list_split[10])
        list_name1_typedb.append(list_split[2])
        list_name1_alias.append(list_split[7])
        list_name1_password.append(list_split[11])
        list_name1_sid.append(list_split[12])
        list_name1_ocupado.append(list_split[4])
        list_name1_total.append(list_split[6])
# BUSQUEDA DE REGISTROS EN EL BACKUP DE DATOS Y CALCULO DE PROMEDIOS DE USO, TOMANDO COMO REFERENCIA LOS TABLESPACES LEIDOS EL DIA DE HOY:

for j in range(len(list_name1_client)):
        for (CLIENTE, TIPO_DB, DESCRIPCION, SID, TABLESPACE,OCUPADO_KBYTES,LIBRE_KBYTES,FECHA,TAM_KBYTES) in data_sql:
                if CLIENTE==list_name1_client[j]:
                        if DESCRIPCION==list_name1_descripcion[j]:
                                if TABLESPACE==list_name1_tablespace[j]:
                                        promedio=promedio+OCUPADO_KBYTES
                                        count=count+1
                                        if str(FECHA)==str(today):
                                                used1=OCUPADO_KBYTES
                                                bandera1=1
                                        if str(FECHA)==str(onelastday):
                                                used2=OCUPADO_KBYTES
                                                bandera2=1
                                        if str(FECHA)==str(twolastday):
                                                used3=OCUPADO_KBYTES
                                                bandera3=1
                                        if str(FECHA)==str(threelastday):
                                                used4=OCUPADO_KBYTES
                                                bandera4=1
                                        if str(FECHA)==str(fourlastday):
                                                used5=OCUPADO_KBYTES
                                                bandera5=1
                                        if (bandera1==1 and bandera2==1):
                                                deltaused1=used1-used2
                                                bandera1_1=1
                                        if (bandera2==1 and bandera3==1):
                                                deltaused2=used2-used3
                                                bandera2_1=1
                                        if (bandera3==1 and bandera4==1):
                                                deltaused3=used3-used4
                                                bandera3_1=1
                                        if (bandera4==1 and bandera5==1):
                                                deltaused4=used4-used5
                                                bandera4_1=1
                                        if (bandera1_1==1 and bandera2_1==1 and bandera3_1==1 and bandera4_1==1):
                                                promedio_delta_used=(deltaused1+deltaused2+deltaused3+deltaused4)
                                                promedio_final_delta=promedio_delta_used/4
                                                list_promedio_final.append(list_name1_client[j]+"|"+list_name1_descripcion[j]+"|"+list_name1_tablespace[j]+"|"+str(promedio_final_delta))
                                                max_delta=max(deltaused1,deltaused2,deltaused3,deltaused4)
                                                list_max_delta.append(float(max_delta))
                                                for(dbtype, customer, dbname, dbuser, dbpass, dbalias, sid, hostname, ip) in data_sql_f:
                                                        if CLIENTE==customer:
                                                                if DESCRIPCION==dbname:
                                                                        list_tablespace_readys.append(CLIENTE+"|"+DESCRIPCION+"|"+TIPO_DB+"|"+TABLESPACE+"|"+str(OCUPADO_KBYTES)+"|"+str(LIBRE_KBYTES)+"|"+str(TAM_KBYTES)+"|"+dbalias+"|"+hostname+"|"+ip+"|"+dbuser+"|"+dbpass+"|"+SID)
        bandera_delta_sum=bandera1_1+bandera2_1+bandera3_1+bandera4_1
        new_delta=deltaused1+deltaused2+deltaused3+deltaused4
        if (bandera_delta_sum > 0 and bandera_delta_sum != 4):
                new_delta=new_delta/bandera_delta_sum
                if new_delta<0:
                        time_last_date=float(list_tablespace_freespace[j]*-1)/new_delta
                if new_delta==0:
                        time_last_date=9999
                if new_delta>0:
                        time_last_date=float(list_tablespace_freespace[j])/new_delta
                list_time_for_fullspace_complete.append(list_name1_client[j]+"|"+list_name1_typedb[j]+"|"+list_name1_descripcion[j]+"|"+list_name1_alias[j]+"|"+list_name1_sid[j]+"|"+list_name1_tablespace[j]+"|"+list_name1_hostname[j]+"|"+list_name1_ip[j]+"|"+str(list_name1_total[j])+"|"+str(list_name1_ocupado[j])+"|"+str(list_tablespace_freespace[j])+"|"+list_name1_user[j]+"|"+list_name1_password[j]+"|"+str(time_last_date))
                cur_update_lastdate_espacios=cnx.cursor()
                query_update_lastdate_espacios=("update espacios_stats set MAX_CRECI_ULTIMOS_DIAS = %s where CLIENTE = '%s' and DESCRIPCION='%s' and TABLESPACE='%s' and FECHA='%s'" % (time_last_date,list_name1_client[j],list_name1_descripcion[j],list_name1_tablespace[j],today))
                cur_update_lastdate_espacios.execute(query_update_lastdate_espacios)
                cnx.commit()
        if count!=0:
                promedio=promedio/count
                list_promedio.append(list_name1_client[j]+"|"+list_name1_descripcion[j]+"|"+list_name1_tablespace[j]+"|"+str(promedio))
        count=0
        promedio=0
        promedio_final_delta=0
        bandera1,bandera2,bandera3,bandera4,bandera5,bandera1_1,bandera2_1,bandera3_1,bandera4_1=0,0,0,0,0,0,0,0,0
        deltaused1,deltaused2,deltaused3,deltaused4=0,0,0,0
        bandera_delta_sum,new_delta,time_last_date=0,0,0
        count_f_2=-1
# CALCULO PARA ESTIMAR TIEMPO DE LLENADO DE ESPACIO DEL RESPECTIVO TABLESPACE
for a in list_tablespace_readys:
        split=a.split("|")
        cliente_ready.append(split[0])
        descripcion_ready.append(split[1])
        tablespace_ready.append(split[3])
        libre_ready.append(float(split[5]))
        tamaño_ready.append(float(split[6]))
        ocupado_ready.append(float(split[4]))
        tipo_db_ready.append(split[2])
        list_name_sid.append(split[12])
        list_name_user.append(split[10])
        list_name_pass.append(split[11])
        list_name_hostname.append(split[8])
        list_name_alias.append(split[7])
        list_name_ip.append(split[9])

for q in range(len(cliente_ready)):
        if list_max_delta[q]==0:
                cliente_ready_used_null.append(cliente_ready[q])
                descripcion_ready_used_null.append(descripcion_ready[q])
                tablespace_ready_used_null.append(tablespace_ready[q])
                list_time_for_fullspace_null.append("NULL")
                list_time_for_fullspace_complete.append(cliente_ready[q]+"|"+tipo_db_ready[q]+"|"+descripcion_ready[q]+"|"+list_name_alias[q]+"|"+list_name_sid[q]+"|"+tablespace_ready[q]+"|"+list_name_hostname[q]+"|"+list_name_ip[q]+"|"+str(tamaño_ready[q])+"|"+str(ocupado_ready[q])+"|"+str(libre_ready[q])+"|"+list_name_user[q]+"|"+list_name_pass[q]+"|"+"9999.0")
        if (list_max_delta[q]>0):
                cliente_ready_used.append(cliente_ready[q])
                descripcion_ready_used.append(descripcion_ready[q])
                tablespace_ready_used.append(tablespace_ready[q])
                time_for_fullspace=float(libre_ready[q]/list_max_delta[q])
                list_time_for_fullspace.append(time_for_fullspace)
                list_time_for_fullspace_complete.append(cliente_ready[q]+"|"+tipo_db_ready[q]+"|"+descripcion_ready[q]+"|"+list_name_alias[q]+"|"+list_name_sid[q]+"|"+tablespace_ready[q]+"|"+list_name_hostname[q]+"|"+list_name_ip[q]+"|"+str(tamaño_ready[q])+"|"+str(ocupado_ready[q])+"|"+str(libre_ready[q])+"|"+list_name_user[q]+"|"+list_name_pass[q]+"|"+str(time_for_fullspace))
        if (list_max_delta[q]<0):
                cliente_ready_used_negativo.append(cliente_ready[q])
                descripcion_ready_used_negativo.append(descripcion_ready[q])
                tablespace_ready_used_negativo.append(tablespace_ready[q])
                time_for_fullspace_negativo=float(libre_ready[q]/(list_max_delta[q]*-1))
                list_time_for_fullspace_negativo.append(time_for_fullspace)
                list_time_for_fullspace_complete.append(cliente_ready[q]+"|"+tipo_db_ready[q]+"|"+descripcion_ready[q]+"|"+list_name_alias[q]+"|"+list_name_sid[q]+"|"+tablespace_ready[q]+"|"+list_name_hostname[q]+"|"+list_name_ip[q]+"|"+str(tamaño_ready[q])+"|"+str(ocupado_ready[q])+"|"+str(libre_ready[q])+"|"+list_name_user[q]+"|"+list_name_pass[q]+"|"+str(time_for_fullspace_negativo))

cur_update=cnx.cursor()

for q1 in range(len(list_time_for_fullspace)):
        query_update=("update espacios_stats set MAX_CRECI_ULTIMOS_DIAS = %s where CLIENTE = '%s' and DESCRIPCION='%s' and TABLESPACE='%s' and FECHA='%s'" % (list_time_for_fullspace[q1],cliente_ready_used[q1],descripcion_ready_used[q1],tablespace_ready_used[q1],today))
        cur_update.execute(query_update)
        cnx.commit()
for q2 in range(len(list_time_for_fullspace_null)):
        query_update=("update espacios_stats set MAX_CRECI_ULTIMOS_DIAS = %s where CLIENTE = '%s' and DESCRIPCION='%s' and TABLESPACE='%s' and FECHA='%s'" % ("9999",cliente_ready_used_null[q2],descripcion_ready_used_null[q2],tablespace_ready_used_null[q2],today))
        cur_update.execute(query_update)
        cnx.commit()
for q3 in range(len(list_time_for_fullspace_negativo)):
        query_update=("update espacios_stats set MAX_CRECI_ULTIMOS_DIAS = %s where CLIENTE = '%s' and DESCRIPCION='%s' and TABLESPACE='%s' and FECHA='%s'" % (list_time_for_fullspace_negativo[q3],cliente_ready_used_negativo[q3],descripcion_ready_used_negativo[q3],tablespace_ready_used_negativo[q3],today))
        cur_update.execute(query_update)
        cnx.commit()

cnx.close()

# IMPRESION DE RESULTADOS SEGUN SU CLIENTE Y SISTEMA
for n in sorted(list_time_for_fullspace_complete):
       print(n)

data_porcen=0.0
data_finally=[]
data_finally_alerts=[]

for k in list_time_for_fullspace_complete:
        data=k.split("|")
        if float(data[9])==0:
                data_porcent="NULL"
        if float(data[9])!=0:
                data_porcen=(float(data[9])*100)/(float(data[8]))
        data_finally.append({"cliente":data[0],"dbtype":data[1],"sid":data[4],"tablespace":data[5],"used":"{0:.4f}".format((float(data[9])/1000.0)),"free":"{0:.4f}".format((float(data[10])/1000.0)),"vida":str(int(float(data[13]))),"porcen":"{0:.2f}".format(float(data_porcen)),"hostname":data[6],"ip":data[7],"ambiente":data[2],"usuario":data[11],"clave":data[12],"dbname":data[3]})
        if (float(data[13]) < 6):
                data_finally_alerts.append({"cliente":data[0],"dbtype":data[1],"sid":data[4],"tablespace":data[5],"used":"{0:.4f}".format((float(data[9])/1000.0)),"free":"{0:.4f}".format((float(data[10])/1000.0)),"vida":str(int(float(data[13]))),"porcen":"{0:.2f}".format(float(data_porcen)),"hostname":data[6],"ip":data[7],"ambiente":data[2],"usuario":data[11],"clave":data[12],"dbname":data[3]})

x_1=0
y_1=0

with open('/home/coecogni/espacios/data_completa_clientes.json', 'w') as outfile:
        outfile.write("{\"fecha\": \""+str(todayok)+"\", \"data\" : [\n")
        for x in data_finally:
                x_1=x_1+1
                json.dump(x,outfile)
                if x_1<(len(data_finally)):
                        outfile.write(",\n")
                if x_1==len(data_finally):
                        outfile.write("\n")
        outfile.write("]}")
        x_1=0

with open('/home/coecogni/espacios/data_completa_clientes_alerts.json', 'w') as outfile:
        outfile.write("{\"fecha\": \""+str(todayok)+"\", \"data\" : [\n")
        for y in data_finally_alerts:
                y_1=y_1+1
                json.dump(y,outfile)
                if y_1<len(data_finally_alerts):
                        outfile.write(",\n")
                if y_1==len(data_finally_alerts):
                        outfile.write("\n")
        outfile.write("]}")
        y_1=0

tiempo = time.time() - t1
print(tiempo)


