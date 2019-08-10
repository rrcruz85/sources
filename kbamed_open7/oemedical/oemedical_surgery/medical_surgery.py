# coding=utf-8
from osv import fields, osv


class surgery (osv.osv):
	_name = "oemedical.surgery"
	_description = "Surgery"
	_columns = {
		'name' : fields.many2one ('oemedical.procedure','Code', help="Procedure Code, for example ICD-10-PCS Code 7-character string"),
		'patient_id' : fields.many2one ('oemedical.patient','Patient', required=True),
		'pathology' : fields.many2one ('oemedical.pathology','Base condition', help="Base Condition / Reason"),
		'classification' : fields.selection ([
				('o','Optional'),
				('r','Required'),
				('u','Urgent')], 'Surgery Classification', select=True),
		'surgeon' : fields.many2one('oemedical.physician','Surgeon', help="Surgeon who did the procedure"),
		'date': fields.datetime ('Date of the surgery'),
		'description' : fields.char ('Description', size=128),
		'extra_info' : fields.text ('Extra Info'),
	}

surgery ()

class medical_patient (osv.osv):
	_name = "oemedical.patient"
	_inherit = "oemedical.patient"
	_columns = {
		'surgery' : fields.one2many('oemedical.surgery', 'patient_id','Surgeries'),
	}

medical_patient ()




