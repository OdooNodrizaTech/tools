# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models
import datetime, os, codecs, pysftp
from dateutil.relativedelta import relativedelta

import odoo
import sys

def index_exists(ls, i):
    return (0 <= i < len(ls)) or (-len(ls) <= i < 0)

class CesceWebService():

    def __init__(self, company, env):
        self.company = company
        self.custom_env = env
                            
        self.modalidad = env['ir.config_parameter'].sudo().get_param('cesce_modalidad')                        
        self.poliza = env['ir.config_parameter'].sudo().get_param('cesce_poliza')
        
        self.separator_fields = env['ir.config_parameter'].sudo().get_param('cesce_csv_delimiter')
        #test_mode
        self.test_mode = True
        cesce_test_mode = str(env['ir.config_parameter'].sudo().get_param('cesce_test_mode'))
        if cesce_test_mode=='False':
            self.test_mode = False 
        
        self.connection_risk_classification = env['ir.config_parameter'].sudo().get_param('cesce_connection_risk_classification')
        self.connection_sale = env['ir.config_parameter'].sudo().get_param('cesce_connection_sale')        
        
        self.connection_ftp_host = odoo.tools.config.get('cesce_ftp_host')
        self.connection_ftp_user = odoo.tools.config.get('cesce_ftp_user')
        self.connection_ftp_password = odoo.tools.config.get('cesce_ftp_password')
        self.connection_ftp_port = int(odoo.tools.config.get('cesce_ftp_port'))        
        
        self.ftp_folder_in = str(env['ir.config_parameter'].sudo().get_param('cesce_ftp_folder_in'))
        self.ftp_folder_out = str(env['ir.config_parameter'].sudo().get_param('cesce_ftp_folder_out'))
        self.ftp_folder_error = str(env['ir.config_parameter'].sudo().get_param('cesce_ftp_folder_error'))
        self.ftp_folder_processed = str(env['ir.config_parameter'].sudo().get_param('cesce_ftp_folder_processed'))
        
        self.cod_provicnasi_esp = {
            'VI': '01',#Alava
            'AB': '02',#Albacete
            'A': '03',#Alicante
            'AL': '04',#Almeria
            'AV': '05',#Avila
            'BA': '06',#Badajoz
            'PM': '07',#Baleares
            'B': '08',#Barcelona
            'BU': '09',#Burgos
            'CC': '10',#Caceres
            'CA': '11',#Cadiz
            'CS': '12',#Castellon
            'CR': '13',#Ciudad Real
            'CO': '14',#Cordoba
            'C': '15',#La coru�a
            'CU': '16',#Cuenca
            'GI': '17',#Gerona
            'GR': '18',#Granada
            'GU': '19',#Guadalajara
            'SS': '20',#Guipuzcoa
            'H': '21',#Huelva
            'HU': '22',#Huesca
            'J': '23',#Jaen
            'LE': '24',#Leon
            'L': '25',#Lerida
            'LO': '26',#La Rioja
            'LU': '27',#Lugo
            'M': '28',#Madrid
            'MA': '29',#Malaga
            'MU': '30',#Murcia
            'NA': '31',#Navarra
            'OR': '32',#Orense
            'O': '33',#Asturias
            'P': '34',#Palencia
            'GC': '35',#Las palmas
            'PO': '36',#Pontevedra
            'SA': '37',#Salamanca
            'TF': '38',#SC Tenerife
            'S': '39',#Cantabria
            'SG': '40',#Segovia
            'SE': '41',#Sevilla
            'SO': '42',#Soria
            'T': '43',#Tarragona
            'TE': '44',#Teruel
            'TO': '45',#Toledo
            'V': '46',#Valencia
            'VA': '47',#Valladolid
            'BI': '48',#Vizcaya
            'ZA': '49',#Zamora
            'Z': '50',#Zaragoza
            'CE': '51',#Ceuta
            'ME': '52',#Melilla
        }
    
    #upload_file_ftp    
    def upload_file_ftp(self, file_name, file_name_real, folder):
        response = {
            'errors': True, 
            'error': "", 
        }
        
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        
        try:
            response['errors'] = True
            response['error'] = 'Error de conexion'
            
            with pysftp.Connection(host=self.connection_ftp_host, username=self.connection_ftp_user, password=self.connection_ftp_password, port=self.connection_ftp_port, cnopts=cnopts) as sftp:
                remote_file = folder+'/'+file_name_real
                sftp.put(file_name, remote_file)
                sftp.close()
                
                response['errors'] = False
                response['error'] = ''
        except Exception as e:
            _logger.info(cnopts)
                                     
            response['errors'] = True
            response['error'] = str(e.message)
            
        return response                        
    
    #get_files_in_folder_ftp    
    def get_files_in_folder_ftp(self, folder, tmp_file):
        files = {}
        
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        
        file_name_err_tmp = os.path.dirname(os.path.abspath(__file__))+'/'+tmp_file
        if os.path.isfile(file_name_err_tmp):
            os.remove(file_name_err_tmp)
                
        with pysftp.Connection(host=self.connection_ftp_host, username=self.connection_ftp_user, password=self.connection_ftp_password, port=self.connection_ftp_port, cnopts=cnopts) as sftp:
            files_get = sftp.listdir(folder)
            if len(files_get)>0:                
                for file_get in files_get:
                    files[file_get] = []
                    file_get_name = str(folder)+'/'+str(file_get)
                    sftp.get(file_get_name, file_name_err_tmp)
                    
                    if os.path.isfile(file_name_err_tmp):
                        #fh = codecs.open(file_name_err_tmp, "r", "utf-8-sig")
                        fh = codecs.open(file_name_err_tmp, mode="r")
                        lines = fh.readlines()
                        
                        if len(lines)>0:
                            for line in lines:
                                #line = unicode(line, errors='replace')#fix errors
                                line = line.decode('latin-1').encode("utf-8")                                                                                                                                                
                                line_split = line.split(self.separator_fields)                                                                
                                if len(line_split)>0:
                                    line_real = []
                                    for line_split_item in line_split:
                                        #line_split_item = line_split_item.decode("UTF-8").replace(u'\ufeff', u'')                                        
                                        line_real.append(line_split_item)
                                        
                                    files[file_get].append(line_real)
        #cesce_files_check                 
        cesce_files_check = []
        cesce_file_check_ids = self.custom_env['cesce.file.check'].search([('folder', '=', folder)])
        if len(cesce_file_check_ids)>0:
            for cesce_file_check_id in cesce_file_check_ids:
                cesce_files_check.append(cesce_file_check_id.file)
            #check
            for file_name, file_name_items_real in files.items():
                if file_name in cesce_files_check:
                    del files[file_name]
        
        return files                                    
    
    #partner_classifications_error
    def partner_classifications_error(self):        
        if self.connection_risk_classification=='ftp':
            self.partner_classifications_error_ftp()
        else:
            self.partner_classifications_error_webservice()
    
    def partner_classifications_error_webservice(self):
        _logger.info('partner_classifications_error_webservice')
        
    def partner_classifications_error_ftp(self):                
        tmp_file = 'error_solicitudes_tmp.txt'
        return_files_in_folder = self.get_files_in_folder_ftp(self.ftp_folder_error, tmp_file)        
        if len(return_files_in_folder)>0:
            for file_name, file_name_items_real in return_files_in_folder.items():
                cesce_file_check_ids = self.custom_env['cesce.file.check'].search([('folder', '=', str(self.ftp_folder_error)), ('file', '=', str(file_name))])
                if len(cesce_file_check_ids) == 0:
                    #operations
                    if 'ERR_SOLICITUDES' in file_name:
                        for file_name_items in file_name_items_real:
                            _logger.info(file_name)
                            _logger.info(file_name_items)
                            partner_id_get = int(str(file_name_items[0]))
                            #importe_solicitado
                            importe_solicitado = file_name_items[10].replace('.', '').replace(',', '.')
                            texto_error = file_name_items[22]

                            if partner_id_get>0:
                                res_partner_ids = self.custom_env['res.partner'].search([('id', '=', partner_id_get)])
                                if len(res_partner_ids)==0:
                                    _logger.info('raro, no se encuentra el partner_id='+str(partner_id_get))
                                else:
                                    res_partner_id_obj = res_partner_ids[0]
                                    if res_partner_id_obj.cesce_risk_state=='classification_sent':
                                        res_partner_id_obj.cesce_risk_state = 'classification_error'
                                    #cesce_error
                                    res_partner_id_obj.cesce_error = texto_error                                    
                    #save cesce_file_check
                    cesce_file_check_vals = {
                        'folder': self.ftp_folder_error,
                        'file': file_name
                    }
                    cesce_file_check_obj = self.custom_env['cesce.file.check'].sudo().create(cesce_file_check_vals)
                                                                                                                                                                                                                                                                
        
    #partner_classifications_out
    def partner_classifications_out(self):
        if self.connection_risk_classification=='ftp':
            self.partner_classifications_out_ftp()
        else:
            self.partner_classifications_out_webservice()
    
    def partner_classifications_out_webservice(self):
        _logger.info('partner_classifications_out_webservice')

    def partner_classification_item_define(self, data):
        #define
        item = {
            'partner_id': False,#25 o 23 o 6
            'code_cesce': False,#0
            'num_sup_cesce': False,#1
            'nombre_deudor': False,#2
            'codigo_fiscal': False,#3
            'codigo_deudor_cesce': False,#4
            'grupo_riesgo_deudor': False,#5
            'mercado': 'inside',#6
            'pais_provincia': False,#7
            'importe_solicitado': False,#8
            'importe_concedido': False,#9
            'currency_id': 1,  # 10
            'plazo_solicitado': False,#11
            'plazo_concedido': False,#12
            'condicion_pago': False,#13
            'tipo_movimiento': False,#14
            'cesce_risk_classification_situation_id': False,#15
            'fecha_solicitud': False,#16
            'fecha_efecto': False,#17
            'fecha_renovacion': False,#extra
            'fecha_anulacion': False,#18
            'fecha_validez': False,#19
            'motivo_validez': False,#20
            'riesgo_comercial': False,#21
            'riesgo_politico': False,#22
            'avalistas': False,#23
            'cesce_risk_classification_motive_id': False,#24
            'codigo_deudor_interno': False,#25
        }
        #code_cesce
        if index_exists(data, 0)==True:
            item['code_cesce'] = str(data[0])
        #num_sup_cesce
        if index_exists(data, 1)==True:
            item['num_sup_cesce'] = str(data[1])
        #nombre_deudor
        if index_exists(data, 2)==True:
            item['nombre_deudor'] = str(data[2])
        #codigo_fiscal
        if index_exists(data, 3)==True:
            item['codigo_fiscal'] = str(data[3]).strip()
        #codigo_deudor_cesce
        if index_exists(data, 4)==True:
            item['codigo_deudor_cesce'] = str(data[4])
        #grupo_riesgo_deudor
        if index_exists(data, 5)==True:
            item['grupo_riesgo_deudor'] = int(str(data[5]))
        #mercado
        if index_exists(data, 6)==True:
            if data[6] == 'Exterior':
                item['mercado'] = 'outside'
        #pais_provincia
        if index_exists(data, 7)==True:
            item['pais_provincia'] = str(data[7])
        # importe_solicitado
        if index_exists(data, 8)==True:
            item['importe_solicitado'] = str(data[8].replace('.', '').replace(',', '.'))
        # importe_concedido
        if index_exists(data, 9)==True:
            item['importe_concedido'] = str(data[9].replace('.', '').replace(',', '.'))
        # currency_id
        if index_exists(data, 10)==True:
            res_currency_ids = self.custom_env['res.currency'].sudo().search([('name', '=', data[10])])
            if len(res_currency_ids) > 0:
                item['currency_id'] = res_currency_ids[0].id
        # plazo_solicitado
        if index_exists(data, 11)==True:
            item['plazo_solicitado'] = int(str(data[11].replace('DIAS', '').strip()))
        # plazo_concedido
        if index_exists(data, 12)==True:
            item['plazo_concedido'] = str(data[12].replace('DIAS', '').strip())
            if item['plazo_concedido']!='':
                item['plazo_concedido'] = int(item['plazo_concedido'])
        # condicion_pago
        if index_exists(data, 13)==True:
            item['condicion_pago'] = str(data[13].replace('OTROS', '').strip())
        #tipo_movimiento
        if index_exists(data, 14)==True:
            item['tipo_movimiento'] = str(data[14])
        # cesce_risk_classification_situation_id
        if index_exists(data, 15)==True:
            cesce_risk_classification_situation_ids = self.custom_env['cesce.risk.classification.situation'].search([('code', '=', data[15])])
            if len(cesce_risk_classification_situation_ids) > 0:
                item['cesce_risk_classification_situation_id'] = cesce_risk_classification_situation_ids[0].id
        # fecha_solicitud
        if index_exists(data, 16)==True:
            fecha_solicitud_pre = data[16]
            item['fecha_solicitud'] = str(fecha_solicitud_pre[0:4]) + '-' + str(fecha_solicitud_pre[4:6]) + '-' + str(fecha_solicitud_pre[6:8])
        # fecha_efecto + fecha_renovacion
        if index_exists(data, 17)==True:
            fecha_efecto_pre = data[17]
            year_fecha_efecto = int(fecha_efecto_pre[0:4])
            item['fecha_efecto'] = str(fecha_efecto_pre[0:4]) + '-' + str(fecha_efecto_pre[4:6]) + '-' + str(fecha_efecto_pre[6:8])
            item['fecha_renovacion'] = str(year_fecha_efecto + 1) + '-' + str(fecha_efecto_pre[4:6]) + '-' + str(fecha_efecto_pre[6:8])
        # fecha_anulacion
        if index_exists(data, 18)==True:
            fecha_anulacion_pre = data[18]
            if fecha_anulacion_pre != "0":
                item['fecha_anulacion'] = str(fecha_anulacion_pre[0:4]) + '-' + str(fecha_anulacion_pre[4:6]) + '-' + str(fecha_anulacion_pre[6:8])
                if item['fecha_anulacion'] == '--':
                    item['fecha_anulacion'] = False
        # fecha_validez
        if index_exists(data, 19)==True:
            fecha_validez_pre = data[19]
            if fecha_validez_pre != "0":
                item['fecha_validez'] = str(fecha_validez_pre[0:4]) + '-' + str(fecha_validez_pre[4:6]) + '-' + str(fecha_validez_pre[6:8])
        #motivo_validez
        if index_exists(data, 20)==True:
            item['motivo_validez'] = int(str(data[20]))
        # riesgo_comercial
        if index_exists(data, 21)==True:
            item['riesgo_comercial'] = str(data[21].replace(',', '.'))
        # riesgo_politico
        if index_exists(data, 22)==True:
            item['riesgo_politico'] =str(data[22].replace(',', '.'))
        #avalistas
        if index_exists(data, 23)==True:
            item['avalistas'] = str(data[23])
        # cesce_risk_classification_motive_id
        if index_exists(data, 24)==True:
            cesce_risk_classification_motive_ids = self.custom_env['cesce.risk.classification.motive'].sudo().search([('code', '=', data[24])])
            if len(cesce_risk_classification_motive_ids) > 0:
                item['cesce_risk_classification_motive_id'] = cesce_risk_classification_motive_ids[0].id
        #codigo_deudor_interno
        if index_exists(data, 25)==True:
            item['codigo_deudor_interno'] = str(data[25])
        # operations codigo_deudor_interno (para calcular el partner_id)
        if item['codigo_deudor_interno']==False:
            _logger.info('No existe la posicion 25')
            _logger.info(data)
        else:
            if item['codigo_deudor_interno'] == "":
                res_partner_ids = self.custom_env['res.partner'].sudo().search(
                    [
                        ('active', '=', True),
                        ('customer', '=', True),
                        ('type', '=', 'contact'),
                        ('cesce_risk_state', '!=', 'none'),
                        ('vat', 'like', item['codigo_fiscal'])
                    ]
                )
                if len(res_partner_ids) > 0:
                    item['partner_id'] = res_partner_ids[0].id
            else:
                if len(str(item['codigo_deudor_interno'])) > 6:  # Fix no es un numero (es un NIF!!)
                    res_partner_ids = self.custom_env['res.partner'].sudo().search(
                        [
                            ('active', '=', True),
                            ('customer', '=', True),
                            ('type', '=', 'contact'),
                            ('vat', 'like', item['codigo_fiscal'])
                        ]
                    )
                    if len(res_partner_ids) > 0:
                        item['partner_id'] = res_partner_ids[0].id
        #return
        return item

    def partner_classification_item(self, data):
        if data['partner_id']==False:
            _logger.info('RARO, no hemos encontrado el ID de cliente')
            _logger.info(data)
        else:
            res_partner_ids = self.custom_env['res.partner'].sudo().search([('id', '=', data['partner_id'])])
            if len(res_partner_ids) == 0:
                _logger.info('RARO, no se encuentra el partner_id=' + str(data['partner_id']))
                _logger.info(data)
            else:
                res_partner_id_obj = res_partner_ids[0]
                _logger.info('Se actualiza la informacion desde CESCE respecto al partner_id=' + str(res_partner_id_obj.id))
                _logger.info(data)
                # operations
                if res_partner_id_obj.cesce_risk_state == 'classification_ok':
                    # cesce_risk_classification_id
                    cesce_risk_classification_ids = self.custom_env['cesce.risk.classification'].sudo().search([('partner_id', '=', res_partner_id_obj.id)])
                    if len(cesce_risk_classification_ids) > 0:
                        for cesce_risk_classification_id in cesce_risk_classification_ids:
                            cesce_risk_classification_id.importe_solicitado = data['importe_solicitado']
                            cesce_risk_classification_id.importe_concedido = data['importe_concedido']
                            cesce_risk_classification_id.fecha_efecto = data['fecha_efecto']
                            cesce_risk_classification_id.fecha_anulacion = data['fecha_anulacion']
                            cesce_risk_classification_id.fecha_renovacion = data['fecha_renovacion']
                            res_partner_id_obj.credit_limit = cesce_risk_classification_id.importe_concedido
                            # cesce_risk_state
                            if cesce_risk_classification_id.importe_concedido == 0:
                                res_partner_id_obj.cesce_risk_state = 'canceled_ok'
                            # tipo_movimiento
                            cesce_risk_classification_id.tipo_movimiento = data['tipo_movimiento']
                            # cesce_risk_classification_situation_id
                            if data['cesce_risk_classification_situation_id'] != False:
                                cesce_risk_classification_id.cesce_risk_classification_situation_id = data['cesce_risk_classification_situation_id']
                    elif res_partner_id_obj.cesce_risk_state == 'classification_sent':
                        # cesce_risk_clasification_vals
                        cesce_risk_clasification_vals = {
                            'partner_id': res_partner_id_obj.id,
                            'code_cesce': data['code_cesce'],
                            'num_sup_cesce': data['num_sup_cesce'],
                            'nombre_deudor': data['nombre_deudor'],
                            'codigo_fiscal': data['codigo_fiscal'],
                            'codigo_deudor_cesce': data['codigo_deudor_cesce'],
                            'grupo_riesgo_deudor': data['grupo_riesgo_deudor'],
                            'mercado': data['mercado'],
                            'pais_provincia': data['pais_provincia'],
                            'importe_solicitado': data['importe_solicitado'],
                            'importe_concedido': data['importe_concedido'],
                            'currency_id': data['currency_id'],
                            'plazo_solicitado': data['plazo_solicitado'],
                            'plazo_concedido': data['plazo_concedido'],
                            'condicion_pago': data['condicion_pago'],
                            'tipo_movimiento': data['tipo_movimiento'],
                            'cesce_risk_classification_situation_id': data['cesce_risk_classification_situation_id'],
                            'fecha_solicitud': data['fecha_solicitud'],
                            'fecha_efecto': data['fecha_efecto'],
                            'fecha_anulacion': data['fecha_anulacion'],
                            'fecha_validez': data['fecha_validez'],
                            'motivo_validez': data['motivo_validez'],
                            'riesgo_comercial': data['riesgo_comercial'],
                            'riesgo_politico': data['riesgo_politico'],
                            'avalistas': data['avalistas'],
                            'cesce_risk_classification_motive_id': data['cesce_risk_classification_motive_id'],
                            'codigo_deudor_interno': data['codigo_deudor_interno'],
                            'fecha_renovacion': data['fecha_renovacion']
                        }
                        cesce_risk_clasification_obj = self.custom_env['cesce.risk.classification'].sudo().create(cesce_risk_clasification_vals)
                        # check_partner and update
                        if cesce_risk_clasification_obj.partner_id.id > 0:
                            cesce_risk_clasification_obj.partner_id.credit_limit = cesce_risk_clasification_obj.importe_concedido
                            # cesce_risk_state
                            if cesce_risk_clasification_obj.partner_id.credit_limit > 0:
                                cesce_risk_clasification_obj.partner_id.cesce_risk_state = 'classification_ok'
                                cesce_risk_clasification_obj.cesce_error = ''
                            else:
                                cesce_risk_clasification_obj.partner_id.cesce_risk_state = 'canceled_ok'

    def partner_classifications_out_ftp(self):
        tmp_file = 'out_solicitudes_tmp.txt'
        return_files_in_folder = self.get_files_in_folder_ftp(self.ftp_folder_out, tmp_file)
        if len(return_files_in_folder)>0:
            for file_name, file_name_items_real in return_files_in_folder.items():
                _logger.info(self.ftp_folder_out)
                _logger.info(file_name)
                cesce_file_check_ids = self.custom_env['cesce.file.check'].search([('folder', '=', str(self.ftp_folder_out)), ('file', '=', str(file_name))])
                if len(cesce_file_check_ids) == 0:
                    # operations
                    if 'OUT_SOLICITUDES' in file_name:
                        for file_name_items in file_name_items_real:
                            data_item = self.partner_classification_item_define(file_name_items)#define normal object
                            self.partner_classification_item(data_item)#operations
                    #save cesce_file_check
                    cesce_file_check_vals = {
                        'folder': self.ftp_folder_out,
                        'file': file_name
                    }
                    cesce_file_check_obj = self.custom_env['cesce.file.check'].sudo().create(cesce_file_check_vals)
    
    #generate_partner_classification
    def generate_partner_classification(self, partner):
        if self.connection_risk_classification=='ftp':
           return self.generate_partner_classification_ftp(partner)
        else:
            return self.generate_partner_classification_webservice(partner) 
    
    def generate_partner_classification_webservice(self, partner):
        _logger.info('generate_partner_classification_webservice')
    
    def generate_partner_classification_ftp(self, partner):                                
        today = datetime.datetime.today()                    
        #provincia_estado
        provincia_estado = ''
        if partner.country_id.id>0 and partner.country_id.code!='ES':
            if partner.state_id.id>0:
                provincia_estado = str(partner.state_id.name[0:30])
        #cod_provincia
        cod_provincia = ''
        if partner.state_id.id>0:
            if partner.state_id.code in self.cod_provicnasi_esp:
                cod_provincia = str(self.cod_provicnasi_esp[partner.state_id.code])                    
        #fix_partner_vat
        partner_vat = partner.vat.upper()            
        #txt_fields
        txt_fields = [
            {
                'type': 'codigo_deudor_intero_compania',
                'value': str(partner.id),
                'value_test': str(partner.id),
                #'value_test': 'Valor cliente',
                'size': 50,
            },
            {
                'type': 'pais',
                'value': str(partner.country_id.code),
                'value_test': 'ES',
                'size': 2,
            },            
            {
                'type': 'nif',
                'value': str(partner_vat.replace('EU', '').replace(partner.country_id.code, '')),
                'value_test': '41980736D',
                'size': 9,
            },
            {
                'type': 'numero_duns',
                'value': '0',
                'value_test': '0',
                'size': 9,
            },
            {
                'type': 'nombre_deudor',
                'value': str(partner.name[0:60]),
                'value_test': 'INDUSTRIAS DE TEST',
                'size': 60,
            },
            {
                'type': 'domicilio',
                'value': str(partner.street[0:60]),
                'value_test': 'AVENIDA DE LA INDUSTRIA,1',
                'size': 60,
            },
            {
                'type': 'poblacion',
                'value': str(partner.city[0:30]),
                'value_test': 'MADRID',
                'size': 30,
            },
            {
                'type': 'codigo_postal',
                'value': str(partner.zip),
                'value_test': '28014',
                'size': 10,
            },
            {
                'type': 'cod_provincia',
                'value': str(cod_provincia),
                'value_test': '28',
                'size': 2,
            },
            {
                'type': 'provincia_estado',
                'value': str(provincia_estado),
                'value_test': '',
                'size': 30,
            },
            {
                'type': 'importe',
                'value': str(str(partner.cesce_amount_requested).replace('.', '')+'00'),
                'value_test': '100000000',
                'size': 14,
            },
            {
                'type': 'divisa',
                'value': str(partner.currency_id.name),
                'value_test': 'EUR',
                'size': 3,
            },
            {
                'type': 'plazo_pago',
                'value': '180',
                'value_test': '180',
                'size': 3,
            },
            {
                'type': 'cod_operacion_cesce',
                'value': str(self.modalidad)+str(self.poliza),
                'value_test': str(self.modalidad)+str(self.poliza),
                'size': 11,
            },
            {
                'type': 'ind_impagos',
                'value': 'N',
                'value_test': 'N',
                'size': 1,
            },
            {
                'type': 'imp_impagos',
                'value': '0',
                'value_test': '0',
                'size': 14,
            },
            {
                'type': 'ind_experiencia',
                'value': 'N',
                'value_test': 'N',
                'size': 1,
            },
            {
                'type': 'imp_experiencia',
                'value': '0',
                'value_test': '0',
                'size': 14,
            },
            {
                'type': 'cod_deudor_cesce',
                'value': '0',
                'value_test': '0',
                'size': 9,
            },
            {
                'type': 'num_suplemento_cesce',
                'value': '0',
                'value_test': '0',
                'size': 6,
            },
            {
                'type': 'observaciones',
                'value': '',
                'value_test': '',
                'size': 150,
            },                                                                                                                        
        ]
        
        txt_line = ''
        for txt_field in txt_fields:
            if self.test_mode==True:
                value_txt_field = txt_field['value_test']
            else:
                value_txt_field = txt_field['value']
                
            txt_line = txt_line + str(str(value_txt_field).ljust(txt_field['size'], ' '))+self.separator_fields                                        
                
        txt_line = txt_line[:-1]#fix remove last character
        txt_line = txt_line + '\r\n'#fix new line
        
        _logger.info(txt_line)
        #error prev
        response = {
            'errors': True, 
            'error': "", 
            'return': "",
        }                                
        #open file for reading
        file_name_real = "In_SOLICITUDES"+str(today.strftime('%d%m%Y%H%M'))+"_"+str(partner.id)+'.csv'                        
        file_name = os.path.dirname(os.path.abspath(__file__))+'/'+file_name_real                            
        #check if exists file
        line_exist_in_file = False
        if os.path.isfile(file_name):
            line_exist_in_file=True                                                                                        
        #continue line_exist_in_file
        if line_exist_in_file==False:
            fh = codecs.open(file_name, "a", "utf-8")
            fh.write(txt_line)
            fh.close()
        
            response_upload_file_ftp = self.upload_file_ftp(file_name, file_name_real, self.ftp_folder_in)#upload_file_ftp
            response['errors'] = response_upload_file_ftp['errors']
            response['error'] = response_upload_file_ftp['error']                                                  
        else:
            response = {
                'errors': True, 
                'error': "Ya existe este archivo .txt", 
                'return': "",
            }
        return response
    
    #cesce_sale_error        
    def cesce_sale_error(self):
        if self.connection_sale=='ftp':
            self.cesce_sale_error_ftp()
        else:
            self.cesce_sale_error_webservice()
        
    def cesce_sale_error_webservice(self):
        _logger.info('cesce_sale_error_webservice')
        
    def cesce_sale_error_ftp(self):
        _logger.info('cesce_sale_error_ftp')
        
        tmp_file = 'error_ventas_tmp.txt'
        return_files_in_folder = self.get_files_in_folder_ftp(self.ftp_folder_error, tmp_file)        
        if len(return_files_in_folder)>0:
            for file_name, file_name_items_real in return_files_in_folder.items():
                cesce_file_check_ids = self.custom_env['cesce.file.check'].search([('folder', '=', str(self.ftp_folder_error)), ('file', '=', str(file_name))])
                if len(cesce_file_check_ids) == 0:
                    # operations
                    if 'ERR_VENTAS' in file_name:
                        for file_name_items in file_name_items_real:
                            account_move_line_id_get = int(str(file_name_items[14]))
                            texto_error = file_name_items[13]

                            if account_move_line_id_get>0:
                                account_move_line_ids = self.custom_env['account.move.line'].search([('id', '=', account_move_line_id_get)])
                                if len(account_move_line_ids)==0:
                                    _logger.info('raro, no se encuentra el move_line_id='+str(account_move_line_ids))
                                else:
                                    account_move_line_id_obj = account_move_line_ids[0]
                                    if account_move_line_id_obj.cesce_sale_state=='sale_sent':
                                        account_move_line_id_obj.cesce_sale_state = 'sale_error'
                                    #cesce_error
                                    account_move_line_id_obj.cesce_error = texto_error
                    #save cesce_file_check
                    cesce_file_check_vals = {
                        'folder': self.ftp_folder_error,
                        'file': file_name
                    }
                    cesce_file_check_obj = self.custom_env['cesce.file.check'].sudo().create(cesce_file_check_vals)
        
    #cesce_sale_out
    def cesce_sale_out(self):
        _logger.info('cesce_sale_out')
        
        if self.connection_sale=='ftp':
            self.cesce_sale_out_ftp()
        else:
            self.cesce_sale_out_webservice()
        
    def cesce_sale_out_webservice(self):
        _logger.info('cesce_sale_out_webservice')
        
    def cesce_sale_out_ftp(self):
        tmp_file = 'out_ventas_tmp.txt'
        return_files_in_folder = self.get_files_in_folder_ftp(self.ftp_folder_out, tmp_file)        
        if len(return_files_in_folder)>0:
            for file_name, file_name_items_real in return_files_in_folder.items():
                cesce_file_check_ids = self.custom_env['cesce.file.check'].search([('folder', '=', str(self.ftp_folder_out)), ('file', '=', str(file_name))])
                if len(cesce_file_check_ids) == 0:
                    # operations
                    if 'OUT_VENTAS' in file_name:
                        for file_name_items in file_name_items_real:
                            if index_exists(file_name_items, 23):
                                file_name_pos_23 = str(file_name_items[23]).strip()
                                if file_name_pos_23=='':
                                    _logger.info('raro, no esta la posicion 23, no viene de Odoo')
                                else:
                                    account_move_line_id_get = int(file_name_pos_23)
                                    if account_move_line_id_get>0:
                                        account_move_line_ids = self.custom_env['account.move.line'].search([('id', '=', account_move_line_id_get)])
                                        if len(account_move_line_ids)==0:
                                            _logger.info('raro, no se encuentra el move_line_id='+str(account_move_line_id_get))
                                        else:
                                            account_move_line_id_obj = account_move_line_ids[0]
                                            if account_move_line_id_obj.cesce_sale_state=='sale_sent':
                                                #nif_filial
                                                nif_filial = file_name_items[1].replace(' ', '').strip()
                                                #fecha_movimiento
                                                fecha_movimiento_pre = file_name_items[3]
                                                fecha_movimiento = str(fecha_movimiento_pre[0:4])+'-'+str(fecha_movimiento_pre[4:6])+'-'+str(fecha_movimiento_pre[6:8])
                                                #nif_deudor
                                                nif_deudor = file_name_items[5].replace(' ', '').strip()
                                                #fecha_factura
                                                fecha_factura_pre = file_name_items[8]
                                                fecha_factura = str(fecha_factura_pre[0:4])+'-'+str(fecha_factura_pre[4:6])+'-'+str(fecha_factura_pre[6:8])
                                                #fecha_vencimiento
                                                fecha_vencimiento_pre = file_name_items[9]
                                                fecha_vencimiento = str(fecha_vencimiento_pre[0:4])+'-'+str(fecha_vencimiento_pre[4:6])+'-'+str(fecha_vencimiento_pre[6:8])
                                                #cesce_sale_situation_id
                                                cesce_sale_situation_id = False
                                                cesce_sale_situation_ids = self.custom_env['cesce.sale.situation'].search([('code', '=', int(file_name_items[12]))])
                                                if len(cesce_sale_situation_ids)>0:
                                                    cesce_sale_situation_id_obj = cesce_sale_situation_ids[0]
                                                    cesce_sale_situation_id = cesce_sale_situation_id_obj.id
                                                #cesce_sale_motive_situation_id
                                                cesce_sale_motive_situation_id = False
                                                cesce_sale_motive_situation_ids = self.custom_env['cesce.sale.motive.situation'].search([('code', '=', int(file_name_items[13]))])
                                                if len(cesce_sale_motive_situation_ids)>0:
                                                    cesce_sale_motive_situation_id_obj = cesce_sale_motive_situation_ids[0]
                                                cesce_sale_motive_situation_id = cesce_sale_motive_situation_id_obj.id
                                                #currency_id
                                                currency_id = 1
                                                res_currency_ids = self.custom_env['res.currency'].search([('name', '=', str(file_name_items[20]))])
                                                if len(res_currency_ids)>0:
                                                    res_currency_id_obj = res_currency_ids[0]
                                                    currency_id = res_currency_id_obj.id
                                                #nif_cedente
                                                nif_cedente = file_name_items[21].replace(' ', '').strip()
                                                #fecha_adquisicion
                                                fecha_adquisicion_pre = file_name_items[22]
                                                fecha_adquisicion = str(fecha_adquisicion_pre[0:4])+'-'+str(fecha_adquisicion_pre[4:6])+'-'+str(fecha_adquisicion_pre[6:8])
                                                if fecha_adquisicion=='0000-00-00':
                                                    fecha_adquisicion = False
                                                #vals
                                                cesce_sale_vals = {
                                                    'account_move_line_id': account_move_line_id_get,
                                                    'nif_filial': str(nif_filial),
                                                    'numero_interno_factura': str(file_name_items[2]),
                                                    'fecha_movimiento': fecha_movimiento,
                                                    'num_sumplemento_cesce': str(file_name_items[4]),
                                                    'nif_deudor': str(nif_deudor),
                                                    'codigo_deudor_cesce': str(file_name_items[6]),
                                                    #'partner_id': file_name_items[7],
                                                    'partner_id': account_move_line_id_obj.partner_id.id,
                                                    'fecha_factura': fecha_factura,
                                                    'fecha_vencimiento': fecha_vencimiento,
                                                    'importe_credito': str(file_name_items[10]),
                                                    #'account_invoice_id': file_name_items[11],
                                                    'account_invoice_id': account_move_line_id_obj.invoice_id.id,
                                                    'cesce_sale_situation_id': cesce_sale_situation_id,
                                                    'cesce_sale_motive_situation_id': cesce_sale_motive_situation_id,
                                                    'percent_riesgo_comercial': str(file_name_items[14]),
                                                    'percent_tasa_rrcc': str(file_name_items[15]),
                                                    'prima_rrcc': str(file_name_items[16]),
                                                    'percent_riesgo_politico': str(file_name_items[17]),
                                                    'percent_tasa_rrpp': str(file_name_items[18]),
                                                    'prima_rrpp': str(file_name_items[19]),
                                                    'currency_id': currency_id,
                                                    'nif_cedente': str(nif_cedente),
                                                    'fecha_adquisicion': fecha_adquisicion,
                                                    'id_interno_factura_cliente': str(file_name_items[23]),
                                                }
                                                cesce_sale_obj = self.custom_env['cesce.sale'].sudo().create(cesce_sale_vals)
                                                #check_account_move_line and update
                                                if cesce_sale_obj.account_move_line_id.id>0:
                                                    cesce_sale_obj.account_move_line_id.cesce_sale_state = 'sale_ok'
                    #save cesce_file_check
                    cesce_file_check_vals = {
                        'folder': self.ftp_folder_out,
                        'file': file_name
                    }
                    cesce_file_check_obj = self.custom_env['cesce.file.check'].sudo().create(cesce_file_check_vals)
    
    #generate_cesce_sale        
    def generate_cesce_sale(self, account_move_line):
        if self.connection_sale=='ftp':
            return self.generate_cesce_sale_ftp(account_move_line)
        else:
            return self.generate_cesce_sale_webservice(account_move_line)
        
    def generate_cesce_sale_webservice(self, account_move_line):
        _logger.info('generate_cesce_sale_webservice')
        
    def generate_cesce_sale_ftp(self, account_move_line):
        today = datetime.datetime.today()
        #fecha_factura
        date_invoice_slit = account_move_line.invoice_id.date_invoice.split("-")
        fecha_factura = date_invoice_slit[0]+date_invoice_slit[1]+date_invoice_slit[2]                  
        #fecha_vencimiento
        date_maturity_slit = account_move_line.date_maturity.split("-")
        fecha_vencimiento = date_maturity_slit[0]+date_maturity_slit[1]+date_maturity_slit[2]              
        #partner_vat
        partner_vat = account_move_line.partner_id.vat.upper()
        
        txt_fields = [
            {
                'type': 'codigo_operacion_cesce',
                'value': str(self.modalidad)+str(self.poliza),
                'value_test': str(self.modalidad)+str(self.poliza),
                'size': 11,
            },
            {
                'type': 'nif_filial',
                'value': '',
                'value_test': '0',
                'size': 20,
            },
            {
                'type': 'num_suplemento_cesce',
                'value': '0',
                'value_test': '1',
                'size': 6,
            },
            {
                'type': 'nif_deudor',
                'value': str(partner_vat.replace('EU', '').replace(account_move_line.partner_id.country_id.code, '')),
                'value_test': '62261643E',
                'size': 20,
            },
            {
                'type': 'codigo_deudor_cesce',
                'value': '',
                'value_test': '0',
                'size': 9,
            },
            {
                'type': 'codigo_deudor_interno_compania',
                'value': str(account_move_line.partner_id.id),
                'value_test': '0',
                'size': 50,
            },
            {
                'type': 'fecha_factura',
                'value': str(fecha_factura),
                'value_test': '20170101',
                'size': 8,
            },
            {
                'type': 'fecha_vencimiento',
                'value': str(fecha_vencimiento),
                'value_test': '20170301',
                'size': 8,
            },
            {
                'type': 'codigo_divisa_iso',
                'value': str(account_move_line.invoice_id.currency_id.name),
                'value_test': 'EUR',
                'size': 3,
            },
            {
                'type': 'importe_credito',
                'value': str(str(account_move_line.debit).replace('.', ''))+'0',                
                'value_test': '26828100',
                'size': 18,
            },
            {
                'type': 'codigo_factura',
                'value': str(account_move_line.invoice_id.number),
                'value_test': 'FA001',
                'size': 15,
            },
            {
                'type': 'nif_cedente',
                'value': '',
                'value_test': '0',
                'size': 20,
            },
            {
                'type': 'fecha_adquisicion',
                'value': '',
                'value_test': '',
                'size': 8,
            },
            {
                'type': 'id_interno_factura_cliente',
                'value': str(account_move_line.id),
                'value_test': str(account_move_line.id),
                'size': 30,
            },
        ]
        
        txt_line = ''
        for txt_field in txt_fields:
            if self.test_mode==True:
                value_txt_field = txt_field['value_test']
            else:
                value_txt_field = txt_field['value']
                
            txt_line = txt_line + str(str(value_txt_field).ljust(txt_field['size'], ' '))+self.separator_fields                                        
                
        txt_line = txt_line[:-1]#fix remove last character
        txt_line = txt_line + '\r\n'#fix new line
        
        _logger.info(txt_line)
        #error prev
        response = {
            'errors': True, 
            'error': "", 
            'return': "",
        }                                
        #open file for reading
        file_name_real = "In_VENTAS"+str(today.strftime('%d%m%Y%H%M'))+"_"+str(account_move_line.id)+'.csv'                        
        file_name = os.path.dirname(os.path.abspath(__file__))+'/'+file_name_real                                    
        #check if exists line
        line_exist_in_file = False
        if os.path.isfile(file_name):
            line_exist_in_file=True                        
        #continue line_exist_in_file
        if line_exist_in_file==False:
            fh = codecs.open(file_name, "a", "utf-8")
            fh.write(txt_line)
            fh.close()
        
            response_upload_file_ftp = self.upload_file_ftp(file_name, file_name_real, self.ftp_folder_in)#upload_file_ftp
            response['errors'] = response_upload_file_ftp['errors']
            response['error'] = response_upload_file_ftp['error']                                                  
        else:
            response = {
                'errors': True, 
                'error': "Ya existe este archivo .txt", 
                'return': "",
            }
        return response
                                                                                                                                                            