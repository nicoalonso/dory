#!/usr/bin/python3

import random
import requests
from pprint import pprint

from msgterm import MsgTerm
from utils import FormHtmlParser
from .RegisterBase import RegisterBase


class OdooRegister(RegisterBase):
    '''Odoo Register
    
    Use for connecto to Odoo register
    
    Extends:
        RegisterBase

    Args:
        config (Configurize): user configuration

    Attributes:
        endpoint (string): odoo endpoint url
        user (string): odoo user
        password (string): odoo password
        client (Session): requests client
    '''

    def __init__(self, config):
        RegisterBase.__init__(self, config)
        self.endpoint = config.get('register.odoo.endpoint')
        self.user = config.get('register.odoo.user')
        self.password = config.get('register.odoo.password')
        self.client = requests.Session()


    def makeUrlCallKw(self, model, method):
        '''Make URL
        
        Used for create the url to call
        
        Arguments:
            model {string}: odoo model
            method {string}: odoo model method
        
        Returns:
            str: the url
        '''

        return self.endpoint + '/web/dataset/call_kw/%s/%s' % (model, method)


    def makePostData(self, model, method, args, kwargs={}):
        '''make post data
        
        Used for create the JSON post data to send to Odoo
        Odoo use JSON RPC 2.0 Protocol
        
        Arguments:
            model {string}: Odoo model
            method {string}: Odoo model method
            args {dict}: arguments to pass Odoo
        
        Keyword Arguments:
            kwargs {dict}: keywords to pass Odoo (default: {{}})
        '''

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


    def checkStatusCode(self, response):
        '''Check status code
        
        Check status code for response object
        
        Arguments:
            response {Response}: response object
        
        Returns:
            bool
        '''

        MsgTerm.debug('Response code: %s' % response.status_code)
        check = (response.status_code >= 200 and response.status_code < 300)
        if not check:
            MsgTerm.warning('Response with error return code: %s' % response.status_code)
        return check


    def checkContentType(self, response, expected='application/json'):
        '''Check content type
        
        Arguments:
            response {Response}: requests responde object
        
        Keyword Arguments:
            expected {str}: content type expected (default: {'application/json'})
        
        Returns:
            bool
        '''

        MsgTerm.debug('Response expected: %s' % expected)
        MsgTerm.debug('Response content-type: %s' % response.headers['content-type'])
        check = (expected in response.headers['content-type'])
        if not check:
            MsgTerm.warning('Response with wrong content type: %s => %s' % (expected, response.headers['content-type']))
        return check


    def checkResponse(self, resp, contentTypeExpected='application/json'):
        '''Verify response
        
        Check status code and content type of response
        
        Arguments:
            resp {Response}: requests response object
        
        Keyword Arguments:
            contentTypeExpected {str}: contenty type expected (default: {'application/json'})
        
        Returns:
            bool
        '''

        return self.checkStatusCode(resp) and self.checkContentType(resp, contentTypeExpected)


    def call(self, model, method, args, kwargs={}):
        '''Call method
        
        call to method of model and pass the arguments
        
        Arguments:
            model {string}: Odoo model
            method {string}: Odoo model method
            args {dict}: Odoo arguments
        
        Keyword Arguments:
            kwargs {dict}: Odoo keyword arguments (default: {{}})
        '''

        url = self.makeUrlCallKw(model, method)
        body = self.makePostData(model, method, args, kwargs)

        MsgTerm.debug('URL: %s' % url)
        if MsgTerm.verbose_level == 0:
            MsgTerm.debug('Request body')
            MsgTerm.jsonPrint(body)

        resp = self.client.post(url, json=body)
        ok = self.checkResponse(resp)
        
        return (ok, resp)


    def login(self):
        '''Odoo login
        
        Login to Odoo register
        
        Returns:
            bool: Login result
        '''

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


    def getReasons(self):
        '''Get reasons
        
        Get reasons to register
        '''

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
        '''Check connection with the register
        
        Returns:
            bool
        '''

        if self.login():
            self.getReasons()

        return True
