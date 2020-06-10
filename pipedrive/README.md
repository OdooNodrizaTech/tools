Se realiza la integración mediante webhooks y SQS con el CRM https://www.pipedrive.com/

## Parámetros de configuración
```
pipedrive_domain
pipedrive_api_token
``` 

pipedrive_domain > https://companydomain.pipedrive.com/
pipedrive_api_token > https://companydomain.pipedrive.com/settings/api
Webhooks > https://companydomain.pipedrive.com/settings/webhooks

## odoo.conf
```
#sqs_pipedrive
sqs_pipedrive_activity_url=https://sqs.eu-west-1.amazonaws.com/734904753081/pipedrive-tuup_dev-webhook-activity-post
sqs_pipedrive_deal_url=https://sqs.eu-west-1.amazonaws.com/734904753081/pipedrive-tuup_dev-webhook-deal-post
sqs_pipedrive_organization_url=https://sqs.eu-west-1.amazonaws.com/734904753081/pipedrive-tuup_dev-webhook-organization-post
sqs_pipedrive_person_url=https://sqs.eu-west-1.amazonaws.com/734904753081/pipedrive-tuup_dev-webhook-person-post
```

## Crones

### Cron SQS Pipedrive Activity
Frecuencia: Cada 5 minutos

Descripción: Consulta el SQS configurado, crearemos las activities como actividades (mail.activity) de Odoo

### Cron Pipedrive Activity Type Exec
Frecuencia: Manual

Descripción: Obtendremos las activityTypes quehabrá que mapear con los tipo de actividad (mail.activity.type) de Odoo

### Cron Pipedrive Currency Exec
Frecuencia: Manual

Descripción: Obtendremos las currencies que se mapearan solas con las monedas (res.currency) de Odoo

### Cron SQS Pipedrive Deal
Frecuencia: Cada 5 minutos

Descripción: Consulta el SQS configurado, crearemos los deals como leads (crm.lead) de Odoo

### Cron SQS Pipedrive Organization
Frecuencia: Cada 5 minutos

Descripción: Consulta el SQS configurado, crearemos las organizations como contactos (res.partner) de Odoo

### Cron SQS Pipedrive Person
Frecuencia: Cada 5 minutos

Descripción: Consulta el SQS configurado, crearemos las persons como contactos (res.partner) de Odoo

### Cron Pipedrive Pipeline Exec
Frecuencia: Manual

Descripción: Obtendremos los pipelines y será necesario definir el tipo: lead/opportunity (Se usará después para crear los leads con ese type, por lo que es MUY importante)

### Cron Pipedrive Product Exec
Frecuencia: Manual

Descripción: Obtendremos los products y será necesario mapearlos con los productos (product.product) de Odoo

### Cron Pipedrive Stage Exec
Frecuencia: Manual

Descripción: Obtendremos los stages y será necesario mapearlos con los etapas (crm.stage) de Odoo y deberemos tener creados previamente los Pipeline para que se vinculen al 100% todos los datos

### Cron Pipedrive User Exec
Frecuencia: Manual

Descripción: Obtendremos los users y será necesario mapearlos con los usuarios (res.users) de Odoo
