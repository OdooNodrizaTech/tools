El módulo contiene el desarrollo que permite realizar toda la integración respecto a Cesce.

Las horas en las que CESCE ‘procesa’ la información y la devuelve (o devuelve porque un riesgo ha cambiado) son: 08:15, 14:15, 17:15 y 21:00

## odoo.conf
```
#cesce
cesce_ftp_host=cesceconnect.cesce.es
cesce_ftp_user=xxx
cesce_ftp_password=xxx
cesce_ftp_port=2022
``` 

## Parámetros de configuración
```
oniad_cesce_modalidad
oniad_cesce_poliza
oniad_cesce_test_mode
oniad_cesce_csv_delimiter
oniad_cesce_ftp_folder_in        
oniad_cesce_ftp_folder_out                
oniad_cesce_ftp_folder_error        
oniad_cesce_ftp_folder_processed        
oniad_cesce_connection_risk_classification        
oniad_cesce_connection_sale
``` 

### cesce.payment.term
id | code | name
--- | --- | ---
1 | 30 | 30 días
2 | 60 | 60 días
3 | 90 | 90 días
4 | 120 | 120 días
5 | 150 | 150 días
6 | 180 | 180 días 

### cesce.risk.classification.motive
id | code | name
--- | --- | ---
1 | 1 | INSUFICIENTES DATOS PARA LA IDENTIFICACION
2 | 3 | SIN ACTIVIDAD COMERCIAL
3 | 4 | NO HA INICIADO ACTIVIDAD
4 | 5 | LA SOCIEDAD HA CESADO / CEDIDO SUS ACTIVIDADES
5 | 6 | DISOLUCION
6 | 8 | SOCIEDAD EN LIQUIDACION
7 | 9 | DEUDOR EN SITUACION CONCURSAL
8 | 12 | DATOS INSUFICIENTES
9 | 21 | INCIDENCIAS EN PAGOS
10 | 23 | DECISION CESCE
11 | 29 | PATRIMONIO NETO NEGATIVO
12 | 31 | DIMENSION ADECUADA
13 | 32 | DIMENSION REDUCIDA
14 | 33 | AUSENCIA DE DATOS FINANCIEROS DE LA SOCIEDAD
15 | 35 | EVOLUCION NEGATIVA DE RESULTADOS
16 | 37 | EVOLUCION NEGATIVA VENTAS
17 | 46 | SOLICITADO POR EL ASEGURADO<
18 | 53 | CERRADA LA COBERTURA PARA EL PAIS
19 | 66 | REVISION RIESGO
20 | 79 | EVOLUCION POSITIVA DE LAS VENTAS
21 | 80 | SECTOR/EVOLUCION FINANCIERA
22 | 81 | PAIS CON RESTRICCIONES

### cesce.risk.classification.situation

<record id="cesce_risk_classification_situation_data_1" model="cesce.risk.classification.situation">
<field name="id">1</field>
<field name="code">P</field>
<field name="name">Pendiente de estudio</field>
</record>
<record id="cesce_risk_classification_situation_data_2" model="cesce.risk.classification.situation">
<field name="id">2</field>
<field name="code">PC</field>
<field name="name">Clasificado pendiente de aceptacion por el cliente</field>
</record>
<record id="cesce_risk_classification_situation_data_3" model="cesce.risk.classification.situation">
<field name="id">3</field>
<field name="code">T</field>
<field name="name">Preestudios</field>
</record>
<record id="cesce_risk_classification_situation_data_4" model="cesce.risk.classification.situation">
<field name="id">4</field>
<field name="code">C</field>
<field name="name">Clasificado y en cobertura</field>
</record>
<record id="cesce_risk_classification_situation_data_5" model="cesce.risk.classification.situation">
<field name="id">5</field>
<field name="code">N</field>
<field name="name">Clasificado y sin cobertura (anulado)</field>
</record>
<record id="cesce_risk_classification_situation_data_6" model="cesce.risk.classification.situation">
<field name="id">6</field>
<field name="code">PA</field>
<field name="name">Clasificado pendiente de activacion (para contratos PPC)</field>
</record>
<record id="cesce_risk_classification_situation_data_7" model="cesce.risk.classification.situation">
<field name="id">7</field>
<field name="code">PN</field>
<field name="name">Clasificado no asegurado (para contratos PPC)</field>
</record>
 

