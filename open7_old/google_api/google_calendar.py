# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _

import argparse
import httplib2
from googleapiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools

import dateutil.parser
import pytz
import logging
import os
import base64
import time
from datetime import timedelta
import datetime
import sys

logger = logging.getLogger('google_api')

class crm_meeting(osv.osv):

    _name = 'crm.meeting'
    _inherit = 'crm.meeting'
    _columns = {
        'google_event_id': fields.char('Google Calendar Event ID'),
        'google_sequence': fields.integer('Sequence for update'),
    }

    _defaults = {
        'google_event_id': False,
        'google_sequence': 0,
    }
    
    def get_credential_dat_file(self, cr, uid, userId):
        path = os.path.dirname(os.path.abspath(__file__)) 
        if os.name == 'nt':
            path += '\\data\\keys\\'
        else:
            path += '/data/keys/'  
            
        instance_pool = self.pool.get('google.api.calendar')
        instance = instance_pool.search(cr, uid, [('user_id', '=', userId)])
        instance = instance_pool.browse(cr, uid, instance[0])          
        account_name = instance.account_id.name.lower().replace (' ','_')
        file_secret_path =  path + account_name + '_credential.dat'
        
        if not os.path.exists(file_secret_path):
            data = instance.account_id.credential_file
            f = open(file_secret_path,'wb')
            f.write(data.decode('base64'))
            f.close()
        return file_secret_path
    
    def create(self, cr, uid, vals, context=None):

        if context is None:
            context = {}

        if context.get('stop_google_calendar_sync', False):
            event_id = super(crm_meeting, self).create(cr, uid, vals, context)
            return event_id

        instance_pool = self.pool.get('google.api.calendar')
        instance = False
        
        if vals.get('user_id', False):
            instance = instance_pool.search(cr, uid, [('user_id', '=', vals['user_id'])])
        if not instance:
            event_id = super(crm_meeting, self).create(cr, uid, vals, context)
            return event_id

        instance = instance_pool.browse(cr, uid, instance[0])
        try:
            credential_dat_file = self.get_credential_dat_file(cr, uid, vals['user_id'])            
            storage = file.Storage(credential_dat_file)
            credentials = storage.get()
            http = httplib2.Http()
            http = credentials.authorize(http)
            service = discovery.build('calendar', 'v3', http=http, cache_discovery=False)

            start_utc = dateutil.parser.parse(vals['date'])
            end_utc = dateutil.parser.parse(vals['date_deadline'])
            if vals.get('allday', False):
                tz = pytz.timezone(instance.user_id.tz) if instance.user_id.tz else pytz.utc
                start = pytz.utc.localize(start_utc).astimezone(tz)     # convert start in user's timezone
                end = pytz.utc.localize(end_utc).astimezone(tz)         # convert end in user's timezone
                new_event = {
                            'summary': vals['name'],
                            'description': vals.get('description', ''),
                            'location': vals.get('location', ''),
                            'start': {'date': start.strftime('%Y-%m-%d'), },
                            'end': {'date': end.strftime('%Y-%m-%d'), },
                            }
            else:
                new_event = {'summary': vals['name'],
                             'description': vals.get('description', ''),
                             'location': vals.get('location', ''),
                             'start': {'dateTime': start_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')},
                             'end': {'dateTime': end_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z'), },
                        }
            new_event = service.events().insert(calendarId=instance.calendar_id, body=new_event, sendNotifications=False).execute()
            vals['google_event_id'] = new_event['id']
        except:
            vals['google_event_id'] = False
            logger.error('Insert google calendar event failed in create method for crm_meeting.')

        event_id = super(crm_meeting, self).create(cr, uid, vals, context)
        return event_id

    def write(self, cr, uid, ids, vals, context=None):

        if context is None:
            context = {}

        if not ids:
            return True

        if isinstance(ids, (int, long)):
            ids = [ids]

        if context.get('stop_google_calendar_sync', False):
            res = super(crm_meeting, self).write(cr, uid, ids, vals, context=context)
            return res

        for event_id in ids:
            # try to sync these events with google calendar
            if any(k in vals for k in ['name', 'description', 'location', 'date', 'date_deadline']):
                google_sequence = self.read(cr, uid, event_id, ['google_sequence'])['google_sequence']
                vals['google_sequence'] = google_sequence + 1
                super(crm_meeting, self).write(cr, uid, event_id, vals, context=context)

                event = self.browse(cr, uid, event_id)
                if event.google_event_id and event.user_id:
                    instance_pool = self.pool.get('google.api.calendar')
                    instance = instance_pool.search(cr, uid, [('user_id', '=', event.user_id.id)])
                    if instance:
                        instance = instance_pool.browse(cr, uid, instance[0])
                        try:
                            credential_dat_file = self.get_credential_dat_file(cr, uid, event.user_id.id)            
                            storage = file.Storage(credential_dat_file) 
                            credentials = storage.get()
                            http = httplib2.Http()
                            http = credentials.authorize(http)
                            service = discovery.build('calendar', 'v3', http=http,cache_discovery=False)

                            start_utc = dateutil.parser.parse(event.date)
                            end_utc = dateutil.parser.parse(event.date_deadline)
                            if event.allday:
                                tz = pytz.timezone(instance.user_id.tz) if instance.user_id.tz else pytz.utc
                                start = pytz.utc.localize(start_utc).astimezone(tz)     # convert start in user's timezone
                                end = pytz.utc.localize(end_utc).astimezone(tz)         # convert end in user's timezone
                                upd_event = {
                                            'summary': event.name,
                                            'description': event.description if event.description else '',
                                            'location': event.location,
                                            'start': {'date': start.strftime('%Y-%m-%d'), },
                                            'end': {'date': end.strftime('%Y-%m-%d'), },
                                            'sequence': event.google_sequence,
                                            }
                            else:
                                upd_event = {'summary': event.name,
                                             'description': event.description if event.description else '',
                                             'location': event.location,
                                             'start': {'dateTime': start_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')},
                                             'end': {'dateTime': end_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z'), },
                                             'sequence': event.google_sequence,
                                            }

                            service.events().update(calendarId=instance.calendar_id, eventId=event.google_event_id, body=upd_event, sendNotifications=False).execute()
                        except:
                            logger.error('Update google calendar event failed for id [%s] .' % (event.google_event_id))
            else:
                super(crm_meeting, self).write(cr, uid, event_id, vals, context=context)

        return True

    def unlink(self, cr, uid, ids, context=None):

        if context == None:
            context = {}

        if context.get('stop_google_calendar_sync', False):
            return osv.osv.unlink(self, cr, uid, ids, context=context)

        del_pool = self.pool.get('crm.meeting.deleted')

        geventids = self.read(cr, uid, ids, ['google_event_id', 'user_id'], context=context)
        for event_id in geventids:
            if event_id['google_event_id'] and event_id['user_id']:

                instance_pool = self.pool.get('google.api.calendar')
                instance = instance_pool.search(cr, uid, [('user_id', '=', event_id['user_id'][0])])
                if instance:
                    instance = instance_pool.browse(cr, uid, instance[0])
                    try:
                        credential_dat_file = self.get_credential_dat_file(cr, uid, event_id['user_id'][0])            
                        storage = file.Storage(credential_dat_file)
                        credentials = storage.get()
                        http = httplib2.Http()
                        http = credentials.authorize(http)
                        service = discovery.build('calendar', 'v3', http=http,cache_discovery=False)
                        service.events().delete(calendarId=instance.calendar_id, eventId=event_id['google_event_id']).execute()
                    except:
                        vals = {'google_event_id': event_id['google_event_id'],
                                'user_id': event_id['user_id'][0]}
                        del_pool.create(cr, uid, vals)

        return osv.osv.unlink(self, cr, uid, ids, context=context)
    
    def test(self, cr, uid, ids, context=None):
        print 'test'

class crm_meeting_deleted(osv.osv):

    _name = 'crm.meeting.deleted'
    _columns = {
        'google_event_id': fields.char('Google Calendar Event ID'),
        'user_id': fields.many2one('res.users', 'User'),
    }

class google_api_account(osv.osv):

    _name = 'google.api.account'
    _columns = {
        'name': fields.char('Account', size=50, required=True),
        'secrets_file':fields.binary('Secrets File', required=True, filters='*.json,*.JSON', help ='Must be the credential.json file generated from google api'),
        'credential_file':fields.binary('Credential File', help ='Must be the credential.dat file generated after executing Syncronize Button'),
        'synchronize': fields.boolean('Auto synchronize'),
        'use_local_browser': fields.boolean('Use local browser', help="""
        If you can not run a local browser on the machine where OpenERP-Server is running on, please deactivate this option. For getting authorized you must start OpenERP-Server in interactive mode (on ubuntu from the location where you installed OpenERP-Server: ./openerp-server -c /etc/openerp-server.conf).
        After clicking on 'Authorize' you willbe asked to enter a verification code."""),
    }

    _defaults = {
        'synchronize': True,
        'use_local_browser': True,
    }
    
    def do_authorize(self, cr, uid, ids, context=None):
        
        try:
            if not context:
                context = {}
            
            account = self.browse(cr, uid, ids[0])        
            path = os.path.dirname(os.path.abspath(__file__))        
            if os.name == 'nt':
                path += '\\data\\keys\\'
            else:
                path += '/data/keys/'            
            
            account_name = account.name.lower().replace (' ','_')                    
            file_secret_path =  path + account_name + '_credential.json'
            
            if not os.path.exists(file_secret_path):
                with open(file_secret_path, 'wb') as dat_file:
                    data = account.secrets_file
                    dat_file.write(data.decode('base64'))
            
            FLOW = client.flow_from_clientsecrets(file_secret_path,
                                                  scope=[
                                                         'https://www.googleapis.com/auth/calendar',
                                                         'https://www.googleapis.com/auth/calendar.readonly',
                                                         'https://www.google.com/m8/feeds',
                                                        ],
                                                  message=tools.message_if_missing(file_secret_path))
            
            file_credential_path =  path + account_name + '_credential.dat'
            
            if account.credential_file and not os.path.exists(file_credential_path):            
                data = account.credential_file
                with open(file_credential_path, 'wb') as dat_file:
                    dat_file.write(data.decode('base64'))
                     
            storage = file.Storage(file_credential_path)
            credentials = storage.get()
            if credentials is None or credentials.invalid:
                parser = argparse.ArgumentParser(
                            description=__doc__,
                            formatter_class=argparse.RawDescriptionHelpFormatter,
                            parents=[tools.argparser])
                if not account.use_local_browser:
                    flags = parser.parse_args(['--noauth_local_webserver'])
                else:
                    flags = parser.parse_args([])
                
                credentials = tools.run_flow(FLOW, storage, flags)
                    
                with open(file_credential_path, 'r') as dat_file:
                    content = dat_file.read()
                    base64String = base64.b64encode(bytes(content))
                    self.write(cr, uid, ids,{'credential_file':base64String}) 
        
        except Exception as exc:
            logger.error(_('Authorize failed. %s' % (exc.value,)))
        
        #raise osv.except_osv(_('Done.'), _('Please verify if your credential file is created or updated in the path the you selected for the secret path folder.'))

class google_api_calendar(osv.osv):

    _name = 'google.api.calendar'
    _columns = {
        'account_id': fields.many2one('google.api.account', 'Account', required=True),
        'user_id': fields.many2one('res.users', 'User', required=True),
        'calendar_id': fields.char('Google calendar id', size=100, required=True, readonly = True),
        'last_update_synchronize_date': fields.datetime(string = 'Last Update Synchronization Date'),
        'update_synchronize_date_every': fields.integer(string = 'Update Synchronize Date Every', help = "Update the Synchronization Date Every x Days set by in this field"),        
    }

    _defaults = {
        'calendar_id'  : 'primary',
        'last_update_synchronize_date' : lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'update_synchronize_date_every' : 3
    }

    _sql_constraints = [
        ('pu-key-1', 'UNIQUE (user_id)', 'User already assigned to a google calendar!'),
        ('pu-key-2', 'UNIQUE (calendar_id)', 'Google calendar already assigned to another user!'),
    ]

    def do_synchronize(self, cr, uid, ids, context=None):

        instance = self.browse(cr, uid, ids[0])
        limit_date = context.get('limit_date',  instance.last_update_synchronize_date or time.strftime('%Y-%m-%d %H:%M:%S'))
        meeting_pool = self.pool.get('crm.meeting')
        del_pool = self.pool.get('crm.meeting.deleted')
             
        path = os.path.dirname(os.path.abspath(__file__))        
        if os.name == 'nt':
            path += '\\data\\keys\\'
        else:
            path += '/data/keys/'   
            
        account_name = instance.account_id.name.lower().replace (' ','_')
                
        file_credential_path =  path + account_name + '_credential.dat'       

        try:
            storage = file.Storage(file_credential_path)
            credentials = storage.get()
            http = httplib2.Http()
            http = credentials.authorize(http)
        except:
            raise osv.except_osv(_('Authorize failed'), _('The credentials have been revoked or expired, please authorize your account.'))


        # Construct the service object for the interacting with the Calendar API.
        service = discovery.build('calendar', 'v3', http=http, cache_discovery=False)

        # build a list with all google-events-id present in crm_meeting for this user
        google_event_ids = meeting_pool.search(cr, uid, [('date','>=',limit_date),('user_id', '=', instance.user_id.id), ('google_event_id', '!=', False)])
        data = meeting_pool.read(cr, uid, google_event_ids, ['google_event_id'])
        google_event_ids = []
        for item in data:
            google_event_ids.append(item['google_event_id'])

        # first sync events from google with crm_meeting                                                        
        page_token = None
        while True:                        
            tmin =  datetime.datetime.strptime(limit_date, '%Y-%m-%d %H:%M:%S').isoformat('T') + "Z"
            tmax =  datetime.datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S').isoformat('T') + "Z"
            
            events = service.events().list(calendarId=instance.calendar_id, timeMin = tmin, timeMax = tmax ,pageToken=page_token).execute()
            for event in events['items']:
                is_deleted = del_pool.search(cr, uid, [('user_id', '=', instance.user_id.id), ('google_event_id', '=', event['id'])])
                if not is_deleted:
                    # check if google event already in openerp
                    crm_meeting = meeting_pool.search(cr, uid, [('date','>=',limit_date),('user_id', '=', instance.user_id.id), ('google_event_id', '=', event['id'])])
                    if crm_meeting:
                        if event.get('updated', False):
                            updated_google = dateutil.parser.parse(event['updated']).astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
                            updated_oe = meeting_pool.read(cr, uid, crm_meeting[0], ['write_date'])
                            updated_oe = dateutil.parser.parse(updated_oe['write_date']).strftime('%Y-%m-%d %H:%M:%S')

                            # in this case do nothing, everything is synchronized
                            if updated_google == updated_oe:
                                if event['id'] in google_event_ids:
                                    google_event_ids.remove(event['id'])
                                continue

                            if updated_google < updated_oe: # check if we have to overwrite google with data from crm_meeting
                                updated_event = meeting_pool.browse(cr, uid, crm_meeting[0])
                                start_utc = dateutil.parser.parse(updated_event.date)
                                end_utc = dateutil.parser.parse(updated_event.date_deadline)
                                if updated_event.allday:
                                    tz = pytz.timezone(instance.user_id.tz) if instance.user_id.tz else pytz.utc
                                    start = pytz.utc.localize(start_utc).astimezone(tz)     # convert start in user's timezone
                                    end = pytz.utc.localize(end_utc).astimezone(tz)         # convert end in user's timezone
                                    event = {
                                             'summary': updated_event.name,
                                             'description': updated_event.description if updated_event.description else '',
                                             'location': updated_event.location,
                                             'start': {
                                                       'date': start.strftime('%Y-%m-%d'),
                                                       },
                                             'end': {
                                                     'date': end.strftime('%Y-%m-%d'),
                                                     },
                                             'sequence': updated_event.google_sequence,
                                             }
                                else:
                                    event = {
                                             'summary': updated_event.name,
                                             'description': updated_event.description if updated_event.description else '',
                                             'location': updated_event.location,
                                             'start': {
                                                       'dateTime': start_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                                                       },
                                             'end': {
                                                     'dateTime': end_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                                                     },
                                             'sequence': updated_event.google_sequence,
                                             }

                                try:
                                    service.events().update(calendarId=instance.calendar_id, eventId=updated_event.google_event_id, body=event, sendNotifications=False).execute()
                                except:
                                    logger.error('Update google calendar event failed for id [%s] .' % (updated_event.google_event_id))

                                meeting_pool.write(cr, uid, updated_event.id, {'google_sequence': updated_event.google_sequence + 1}, context={'stop_google_calendar_sync': 'True'})
                                if updated_event.google_event_id in google_event_ids:
                                    google_event_ids.remove(updated_event.google_event_id)

                                continue

                    # convert dateTime to utc
                    # skip events from google calendar when not all fields are present
                    if not ('start' in event and 'end' in event):
                        logger.error('skipped event from google calendar due to missing fields. Event: %s' % (str(event)))
                        continue

                    start = event['start']
                    end = event['end']
                    if 'dateTime' in start:
                        start_utc = dateutil.parser.parse(start['dateTime']).astimezone(pytz.utc)
                        end_utc = dateutil.parser.parse(end['dateTime']).astimezone(pytz.utc)
                        diff = end_utc - start_utc
                        duration = round(float(diff.days) * 24 + (float(diff.seconds) / 3600), 2)
                        allday = False
                    elif 'date'in start:
                        tz = pytz.timezone(instance.user_id.tz) if instance.user_id.tz else pytz.utc

                        start_utc = dateutil.parser.parse(start['date'])
                        start_utc = pytz.utc.localize(start_utc).astimezone(tz)
                        start_utc = start_utc.replace(hour=0, minute=0, second=0)   # change start's time to 00:00:00                        

                        end_utc = dateutil.parser.parse(end['date'])
                        end_utc = pytz.utc.localize(end_utc).astimezone(tz)
                        end_utc = end_utc.replace(hour=0, minute=0, second=0)   # change start's time to 00:00:00

                        diff = end_utc - start_utc
                        duration = round(float(diff.days) * 24 + (float(diff.seconds) / 3600), 2)
                        allday = True

                        start_utc = start_utc.astimezone(pytz.utc)                  # convert start back to utc                                          
                        end_utc = end_utc.astimezone(pytz.utc)                      # convert end back to utc


                    if crm_meeting:
                        if event.get('updated', False):
                            updated_google = dateutil.parser.parse(event['updated']).astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
                            updated_oe = meeting_pool.read(cr, uid, crm_meeting[0], ['write_date'])
                            updated_oe = dateutil.parser.parse(updated_oe['write_date']).strftime('%Y-%m-%d %H:%M:%S')

                            if updated_google > updated_oe:  # overwrite crm_meeting with data from google                                                                                                                                       
                                meeting_pool.write(cr, uid, crm_meeting, {'name': event.get('summary', ''),
                                                                          'description': event.get('description', ''),
                                                                          'date': start_utc.strftime('%Y-%m-%d %H:%M:%S'),
                                                                          'date_deadline': end_utc.strftime('%Y-%m-%d %H:%M:%S'),
                                                                          'duration': duration,
                                                                          'allday': allday,
                                                                          'location': event.get('location', '')}, context={'stop_google_calendar_sync': 'True'})
                        else:
                            meeting_pool.write(cr, uid, crm_meeting, {'name': event.get('summary', ''),
                                                                      'description': event.get('description'),
                                                                      'date': start_utc.strftime('%Y-%m-%d %H:%M:%S'),
                                                                      'date_deadline': end_utc.strftime('%Y-%m-%d %H:%M:%S'),
                                                                      'duration': duration,
                                                                      'allday': allday,
                                                                      'location': event.get('location', '')}, context={'stop_google_calendar_sync': 'True'})
                    else:
                        meeting_pool.create(cr, uid, {'user_id': instance.user_id.id,
                                                      'name': event.get('summary', ''),
                                                      'description': event.get('description'),
                                                      'date': start_utc.strftime('%Y-%m-%d %H:%M:%S'),
                                                      'date_deadline': end_utc.strftime('%Y-%m-%d %H:%M:%S'),
                                                      'duration': duration,
                                                      'allday': allday,
                                                      'location': event.get('location', ''),
                                                      'google_event_id': event['id']}, context={'stop_google_calendar_sync': 'True'})
                    if event['id'] in google_event_ids:
                        google_event_ids.remove(event['id'])
            page_token = events.get('nextPageToken')
            if not page_token:
                break

        # now sync new crm_meetings with google
        new_events = meeting_pool.search(cr, uid, [('date','>=',limit_date),('user_id', '=', instance.user_id.id), ('google_event_id', '=', False)])
        for new_event in meeting_pool.browse(cr, uid, new_events):
            start_utc = dateutil.parser.parse(new_event.date)
            end_utc = dateutil.parser.parse(new_event.date_deadline)
            if new_event.allday:
                tz = pytz.timezone(instance.user_id.tz) if instance.user_id.tz else pytz.utc
                start = pytz.utc.localize(start_utc).astimezone(tz)     # convert start in user's timezone
                end = pytz.utc.localize(end_utc).astimezone(tz)         # convert end in user's timezone
                event = {
                         'summary': new_event.name,
                         'description': new_event.description if new_event.description else '',
                         'location': new_event.location,
                         'start': {
                                   'date': start.strftime('%Y-%m-%d'),
                                   },
                         'end': {
                                 'date': end.strftime('%Y-%m-%d'),
                                 },
                         }
            else:
                event = {
                         'summary': new_event.name,
                         'description': new_event.description if new_event.description else '',
                         'location': new_event.location,
                         'start': {
                                   'dateTime': start_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                                   },
                         'end': {
                                 'dateTime': end_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                                 },
                         }

            try:
                google_new_event = service.events().insert(calendarId=instance.calendar_id, body=event, sendNotifications=False).execute()
            except:
                logger.error('Insert google calendar event failed for crm_meeting id [%d] .' % (new_event.id))
                google_new_event = False

            if google_new_event:
                meeting_pool.write(cr, uid, new_event.id, {'google_event_id': google_new_event['id']})

        # delete events in google calendar which were deleted in OpenERP for this user
        delids = del_pool.search(cr, uid, [('user_id', '=', instance.user_id.id)])
        for del_event in del_pool.browse(cr, uid, delids):
            try:
                service.events().delete(calendarId=instance.calendar_id, eventId=del_event.google_event_id).execute()
            except:
                # handle it
                logger.error('Delete google calendar event failed for id [%s] .' % (del_event.google_event_id))
        del_pool.unlink(cr, uid, delids)

        # now delete all events from crm_meeting which were not updated and/or created by google calendar, this ones are deleted in google calendar    
        for gid in google_event_ids:
            delids = meeting_pool.search(cr, uid, [('date','>=',limit_date),('user_id', '=', instance.user_id.id), ('google_event_id', '=', gid)])
            meeting_pool.unlink(cr, uid, delids, context={'stop_google_calendar_sync': 'True'})

        context["calendar_default_user_id"] = uid
        
        return {
            'name': 'Meetings',
            'view_type': 'form',
            'view_mode': 'calendar,tree,form,gantt',
            'res_model': 'crm.meeting',
            'type': 'ir.actions.act_window',
            'context': context,
        }  

    def synchronize_accounts(self, cr, uid, ids=False, context=None):
        """WARNING: meant for cron usage only"""

        account_pool = self.pool.get('google.api.account')
        instance_pool = self.pool.get('google.api.calendar')

        accounts = account_pool.search(cr, uid, [('synchronize', '=', True)])
        for account_id in accounts:
            instances = instance_pool.search(cr, uid, [('account_id', '=', account_id)])
            for instance_id in instances:
                try:
                    calendar = instance_pool.browse(cr, uid, instance_id)
                    if not context:
                        context = {}
                    context['limit_date'] = calendar.last_update_synchronize_date                    
                    instance_pool.do_synchronize(cr, uid, [instance_id], context)
                    
                    delta_date = calendar.last_update_synchronize_date + timedelta(days= calendar.update_synchronize_date_every or 3)
                    
                    if delta_date >= datetime.datetime.now():
                        instance_pool.write(cr, uid, instance_id, {
                           'last_update_synchronize_date' : datetime.datetime.now()  
                        })                                        
                    
                except:
                    logger.error('Auto synchronizing failed.')
