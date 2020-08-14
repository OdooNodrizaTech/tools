Se realiza la integración con GoogleAnalytics para obtener información respecto a:

- googleanalytics_result_beahavior
- googleanalytics_result_campaign
- googleanalytics_result_general

## odoo.conf
- #googleanalytics_api
- googleanalytics_api_key_file=/home/ubuntu/googleanalytics_api_key_file.json

## Crones

### Cron Googleanalytics Result Beahavior Get Previous Day info

Frecuencia: 1 vez al día
Descripción: Obtiene todos los datos de la API de acuerdo al día anterior de los profile_ids definidos