### cesce.sale.motive.situation

<record id="cesce_sale_motive_situation_data_1" model="cesce.sale.motive.situation">
<field name="id">1</field>
<field name="code">1</field>
<field name="name">SUPLEMENTO INEXISTENTE/NO LOCALIZADO</field>
</record>
<record id="cesce_sale_motive_situation_data_2" model="cesce.sale.motive.situation">
<field name="id">2</field>
<field name="code">2</field>
<field name="name">DEUDOR INEXISTENTE/NO LOCALIZADO</field>
</record>
<record id="cesce_sale_motive_situation_data_3" model="cesce.sale.motive.situation">
<field name="id">3</field>
<field name="code">3</field>
<field name="name">F. ADQUISICION, NO EN PER.VALIDEZ SUPLTO.</field>
</record>
<record id="cesce_sale_motive_situation_data_4" model="cesce.sale.motive.situation">
<field name="id">4</field>
<field name="code">4</field>
<field name="name">SUPLTO.ANUL.(F.ADQUSICION. > F.ANULAC.SUPLTO.)</field>
</record>
<record id="cesce_sale_motive_situation_data_5" model="cesce.sale.motive.situation">
<field name="id">5</field>
<field name="code">5</field>
<field name="name">FECHA ADQUISICION > FECHA PROCESO/NOTIFICACION</field>
</record>
<record id="cesce_sale_motive_situation_data_6" model="cesce.sale.motive.situation">
<field name="id">6</field>
<field name="code">6</field>
<field name="name">FECHA ADQUISICION menor F. EFECTO POLIZA</field>
</record>
<record id="cesce_sale_motive_situation_data_7" model="cesce.sale.motive.situation">
<field name="id">7</field>
<field name="code">7</field>
<field name="name">FECHA ADQUISICION ANTERIOR 1 FECHA EFECTO SUPLEMENTO</field>
</record>
<record id="cesce_sale_motive_situation_data_8" model="cesce.sale.motive.situation">
<field name="id">8</field>
<field name="code">8</field>
<field name="name">FECHA ADQUISICION ANTERIOR 1 FECHA EFECTO SUPLEMENTO</field>
</record>
<record id="cesce_sale_motive_situation_data_9" model="cesce.sale.motive.situation">
<field name="id">9</field>
<field name="code">9</field>
<field name="name">PRIMA POLITICA > PRIMA UNICA ?</field>
</record>
<record id="cesce_sale_motive_situation_data_10" model="cesce.sale.motive.situation">
<field name="id">10</field>
<field name="code">10</field>
<field name="name">COND. PAGO > MAXIMOS DEL SUPLEMENTO</field>
</record>
<record id="cesce_sale_motive_situation_data_11" model="cesce.sale.motive.situation">
<field name="id">11</field>
<field name="code">11</field>
<field name="name">FUERA DE PLAZO</field>
</record>
<record id="cesce_sale_motive_situation_data_12" model="cesce.sale.motive.situation">
<field name="id">12</field>
<field name="code">12</field>
<field name="name">NOTIFICAC. RECHAZADA</field>
</record>
<record id="cesce_sale_motive_situation_data_13" model="cesce.sale.motive.situation">
<field name="id">13</field>
<field name="code">13</field>
<field name="name">EXISTE MAS DE UN DEUDOR PARA EL NIF DADO</field>
</record>
<record id="cesce_sale_motive_situation_data_14" model="cesce.sale.motive.situation">
<field name="id">14</field>
<field name="code">14</field>
<field name="name">EXISTE MAS DE UN DEUDOR PARA EL NIF DADO</field>
</record>
<record id="cesce_sale_motive_situation_data_15" model="cesce.sale.motive.situation">
<field name="id">15</field>
<field name="code">15</field>
<field name="name">SUPLTO. NO EN VIGOR</field>
</record>
<record id="cesce_sale_motive_situation_data_16" model="cesce.sale.motive.situation">
<field name="id">16</field>
<field name="code">16</field>
<field name="name">ANULALIDAD PENDIENTE DE PAGO</field>
</record>
<record id="cesce_sale_motive_situation_data_20" model="cesce.sale.motive.situation">
<field name="id">20</field>
<field name="code">20</field>
<field name="name">DEUDOR DESCONOCIDO</field>
</record>
<record id="cesce_sale_motive_situation_data_21" model="cesce.sale.motive.situation">
<field name="id">21</field>
<field name="code">21</field>
<field name="name">DEUDOR NO CLASIFICADO</field>
</record>
<record id="cesce_sale_motive_situation_data_24" model="cesce.sale.motive.situation">
<field name="id">24</field>
<field name="code">24</field>
<field name="name">NO DISPONE DE TASA PARA ESE PLAZO DE PAGO</field>
</record>
<record id="cesce_sale_motive_situation_data_27" model="cesce.sale.motive.situation">
<field name="id">27</field>
<field name="code">27</field>
<field name="name">INSTRUMENTO/PLAZO PAGO INEXISTENTE</field>
</record>
<record id="cesce_sale_motive_situation_data_28" model="cesce.sale.motive.situation">
<field name="id">28</field>
<field name="code">28</field>
<field name="name">DEUDOR SIN VENTAS PTES. DE VENCER</field>
</record>
<record id="cesce_sale_motive_situation_data_29" model="cesce.sale.motive.situation">
<field name="id">29</field>
<field name="code">29</field>
<field name="name">DEUDOR SIN VENTAS</field>
</record>
<record id="cesce_sale_motive_situation_data_30" model="cesce.sale.motive.situation">
<field name="id">30</field>
<field name="code">30</field>
<field name="name">PAIS EXCLUIDO</field>
</record>
<record id="cesce_sale_motive_situation_data_31" model="cesce.sale.motive.situation">
<field name="id">31</field>
<field name="code">31</field>
<field name="name">RIESGOS EXCLUIDOS</field>
</record>
<record id="cesce_sale_motive_situation_data_32" model="cesce.sale.motive.situation">
<field name="id">32</field>
<field name="code">32</field>
<field name="name">PLAZO PAGO > MAXIMO DE MODALIDAD</field>
</record>
<record id="cesce_sale_motive_situation_data_33" model="cesce.sale.motive.situation">
<field name="id">33</field>
<field name="code">33</field>
<field name="name">NECESIDAD AUTORIZACION DE EMBARQUE</field>
</record>
<record id="cesce_sale_motive_situation_data_34" model="cesce.sale.motive.situation">
<field name="id">34</field>
<field name="code">34</field>
<field name="name">DEUDOR CON IMPAGOS NOTIFICADO</field>
</record>
<record id="cesce_sale_motive_situation_data_37" model="cesce.sale.motive.situation">
<field name="id">37</field>
<field name="code">37</field>
<field name="name">NO CONTEMPLADO EN CONDICIONES POLIZA</field>
</record>
<record id="cesce_sale_motive_situation_data_38" model="cesce.sale.motive.situation">
<field name="id">38</field>
<field name="code">38</field>
<field name="name">DEUDORES EXCLUIDOS</field>
</record>
 

