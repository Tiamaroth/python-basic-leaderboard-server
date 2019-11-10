import unittest
from test.test_base import TestBase,server_url
import json
import urllib.request
class TestRouting(TestBase):
    kMethod_get = 'get'
    kMethod_post = 'post'
    kUpdate_user_absolute = '/update/user/absolute'
    kUpdate_user_relative = '/update/user/relative'
    def test_wrong_resource_call(self):
        """
            Expect 404 if we call a non existing resource, with a few common typos
        """
        self.check_call_fail_with_error(self.kMethod_get, "/tops/100", None, 404)
        
        self.check_call_fail_with_error(self.kMethod_post, "/update/users/absolute", None, 404)
        

    
    def test_wrong_parameter_type(self):
        """
            Expect 400 if we send wrong data type
        """
        #absolute score wrong type
        update_abs_user_dict = {'user': 123 , 'score': "100"} 
        self.check_call_fail_with_error(self.kMethod_post, self.kUpdate_user_absolute, update_abs_user_dict, 400) 
        
        #absolute score missing 
        update_abs_user_dict = {'user': 123}
        self.check_call_fail_with_error(self.kMethod_post, self.kUpdate_user_absolute, update_abs_user_dict, 400) 
        
        #user wrong type  
        update_abs_user_dict = {'user': "123" , 'score': 100}
        self.check_call_fail_with_error(self.kMethod_post, self.kUpdate_user_absolute, update_abs_user_dict, 400) 
        
        #user missing 
        update_abs_user_dict = {'score': 100}
        self.check_call_fail_with_error(self.kMethod_post, self.kUpdate_user_absolute, update_abs_user_dict, 400) 
        
        #too many params
        update_abs_user_dict = {'user': 100,'score': 100,'three': 100}
        self.check_call_fail_with_error(self.kMethod_post, self.kUpdate_user_absolute, update_abs_user_dict, 400) 
        
        #relative score wrong type
        update_abs_user_dict = {'user': "123" , 'score': 100}
        self.check_call_fail_with_error(self.kMethod_post, self.kUpdate_user_relative, update_abs_user_dict, 400) 


    def test_wrong_gets(self):
        #too many arguments after top
        self.check_call_fail_with_error(self.kMethod_get, '/top/100/20', None, 400) 

        #too few arguments after top
        self.check_call_fail_with_error(self.kMethod_get, '/top/', None, 400) 

        #wrong type
        self.check_call_fail_with_error(self.kMethod_get, '/top/wrongType', None, 400) 

        #too many arguments after partial
        self.check_call_fail_with_error(self.kMethod_get, '/partial/100/20/200', None, 400) 

        #too few arguments after top
        self.check_call_fail_with_error(self.kMethod_get, '/partial/', None, 400) 

        #wrong type
        self.check_call_fail_with_error(self.kMethod_get, '/partial/wrongType/again', None, 400) 
        
        
    def check_call_fail_with_error(self,method,address,params,error_code):
        try:
            if method == 'get': 
                self.send_http_get(server_url + address)
            else:
                self.send_http_post(server_url + address,params)
            self.fail("Should have thrown http error %s" % error_code)
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code,error_code)
