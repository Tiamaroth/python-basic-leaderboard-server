import unittest
from test.test_base import TestBase,server_url
import json
import urllib.error
import operator
import server
class TestLeaderboardOps(TestBase):

    


    def test_empty_list(self):
        """
            Checks that if we do not post any score, the top 100 is empty
        """
        response = self.send_http_get(server_url + "/top/100")  
        self.assertEqual(response, b'[]')


    def test_update_absolute_score(self):
        """
            Checks that we are able to update an absolute score
        """
        update_abs_user_dict = {'user': 123 , 'score': 100}
        self.send_http_post(server_url + "/update/user/absolute",update_abs_user_dict)
        response = self.send_http_get_deserialized(server_url + "/top/100")
        self.assertEqual(response, [{'user': 123, 'score': 100}])

    def test_update_relative_score(self):
        """
            Checks that we are able to update a relative score of a user
        """
        add_user_dict = {'user': 123 , 'score': 100}
        self.send_http_post(server_url + "/update/user/absolute",add_user_dict)

        update_rel_user_dict = {'user': 123 , 'score': '+10'}
        self.send_http_post(server_url + "/update/user/relative",update_rel_user_dict)
        
        response = self.send_http_get_deserialized(server_url + "/top/100")
        self.assertEqual(response, [{'user': 123, 'score' : 110}])

        update_rel_user_dict = {'user': 123 , 'score': '-20'}
        self.send_http_post(server_url + "/update/user/relative",update_rel_user_dict)
        response = self.send_http_get_deserialized(server_url + "/top/100")
        self.assertEqual(response, [{'user': 123, 'score' : 90}])

    def test_update_fail_relative_score(self):
        """
            Checks that we fail to update a relative score of a non existing user
        """
        print("test_update_fail_relative_score")
        update_rel_user_dict = {'user': 123 , 'score': '+10'}
        try:
            self.send_http_post(server_url + "/update/user/relative",update_rel_user_dict)
            self.fail("Should have thrown http error 404")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code,404)
    
    def test_get_user_ordering(self):
        """
            Checks that  randomly inserted user are ordered and they are ordered after update
        """
        generated_users = self.add_X_user(5)
        for u in generated_users:
            self.send_http_post(server_url + "/update/user/absolute",u)
        response = self.send_http_get_deserialized(server_url + "/top/100")
        
        
        self.assertEqual(len(response),5) #TODO magic number removal

        for current_u, next_u in zip(response, response[1:]):
            current_score = current_u['score']
            next_score = next_u['score']
            self.assertGreaterEqual(current_score , next_score)

        update_rel_user_dict = {'user': 3 , 'score': '+1000'}
        self.send_http_post(server_url + "/update/user/relative",update_rel_user_dict)    

        response = self.send_http_get_deserialized(server_url + "/top/100")
        
       
        self.assertEqual(len(response),5) #TODO magic number removal

        for current_u, next_u in zip(response, response[1:]):
            current_score = current_u['score']
            next_score = next_u['score']
            self.assertGreaterEqual(current_score , next_score)

    def test_get_tops(self):
        """
            Checks that we are able to retrive topList 
        """
        generated_users = self.add_X_user(600)
        for u in generated_users:
            self.send_http_post(server_url + "/update/user/absolute",u)
        
        response = self.send_http_get_deserialized(server_url + "/top/100")
        
        self.assertEqual(len(response),100) #TODO magic number removal
        
        response = self.send_http_get_deserialized(server_url + "/top/200")
        
        self.assertEqual(len(response),200) #TODO magic number removal
       
        response = self.send_http_get_deserialized(server_url + "/top/500")
        
        self.assertEqual(len(response),500) #TODO magic number removal
        
    def test_get_partial(self):
        """
            Checks that we can retrieve partial chunks of leaderboard
        """
        generated_users = self.add_X_user(10)
        for u in generated_users:
            self.send_http_post(server_url + "/update/user/absolute",u) #TODO refactor
        sorted_list = sorted(generated_users,  key=operator.itemgetter("score","user"), reverse=True)
        
        # simple case
        response = self.send_http_get_deserialized(server_url + "/partial/5/2")
        self.assertEqual(sorted_list[2:7],response)

        # upper boundaries
        response = self.send_http_get_deserialized(server_url + "/partial/9/3")
        self.assertEqual(sorted_list[5:],response)  

        # lower boundaries
        response = self.send_http_get_deserialized(server_url + "/partial/2/3")
        self.assertEqual(sorted_list[:5],response)

        # huge boundaries
        response = self.send_http_get_deserialized(server_url + "/partial/5/10")
        self.assertEqual(sorted_list,response)

    def test_same_score_ordered_by_id(self):
        """
            Checks that user with same score are ordered by user id
        """
        add_user_dict = {'user': 1 , 'score': 100}
        self.send_http_post(server_url + "/update/user/absolute",add_user_dict)

        add_user_dict = {'user': 2 , 'score': 100}
        self.send_http_post(server_url + "/update/user/absolute",add_user_dict)

        add_user_dict = {'user': 3 , 'score': 100}
        self.send_http_post(server_url + "/update/user/absolute",add_user_dict)

        response = self.send_http_get_deserialized(server_url + "/top/100")
        self.assertEqual(response, [{'user': 3, 'score' : 100},{'user': 2, 'score' : 100},{'user': 1, 'score' : 100}])