### cesce.sale.situation

<record id="cesce_sale_situation_data_1" model="cesce.sale.situation">
<field name="id">1</field>
<field name="code">1</field>
<field name="name">NO ADMITIDA</field>
</record>
<record id="cesce_sale_situation_data_2" model="cesce.sale.situation">
<field name="id">2</field>
<field name="code">3</field>
<field name="name">CAPTURADO</field>
</record>
<record id="cesce_sale_situation_data_3" model="cesce.sale.situation">
<field name="id">3</field>
<field name="code">4</field>
<field name="name">BAJA</field>
</record>
<record id="cesce_sale_situation_data_4" model="cesce.sale.situation">
<field name="id">4</field>
<field name="code">5</field>
<field name="name">TARIFICADO</field>
</record>
<record id="cesce_sale_situation_data_5" model="cesce.sale.situation">
<field name="id">5</field>
<field name="code">6</field>
<field name="name">ADMITIDA/PDTE. TARIFICAR</field>
</record>
<record id="cesce_sale_situation_data_6" model="cesce.sale.situation">
<field name="id">6</field>
<field name="code">8</field>
<field name="name">ERRONEA</field>
</record>
<record id="cesce_sale_situation_data_7" model="cesce.sale.situation">
<field name="id">7</field>
<field name="code">9</field>
<field name="name">RECHAZADA</field>
</record>
<record id="cesce_sale_situation_data_8" model="cesce.sale.situation">
<field name="id">8</field>
<field name="code">10</field>
<field name="name">REHABILITADA</field>
</record>
<record id="cesce_sale_situation_data_9" model="cesce.sale.situation">
<field name="id">9</field>
<field name="code">11</field>
<field name="name">ADMITIDA/PDTE.ACTUAL.ENTIDADES</field>
</record>
<record id="cesce_sale_situation_data_10" model="cesce.sale.situation">
<field name="id">10</field>
<field name="code">13</field>
<field name="name">SUSPENDIDA COBERTURA</field>
</record>
<record id="cesce_sale_situation_data_11" model="cesce.sale.situation">
<field name="id">11</field>
<field name="code">14</field>
<field name="name">PRORROGADO</field>
</record>
<record id="cesce_sale_situation_data_12" model="cesce.sale.situation">
<field name="id">12</field>
<field name="code">15</field>
<field name="name">RETENIDO</field>
</record>
<record id="cesce_sale_situation_data_13" model="cesce.sale.situation">
<field name="id">13</field>
<field name="code">16</field>
<field name="name">VENCIDO</field>
</record>
<record id="cesce_sale_situation_data_14" model="cesce.sale.situation">
<field name="id">14</field>
<field name="code">19</field>
<field name="name">NCR CARGA INICIAL</field>
</record>
<record id="cesce_sale_situation_data_15" model="cesce.sale.situation">
<field name="id">15</field>
<field name="code">20</field>
<field name="name">PENDIENTE ADMITIR PRORROGA</field>
</record>
 

