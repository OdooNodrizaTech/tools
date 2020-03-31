Se añaden los cambios necesarios para que el widget=phone funcione como un link tel:+34 (o según el valor del campo que se envíe como field_phone_code en las opciones del widget)

Ejemplo SIN campo de código:
```
<field name="mobile" widget="phone" />
``` 

Ejemplo de campo CON código:
```
<field name="mobile_code" class="oe_edit_only" nolabel="1" readonly="0" style="width:30%;" />
<field name="mobile" widget="phone" options="{'field_phone_code': 'mobile_code'}" nolabel="1" readonly="0" style="width:70%;" />
```
