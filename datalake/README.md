El módulo contiene el desarrollo respecto a enviar los datos a datalake

## odoo.conf
```
aws_access_key_id=xxx
aws_secret_key_id=xxxx
```

## Parámetros de configuración
```
ses_datalake_test
```

## Crones

### Cron Generate Google Analytics Reports Yesterday - Datalake 

Frecuencia: 1 vez cada día

Descripción: Envía a los diferentes SNS (https://grupoarelux.atlassian.net/wiki/spaces/O/pages/323879466/Google+Analytics) un mensaje con los parámetros correspondientes respecto a la fecha de ay


### Cron Generate Google Analytics Reports All Year - Datalake 

Frecuencia: 1 vez cada año

Descripción: Envía a los diferentes SNS (https://grupoarelux.atlassian.net/wiki/spaces/O/pages/323879466/Google+Analytics) un mensaje con los parámetros correspondientes respecto a todos los días (hasta la fecha) del año actual.