### cesce.webservice.error

<record id="cesce_webservice_error_data_1" model="cesce.webservice.error">
<field name="id">1</field>
<field name="code">SCU001</field>
<field name="name">Usuario o Password incorrecto</field>
<field name="area">security</field>
</record>
<record id="cesce_webservice_error_data_2" model="cesce.webservice.error">
<field name="id">2</field>
<field name="code">SCU002</field>
<field name="name">Password caducada</field>
<field name="area">none</field>
</record>
<record id="cesce_webservice_error_data_3" model="cesce.webservice.error">
<field name="id">3</field>
<field name="code">SCU003</field>
<field name="name">Usuario desactivado (bloqueado) o Cliente no activo</field>
<field name="area">none</field>
</record>
<record id="cesce_webservice_error_data_4" model="cesce.webservice.error">
<field name="id">4</field>
<field name="code">SCU004</field>
<field name="name">Usuario no valido (para cliente indicado)</field>
<field name="area">none</field>
</record>
<record id="cesce_webservice_error_data_5" model="cesce.webservice.error">
<field name="id">5</field>
<field name="code">CCC001</field>
<field name="name">Contrato no localizado o invalido</field>
<field name="area">none</field>
</record>
<record id="cesce_webservice_error_data_6" model="cesce.webservice.error">
<field name="id">6</field>
<field name="code">CCC002</field>
<field name="name">(NumContrato) contrato y (UsuarioCliente) codigo cliente incorrectos</field>
<field name="area">none</field>
</record>
<record id="cesce_webservice_error_data_7" model="cesce.webservice.error">
<field name="id">7</field>
<field name="code">RSC003</field>
<field name="name">(Deudor.IdFiscal) Codigo fiscal no valido</field>
<field name="area">risk</field>
</record>
<record id="cesce_webservice_error_data_8" model="cesce.webservice.error">
<field name="id">8</field>
<field name="code">RSC004</field>
<field name="name">(Deudor.CodP) Codigo postal no valido</field>
<field name="area">risk</field>
</record>
<record id="cesce_webservice_error_data_9" model="cesce.webservice.error">
<field name="id">9</field>
<field name="code">RSC005</field>
<field name="name">(Deudor.CodP) Codigo Postal no valido</field>
<field name="area">risk</field>
</record>
<record id="cesce_webservice_error_data_10" model="cesce.webservice.error">
<field name="id">10</field>
<field name="code">RSC006</field>
<field name="name">(Deudor.Tel) Telefono no valido</field>
<field name="area">risk</field>
</record>
<record id="cesce_webservice_error_data_11" model="cesce.webservice.error">
<field name="id">11</field>
<field name="code">RSC007</field>
<field name="name">(Deudor.Mail) Email no valido</field>
<field name="area">risk</field>
</record>
<record id="cesce_webservice_error_data_12" model="cesce.webservice.error">
<field name="id">12</field>
<field name="code">RSC008</field>
<field name="name">(Deudor.ImpS) Importe no puede ser cero</field>
<field name="area">risk</field>
</record>
<record id="cesce_webservice_error_data_13" model="cesce.webservice.error">
<field name="id">13</field>
<field name="code">RSC009</field>
<field name="name">(Deudor.Mon) Codigo moneda ISO no valido</field>
<field name="area">risk</field>
</record>
<record id="cesce_webservice_error_data_14" model="cesce.webservice.error">
<field name="id">14</field>
<field name="code">RSC010</field>
<field name="name">(Deudor.PzoS) Plazo de pago invalido (ejem: 30, 60, 90, 120, 150, 180)</field>
<field name="area">risk</field>
</record>
<record id="cesce_webservice_error_data_15" model="cesce.webservice.error">
<field name="id">15</field>
<field name="code">RSC011</field>
<field name="name">(Deudor.Impagos) no valido, opciones posibles: Y,N</field>
<field name="area">risk</field>
</record>
<record id="cesce_webservice_error_data_16" model="cesce.webservice.error">
<field name="id">16</field>
<field name="code">RSC012</field>
<field name="name">(Deudor.ImpImpagos) Si Deudor.Impagos='Y' importe no puede ser 0</field>
<field name="area">risk</field>
</record>
<record id="cesce_webservice_error_data_17" model="cesce.webservice.error">
<field name="id">17</field>
<field name="code">RSC013</field>
<field name="name">(Deudor.InsPagoS) plazo de pago invalido</field>
<field name="area">risk</field>
</record>
<record id="cesce_webservice_error_data_18" model="cesce.webservice.error">
<field name="id">18</field>
<field name="code">RSC014</field>
<field name="name">(Deudor.Nif, Deudor.Nom) Campo obligatorio</field>
<field name="area">risk</field>
</record>
<record id="cesce_webservice_error_data_19" model="cesce.webservice.error">
<field name="id">19</field>
<field name="code">RSC015</field>
<field name="name">(Deudor.Pais) codigo ISO pais no valido</field>
<field name="area">risk</field>
</record>
<record id="cesce_webservice_error_data_20" model="cesce.webservice.error">
<field name="id">20</field>
<field name="code">RAD0001</field>
<field name="name">Clasificacion o Empresa no localizada</field>
<field name="area">risk</field>
</record>
<record id="cesce_webservice_error_data_21" model="cesce.webservice.error">
<field name="id">21</field>
<field name="code">RAD0002</field>
<field name="name">Empresa.Pais y Empresa.Nif o Empresa.Spto, o Empresa.RC obligatorios</field>
<field name="area">risk</field>
</record>


