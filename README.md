### Test
Run `make clean && make test` to run the test suite

Tests on master branch should fail on last test

Test should all pass on patch branch

### Setting up site
Run `make clean && make run` and visit localhost:5050, use `John Smith` and `johnpw` to login

### Detecting/Exploiting the vulnerability
Set up the site

Inject sql into the search field on `/admin` - `IF(SUBSTRING(password,1,1) = CHAR(106), SLEEP(5), null)`
Observe abnormal response time
Inject sql into the search field on `/admin` - `IF(SUBSTRING(password,1,1) = CHAR(105), SLEEP(5), null)`
Observe the regular response time

Try with other characters to leak password for the given user
Passwords can be seen in seed in src/app/migrations/versions

### Patching
Switch to patch branch and set up site normally as above

To patch this vulnerability, we query the user fields using the ORM and pop sensitive information

```
        user_model = db.session.query(User).get(id).__dict__

        user_model.pop('password', None)
        user_model.pop('_sa_instance_state', None)

```

### Description
This program is designed to be vulnerable to timing based blind SQL injection, the program utilises make file
and docker/docker-compose to be as portable as possible. The program is built in python3 using the Flask framework
together with SQLAlchemy and alembic.
