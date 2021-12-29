from mysite.directory.models import *
from rest_framework.authtoken.models import Token  # Import the Token model

wayne_co = Company.objects.create(name="Wayne Enterprises")

batman = User.objects.create_user(username="Batman", 
first_name="Bruce", last_name="Wayne", company=wayne_co)  

robin = User.objects.create_user(username="Robin", 
first_name="Jason", last_name="Todd", company=wayne_co, reports_to=batman)  

nightwing = User.objects.create_user(username="Nightwing", 
first_name="Dick", last_name="Grayson", company=wayne_co, reports_to=batman)

stark_co = Company.objects.create(name="Stark Enterprises")

ironman = User.objects.create_user(username="Ironman", 
first_name="Tony", last_name="Stark", company=stark_co)

falcon = User.objects.create_user(username="Falcon", 
first_name="Sam", last_name="Wilson", company=stark_co, reports_to=ironman)

happy = User.objects.create_user(username="Happy", 
first_name="Harold", last_name="Hogan", company=stark_co, reports_to=ironman)  

spiderman = User.objects.create_user(username="Spiderman", 
first_name="Peter", last_name="Parker", company=stark_co, reports_to=happy)

get_token_from_user = dict()

users = [batman, robin, nightwing, ironman, falcon, happy, spiderman]

for user in users:
    get_token_from_user[user] = Token.objects.create(user=user)

print(get_token_from_user[spiderman])

print(get_token_from_user[ironman])