En el apartado Contabilidad > Ventas se añade el apartado "Cesce" con los apuntes contables que correspondería para exportara a Cesce.

Para instalarlo será necesario eliminar estas líneas en res_partner_view.xml
```
                <div>
                    <button type="action" class="btn-link" name="%(oniad_cesce.cesce_risk_classification_action)d" context="{'search_default_partner_id': active_id}">
                        <field string="Cesce clasificaciones de riesgo" name="cesce_risk_classification_count" widget="statinfo"/>
                    </button>
                </div>
```                
y una vez instalado, colocarlas de nuevo y actualizar el addon

 
Aplicar permisos 777 a la carpeta /ont/tools/cesce/

## Crones

### Cron Cesce Risk Classsification Check File Out 
Frecuencia: 1 vez cada 3 horas

Descripción:

Revisa los errores de Clasificaciones de riesgo (la información que CESCE nos ha dejado en el FTP y que no habíamos gestionado)
Revisa los OUT de Clasifiaciones de riesgo (la información que CESCE nos ha dejado en el FTP y que no habíamos gestionado)

Toda esta información siempre será respecto a lo que previamente le hemos pedido (enviado Clasifiaciones de riesgo) o cambios que Cesce ha hecho (le ha modificado -aumentado, dismimuido o eliminado- el riesgo concedido) respecto a un cliente

