# Odoo register

import random
import requests
from pprint import pprint

from config import MsgTerm
from utils import FormHtmlParser
from .RegisterBase import RegisterBase

# Odoo class register
class OdooRegister(RegisterBase):
    # Constructor
    def __init__(self, config):
        RegisterBase.__init__(self, config)
        self.endpoint = config.get('register.odoo', 'endpoint')
        self.user = config.get('register.odoo', 'user')
        self.password = config.get('register.odoo', 'password')
        self.client = requests.Session()

    # Make URL
    def makeUrlCallKw(self, model, method):
        return self.endpoint + '/web/dataset/call_kw/%s/%s' % (model, method)

    # Make post data for json RPC 2.0
    def makePostData(self, model, method, args, kwargs={}):
        return {
            "id": random.randrange(99999999),
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": "hr.attendance",
                "method": "get_all_attendance_reasons",
                "args": args,
                "kwargs": kwargs
            }
        }

    # Check status code
    def checkStatusCode(self, response):
        MsgTerm.debug('Response code: %s' % response.status_code)
        check = (response.status_code >= 200 and response.status_code < 300)
        if not check:
            MsgTerm.warning('Response with error return code: %s' % response.status_code)
        return check

    # Check content type
    def checkContentType(self, response, expected='application/json'):
        MsgTerm.debug('Response expected: %s' % expected)
        MsgTerm.debug('Response content-type: %s' % response.headers['content-type'])
        check = (expected in response.headers['content-type'])
        if not check:
            MsgTerm.warning('Response with wrong content type: %s => %s' % (expected, response.headers['content-type']))
        return check

    # Verify Response
    def checkResponse(self, resp, contentTypeExpected='application/json'):
        return self.checkStatusCode(resp) and self.checkContentType(resp, contentTypeExpected)

    # Call method
    def call(self, model, method, args, kwargs={}):
        url = self.makeUrlCallKw(model, method)
        body = self.makePostData(model, method, args)
        MsgTerm.debug('URL: %s' % url)
        if MsgTerm.verbose_level == 0:
            MsgTerm.debug('Request body')
            MsgTerm.jsonPrint(body)

        # data=json.dumps(data),
        resp = self.client.post(url, json=body)
        ok = self.checkResponse(resp)
        
        return (ok, resp)

    # Login to Odoo
    def login(self):
        # Get form page and catch csrf_token
        resp = self.client.get(self.endpoint)

        if not self.checkResponse(resp, 'text/html'):
            MsgTerm.error('[Login] Error to request web')
            return False

        # Parser html
        parser = FormHtmlParser()
        parser.feed(resp.text)
        form = parser.getForm('login')

        if not form:
            MsgTerm.error('[Login] Form login not found')
            return False

        # Create body
        body = {}
        for (name, field) in form['inputs'].items():
            if 'value' in field:
                value = field['value']
            else:
                value = ''
            body[name] = value

        # Set user and password
        if 'csrf_token' in body:
            MsgTerm.debug('[Login] csrf_token: %s' % body['csrf_token'])
        else:
            MsgTerm.warning('[Login] not found csrf_token')

        url = self.endpoint + form['action']
        MsgTerm.debug('[Login] Url: %s' % url)
        body['login'] = self.user
        body['password'] = self.password
        resp = self.client.post(url, data=body)

        if not (self.checkResponse(resp, 'text/html') and self.client.cookies.get('session_id')):
            MsgTerm.error('[Login] Error to Login')
            return False

        MsgTerm.debug('[Login] session_id: %s' % self.client.cookies.get('session_id'))
        return True

    # Get Reasons
    def getReasons(self):
        model = 'hr.attendance'
        method = 'get_all_attendance_reasons'
        args = [[650]]

        ok, resp = self.call(model, method, args)
        if ok:
            MsgTerm.jsonPrint(resp.json())



# Llamadas:
# 
# /web/dataset/search_read
# /web/dataset/call_kw/hr.employee/attendance_manual
# /web/dataset/call_kw/hr.employee/search_read
# /web/dataset/call_kw/hr.attendance/add_motivo
# /web/dataset/call_kw/hr.attendance/get_motivo
# /web/dataset/call_kw/hr.attendance/get_all_attendance_reasons
# /web/dataset/call_kw/hr.attendance/get_time_worked_today
# /web/dataset/call_kw/hr.attendance/load_views
# /web/dataset/call_kw/hr.attendance/read
# /web/dataset/call_kw/hr.attendance.reason/read
# /web/dataset/call_kw/hr.attendance/onchange
# /web/dataset/call_kw/hr.attendance.status/name_search
# /web/dataset/call_kw/hr.attendance/write
# /web/dataset/call_kw/hr.attendance/read


# /web/dataset/call_kw/mail.message/message_format
# /web/dataset/call_kw/ir.attachment/search_read
# /web/dataset/call_kw/altia.altia.proyecto/name_search
# /web/image/res.partner/684/image_small

# /web/action/load
# /mail/read_followers


    # Check connection with register
    def check(self):
        if self.login():
            self.getReasons()

        return True