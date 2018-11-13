########### AUTOR: ORLANDO CORREA #################

### PARAMETROS DE ENTRADA EN ORDEN: ###############
### Script que genera un JSON con un listado de   #
### uso historico de determinada Base de datos    #
###     1. CLIENTE                                #
###     2. TIPO DE BASE DE DATOS                  #
###     3. SID                                    #
###     4. DESCRIPCION DEL SISTEMA                #
###     5. NOMBRE DEL TABLESPACE                  #
###     6. NUMERO DE HISTORICOS QUE QUIERE VER    #
###                                               #
###################################################

import json,collections
import mysql.connector #Driver for MySQL
from mysql.connector import errorcode #Error management
import sys
import datetime
from datetime import timedelta
from datetime import datetime as dt

list_tablespace_readys,data_finally=[],[]
x = [['cliente', 'dbtype','sid','ambiente','tablespace','used','free','vida','fecha']]

x_1=0
y_1=0
todayok=dt.now().strftime('%Y-%m-%d %H:%M:%S')
d = datetime.date.today()  # Today

# CREACION DELTA DE DIAS
lastday= d - timedelta(days=int(float(sys.argv[6])))
onelastday= lastday.strftime('%Y-%m-%d') +' '+ '13:30:40';
today= d.strftime('%Y-%m-%d') +' '+ '13:30:40'

###### LOGICA DE EXTRACION DE ESPACIOS, SIENDO FILTRADAS POR LOS PARAMETROS CLIENTE-DESCRIPCION-TABLESPACE-FECHA----ASEGURANDO ASI LOS DATOS CORRECTOS ############

cnx=mysql.connector.connect(user='espacios', password='ibmsap2014', database='espacios');
cur_sql=cnx.cursor();
query=("SELECT CLIENTE,TIPO_DB,SID,DESCRIPCION,TABLESPACE,OCUPADO_KBYTES,LIBRE_KBYTES,MAX_CRECI_ULTIMOS_DIAS,FECHA FROM espacios_stats where TIPO_DB=%s and SID=%s and DESCRIPCION=%s and TABLESPACE=%s and FECHA between %s and %s")
cur_sql.execute(query,(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],onelastday,today));
data_sql = cur_sql.fetchall ()

# ACTUALIZACION TABLA DE LOS CLIENTES LEIDOS EL DIA DE HOY
for (CLIENTE,TIPO_DB,SID,DESCRIPCION,TABLESPACE,OCUPADO_KBYTES,LIBRE_KBYTES,MAX_CRECI_ULTIMOS_DIAS,FECHA) in data_sql:
        list_tablespace_readys.append(CLIENTE+"|"+TIPO_DB+"|"+SID+"|"+DESCRIPCION+"|"+TABLESPACE+"|"+str(OCUPADO_KBYTES)+"|"+str(LIBRE_KBYTES)+"|"+str(MAX_CRECI_ULTIMOS_DIAS)+"|"+str(FECHA))


text = 'some string... this part will be removed.'
head, sep, tail = text.partition('...')

for k in list_tablespace_readys:
        data=k.split("|")
        fecha_sort,nofunk,nofunk1 = data[8].partition(' ')
        data_finally.append((data[0],data[1],data[2],data[3],data[4],"{0:.4f}".format((float(data[5])/1000.0)),"{0:.4f}".format((float(data[6])/1000.0)),data[7],fecha_sort))

with open('/home/coecogni/espacios/data_historico_'+sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'_'+sys.argv[5]+'.json', 'w') as outfile:
        outfile.write("{\"fecha\": \""+str(todayok)+"\", \"data\" : [\n")
        for x in data_finally:
                x_1=x_1+1
                json.dump({'fecha':x[8],'cliente':x[0], 'dbtype':x[1],'sid':x[2],'ambiente':x[3],'tablespace':x[4],'used':x[5],'free':x[6],'vida':x[7]},outfile,indent=4)
                if x_1<(len(data_finally)):
                        outfile.write(",\n")
                if x_1==len(data_finally):
                        outfile.write("\n")
        outfile.write("]}")
        x_1=0