### Cron Cesce Sale Generate File 
Frecuencia: 1 vez al mes

Día: 15/xx/xxxx

Descripción: 

Revisa todos los apuntes contables de la cuenta contable de Clientes del diario de "Facturas de cliente" con debit > 0, cliente que tenga riesgo > 0, 'Estado venta cesce' = 'ninguno' y con la fecha de factura de la factura vinculado >= hoy -1 mes (dia 1) y <= día1 del mes actual + 1 mes - 1 dia
De todos los apuntes contables que corresponde se "declara la venta" (genera el archivo en el FTP) y se cambia el estado "Venta enviada"

### Cron Cesce Sale Check File Out 
Frecuencia: 1 vez al día

Descripción:

Revisa los errores de Declaracion de ventas (la información que CESCE nos ha dejado en el FTP y que no habíamos gestionado)
Revisa los OUT de Declaracion de ventas (la información que CESCE nos ha dejado en el FTP y que no habíamos gestionado)

Toda esta información lo mas probable es que solo nos la de 1 vez al mes puesto que si SOLO notificamos ventas desde Odoo y las notificamos 1 vez al mes es "poco probable" que nos notifiquen otras cosas en otros días, pero por si acaso.

### Cron Cesce Risk Classification Fecha Renovacion 
Frecuencia: 1 vez cada mes

Día: 15/xxx/xxxx

Descripción:

Revisa todas las clasificaciones de riesgo filtrando por "fecha renovacion" >= hoy y <= hoy -30 dias, clientes activos y clientes cuyo "Estado riesgo cesce" sea ("Clasificacion enviada", "Clasificacion Ok" o "Clasificación error"
De las clasificaciones de riesgo que se encuentran se busca la suma de la BI de factura de venta de los últimos 6 meses y se envia esa información al canal de Slack para "actuar" sobre ellos

### Cron Cesce Risk Classification Cambiar Fecha Renovacion 
Frecuencia: 1 vez al mes

Día: 06/xx/xxxx

Descripción:

Revisa todas las clasifiaciones de riesgo cuya fecha de renovacion sea < hoy - 2 meses, que el cliente tiene un riesgo > 0€ y que el estado de "Clasificacion de riesgo" sea "Clasificacion Ok"
De las clasifaciones de riesgo que encuentra con estos criterios le incrementa 1 año a la fecha de renovación que tuviera.
