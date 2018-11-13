DECLARE
 v_tablespace_name              dba_data_files.tablespace_name%TYPE;
 v_tam_kbytes                   NUMBER(14);
 v_libre_kbytes                 NUMBER(14);
 v_ocupado_kbytes               NUMBER(14);
 v_max_bloque_libre             NUMBER(14);
 v_crec_ocupado_diario_kbytes   NUMBER(14);
 v_max_creci_ultimos_dias       NUMBER(14);
 v_extents                      NUMBER(14);
 v_crec_diario_extents          NUMBER(8);
 v_cliente                      VARCHAR2(20);
 v_tipo                         VARCHAR2(20);
 v_fecha_mysql                  VARCHAR2(12);
 v_sid                          CHAR(3);
 v_descripcion                  VARCHAR2(45);
 v_line                         VARCHAR2(4000);

CURSOR data_files IS
  SELECT tablespace_name, sum(bytes)/1024 tam_kbytes
    FROM dba_data_files
   WHERE tablespace_name !='PSAPTEMP'
     AND tablespace_name !='PSAPROLL'
     AND tablespace_name !='PSAPUNDO'
     AND tablespace_name !='PSAPUNDO01'
     AND tablespace_name !='UNDOTBS1'
     AND tablespace_name !='PSAPUNDO001'
     AND tablespace_name !='PSAPUNDO002'
   GROUP BY tablespace_name;

BEGIN
 /* v_cliente := 'customer';*/
 /* v_tipo := 'dbtype';*/
 /* v_fecha_mysql := '200420181135';*/
 /* v_sid := 'sid';*/
 /* v_descripcion := 'dbname';*/
  v_crec_ocupado_diario_kbytes := 0;
  v_crec_diario_extents := 0;
  v_max_creci_ultimos_dias := 0;
  FOR tablespaces IN data_files LOOP
      v_tablespace_name := tablespaces.tablespace_name;
      v_tam_kbytes := tablespaces.tam_kbytes;

      SELECT SUM(bytes)/1024, MAX(bytes)/1024
        INTO v_libre_kbytes, v_max_bloque_libre
        FROM dba_free_space
        WHERE tablespace_name=v_tablespace_name;
      IF v_libre_kbytes IS NULL THEN
         v_libre_kbytes :=0;
      END IF;
      IF v_max_bloque_libre IS NULL THEN
         v_max_bloque_libre :=0;
      END IF;
      SELECT SUM(bytes)/1024, SUM(extents)
        INTO v_ocupado_kbytes, v_extents
        FROM dba_segments
      WHERE tablespace_name=v_tablespace_name;
      IF v_ocupado_kbytes IS NULL THEN
         v_ocupado_kbytes :=0;
      END IF;
      IF v_extents IS NULL THEN
         v_extents :=0;
      END IF;

/*DBMS_OUTPUT.PUT_LINE(v_cliente||','||v_tipo||','||v_fecha_mysql||','||v_sid||','||v_descripcion||','||v_tablespace_name||','||v_tam_kbytes||','||v_libre_kbytes||','||v_ocupado_kbytes||','||v_max_bloque_libre||','||v_crec_ocupado_diario_kbytes||','||v_extents||','||v_crec_diario_extents||','||v_max_creci_ultimos_dias);*/

v_line:=v_line||v_tablespace_name||','||v_tam_kbytes||','||v_libre_kbytes||','||v_ocupado_kbytes||','||v_max_bloque_libre||','||v_crec_ocupado_diario_kbytes||','||v_extents||','||v_crec_diario_extents||','||v_max_creci_ultimos_dias||'|';
        :cur_out:=v_line;
END LOOP;
END;
