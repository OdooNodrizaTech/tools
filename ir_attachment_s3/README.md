El módulo contiene el desarrollo respecto a la integración con S3 de diferentes backups

 
### odoo.conf
```
aws_access_key_id=xxxx
aws_secret_key_id=xxxxx
aws_region_name=eu-west-1
```

### Parámetros de configuración
```
ir_attachment_s3_bucket_name
```

En la acción de eliminar un adjunto, se revisa si es del tipo URL y si contiene amazonaws.com puesto que en ese caso será necesario eliminarlo de S3.
 
Importante que el bucket de S3 tenga permiso público. 

Existen diferentes crons para diferentes acciones:

### S3 Upload Ir Attachments 

Frecuencia: 1 vez al día

Hora: 14:37

Descripción: 

Revisa todos los adjuntos del sistema de type 'binary' que tengan un elemento relacionado y un model limitando la consulta a 1000.
Para cada uno de los registros se sube a S3 al directorio correspondiente del bucket de S3 definido

 

No debería ser necesario este cron puesto que cada vez que se crea un adjunto se envía a S3 directamente (así como cuando se elimina) pero se hace "por si acaso".
