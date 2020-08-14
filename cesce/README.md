El módulo contiene el desarrollo que permite realizar toda la integración respecto a Cesce (https://www.cesce.es/).

Las horas en las que CESCE ‘procesa’ la información y la devuelve (o devuelve porque un riesgo ha cambiado) son: 08:15, 14:15, 17:15 y 21:00

## odoo.conf
- #cesce
- cesce_ftp_host=cesceconnect.cesce.es
- cesce_ftp_user=xxx
- cesce_ftp_password=xxx
- cesce_ftp_port=2022

## Parámetros de configuración
- oniad_cesce_modalidad
- oniad_cesce_poliza
- oniad_cesce_test_mode
- oniad_cesce_csv_delimiter
- oniad_cesce_ftp_folder_in        
- oniad_cesce_ftp_folder_out                
- oniad_cesce_ftp_folder_error        
- oniad_cesce_ftp_folder_processed        
- oniad_cesce_connection_risk_classification        
- oniad_cesce_connection_sale

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
id | code | name
--- | --- | ---
1 | P | Pendiente de estudio
2 | PC | Clasificado pendiente de aceptacion por el cliente
3 | T | Preestudios
4 | C | Clasificado y en cobertura
5 | N | Clasificado y sin cobertura (anulado)
6 | PA | Clasificado pendiente de activacion (para contratos PPC)
7 | PN | Clasificado no asegurado (para contratos PPC)

### cesce.sale.motive.situation
id | code | name
--- | --- | ---
1 | 1 | SUPLEMENTO INEXISTENTE/NO LOCALIZADO
2 | 2 | DEUDOR INEXISTENTE/NO LOCALIZADO
3 | 3 | F. ADQUISICION, NO EN PER.VALIDEZ SUPLTO.
4 | 4 | SUPLTO.ANUL.(F.ADQUSICION. > F.ANULAC.SUPLTO.)
5 | 5 | FECHA ADQUISICION > FECHA PROCESO/NOTIFICACION
6 | 6 | FECHA ADQUISICION menor F. EFECTO POLIZ
7 | 7 | FECHA ADQUISICION ANTERIOR 1 FECHA EFECTO SUPLEMENTO
8 | 8 | FECHA ADQUISICION ANTERIOR 1 FECHA EFECTO SUPLEMENTO
9 | 9 | PRIMA POLITICA > PRIMA UNICA ?
10 | 10 | COND. PAGO > MAXIMOS DEL SUPLEMENTO
11 | 11 | FUERA DE PLAZO
12 | 12 | NOTIFICAC. RECHAZADA
13 | 13 | EXISTE MAS DE UN DEUDOR PARA EL NIF DADO
14 | 14 | EXISTE MAS DE UN DEUDOR PARA EL NIF DADO
15 | 15 | SUPLTO. NO EN VIGOR
16 | 16 | ANULALIDAD PENDIENTE DE PAGO
20 | 20 | DEUDOR DESCONOCIDO
21 | 21 | DEUDOR NO CLASIFICADO
24 | 24 | NO DISPONE DE TASA PARA ESE PLAZO DE PAGO
27 | 27 | INSTRUMENTO/PLAZO PAGO INEXISTENTE
28 | 28 | DEUDOR SIN VENTAS PTES. DE VENCER
29 | 29 | DEUDOR SIN VENTAS
30 | 30 | PAIS EXCLUIDO
31 | 31 | RIESGOS EXCLUIDOS
32 | 32 | PLAZO PAGO > MAXIMO DE MODALIDAD
33 | 33 | NECESIDAD AUTORIZACION DE EMBARQUE
34 | 34 | DEUDOR CON IMPAGOS NOTIFICADO
37 | 37 | NO CONTEMPLADO EN CONDICIONES POLIZA
38 | 38 | DEUDORES EXCLUIDOS

### cesce.sale.situation
id | code | name
--- | --- | ---
1 | 1 | NO ADMITIDA
2 | 2 | CAPTURADO
3 | 4 | BAJA
4 | 5 | TARIFICADO
5 | 6 | ADMITIDA/PDTE. TARIFICAR
6 | 8 | ERRONEA
7 | 9 | RECHAZADA
8 | 10 | REHABILITADA
9 | 11 | ADMITIDA/PDTE.ACTUAL.ENTIDADES
10 | 13 | SUSPENDIDA COBERTURA
11 | 14 | PRORROGADO
12 | 15 | RETENIDO
13 | 16 | VENCIDO
14 | 19 | NCR CARGA INICIAL
15 | 20 | PENDIENTE ADMITIR PRORROGA

### cesce.webservice.error
id | code | name | area
--- | --- | --- | ---
1 | SCU001 | Usuario o Password incorrecto | security
2 | SCU002 | Password caducada | none
3 | SCU003 | Usuario desactivado (bloqueado) o Cliente no activo | none
4 | SCU004 | Usuario no valido (para cliente indicado) | none
5 | CCC001 | Contrato no localizado o invalido | none
6 | CCC002 | (NumContrato) contrato y (UsuarioCliente) codigo cliente incorrectos | none
7 | RSC003 | (Deudor.IdFiscal) Codigo fiscal no valido | risk
8 | RSC004 | (Deudor.CodP) Codigo postal no valido | risk
9 | RSC005 | (Deudor.CodP) Codigo Postal no valido | risk
10 | RSC006 | (Deudor.Tel) Telefono no valido | risk
11 | RSC007 | (Deudor.Mail) Email no valido | risk
12 | RSC008 | (Deudor.ImpS) Importe no puede ser cero | risk
13 | RSC009 | (Deudor.Mon) Codigo moneda ISO no valido | risk
14 | RSC010 | (Deudor.PzoS) Plazo de pago invalido (ejem: 30, 60, 90, 120, 150, 180) | risk
15 | RSC011 | (Deudor.Impagos) no valido, opciones posibles: Y,N | risk
16 | RSC012 | (Deudor.ImpImpagos) Si Deudor.Impagos='Y' importe no puede ser 0 | risk
17 | RSC013 | (Deudor.InsPagoS) plazo de pago invalido | risk
18 | RSC014 | (Deudor.Nif, Deudor.Nom) Campo obligatorio | risk
19 | RSC015 | (Deudor.Pais) codigo ISO pais no valido | risk
20 | RAD0001 | Clasificacion o Empresa no localizada | risk
21 | RAD0002 | Empresa.Pais y Empresa.Nif o Empresa.Spto, o Empresa.RC obligatorios | risk


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
Frecuencia: 1 vez cada 3 horas

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
