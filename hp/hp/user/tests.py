from django.test import TestCase
from healthpark.user.models import User

"""IMPORTANT!: Use the command ' manage.py test --settings="settings_test" '
to run these tests... """

class User_test(TestCase):
    
    def setUp(self):
        for x in range(1,6):
            user = User(nickname = 'user_%s' % x,
                         first_name = 'xyz',
                         last_name = 'XYZ',
                         password = 'userxxyz',
                         email = 'xyz@xyz.com',
                         address = 'asdf asdfasdf asdf ',
                         phone_number = '0300123987852',
                         fax_number = '021545896217',
                         website = 'http://www.xyz.org'
                         )
            user.save()
            
    #Send sample id, match with user object in database, retrieve the user object
    # and assertEqual sample string  
    
    def test_model(self):

        # Retrieve sample user object
        get_user = User.objects.get(id = 5)
        self.assertEqual(get_user.nickname, 'user_5')

        
        