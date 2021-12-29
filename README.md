# backend-project-template

## Welcome
Hello! Welcome to the backend engineering task as part of your interview process with Deel as a Python/Django developer! This task should take about 1-3 hours of your time. As you're completing the tasks below, make sure you document your process including any snags you hit, trade-offs you made, or shortcuts you decided to take. Your decision-making process is equally as important as the completion of these tasks.

### Requirements
- Docker

### Set-up Instructions
This project is already fully configured to launch. You will only need to add data to the DB to get started.

Clone this repository, navigate into the root directory, and boot up using `docker-compose up directory`. This command will pull the base python image, install requirements, migrate and launch the local server.

To add some data, open another shell and connect to the running container with `docker-compose exec directory bash`. You can then navigate into the directory `cd mysite`, and launch the shell with `./manage.py shell`.

### Data & Models
The models in this app are very simple. There are only 3 you need to worry about:
1) The `User` model. This model contains basic attributes from Django, with only the addition of `Company` and `reports_to` foreign keys.
2) The `Company` model. All `User`s have a `Company`. It is a natural grouping for a Enterprise SaaS product.
3) The `Token` object (`from rest_framework.authtoken.models import Token`). This will be used for authenticating a `User` over the API.

To add some data, you can use `create_user`.
```python
>>> from directory.models import *
>>> company = Company.objects.create(name="Test Company")  # Create a new Company
>>> user = User.objects.create_user(username=..., first_name=..., last_name=..., company=company)  # Add a user to the Company.
>>> from rest_framework.authtoken.models import Token  # Import the Token model
>>> token = Token.objects.create(user=user)  # Create an API Token for this new user.
>>> print(token.key)  # Display the API key for this User.
```

You will likely need to add more data to the DB to properly implement the requirements for the tasks below. Creating a script would *probably* be useful. :wink:

### Tasks
1) Make sure that for the `/users` endpoint, that only users for the calling user's company are shown.

This is done overriding the get_queryset.

2) Update the `reports` action in `UsersViewSet` to return all reports _down_ the reporting tree, recursively.

This is very inneficient, it's a tree struture with pointers only pointing up. A better way would be having a list of reportees in every user, therefore pointing down. This raises two concerns: 1) We would have to ensure consistency, every arrow pointing up must have one exactly like it pointing down(and vice-versa). 2) Recursive functions can cause call stack overflow at scale either way.

3) Add another action, similar to `reports`, called `managers`, that does the inverse of `reports`. It should return all users _up_ the reporting tree from the designated user.

You just have to follow the trail of pointers up, since every user only reports to one person. This is efficient. I had a little trouble questioning wheter or not I should convert the lists and sets to queryset, but that would de an uneeded overhead, there's likely a way to do this using querysets directly.

If the user structure was too big, passing the entire user data would not be efficient, and it would be better to pass by primary key and use it to query the managers.

4) Add a [filter](https://django-filter.readthedocs.io/en/stable/guide/usage.html#the-filter) for the `/users` endpoint that returns only users that have at least 1 person reporting to them (AKA, filter out users who are/are not managers). Name this filter `is_manager`. It should handle both `true`/`false` values.

5) Add another for the `/users` endpoint that returns only users that _do not_ have a manager. Name this filter `has_manager`. It should handle both `true`/`false` values.

6) Add tests. A `mysite/directory/tests/tests.py` file is configured for you. Add tests there. To run the tests, open a second shell and use the `docker-compose exec directory bash` command to enter the running container. Then run the tests with `./manage.py test -v 2`.

I tried following the testing insctructions as close as I could, but could not use the reversed function, I also feel like the authentication itself could be tested instead of forced.

### Follow-up Questions
1) Provide a few bullet points of optimizations or improvements you would make if given more time.

#Rework the entire authentication principles, they are very bad for security and not very different from storing plain text passwords.

#set up an openAPI/Swagger endpoint

2) Any cool feature ideas that you could add as well with minimal effort?

I was thinking of making it more RESTful by adding a post,put,patch,delete. 

Good luck!


## Development diary

Creating the database was very fun, I like superheroes. The dataset is based on requirements: it has to have multiple companies(person from company A can't see company B). It needs to have a hierarchy of at least two levels, so we can test looking up and down the reports.

I had to chose to return 204 http status when it's returning an empty list, many applications return 200.

I'm assuming every user only reports to a single person or to no one.
