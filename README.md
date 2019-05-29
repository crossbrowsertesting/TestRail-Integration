# TestRail Integration for CBT
TestRail-CBT integration is created to help our users easily upload their test results to their test runs using TestRail's provided API. This example is written in python but you can read about how to use this API in their documentation here: [TestRail API Docs](http://docs.gurock.com/testrail-api2/start)

### Dependencies
1. TestRail account with API enabled (You  can do this by going to Administration -> Site Settings -> API -> Enable API)
2. Requests (HTTP request library for python)
3. Json (Json library for python)


Both of these are native to python and should already be included in your python environment. If though you do not have these preinstalled you can install them with the package manager Pip.
Using pip to install, go to your terminal and type: `pip install requests` or `pip install json`

***

### Quickstart Guide
Clone this repo and add `TestRails.py` to your working directory.

For authentication you will need to provide your `email` and `password` as well as your `TestRail url`. Here is a quick example of how a QA at Cross Browser Testing would authenticate their requests.
```
testrail_auth = TestRail('cbtQA@crossbrowsertesting.com', 'password_here', 'testcbt.testrail.io')
```

To add a result to a test you will call `add_result()` and provide the two required arguments: `test_id` and `status_id`. All other fields are optional and are set by keywords. Put this snippet of code at the end of your test cycle to mark whether your CBT test has passed or failed.
```
testrail_auth.add_result(test_id, status_id, comment = "Your comment here", version = "1.0.0")
```

**A example of all the fields you can set are listed here:**

| Name | Type | Description |
| ----------- | ----- | ---- |
| status_id	 | int | The ID of the test status. |
| comment | string | The comment / description for the test result |
| version | string | The version or build you tested against |
| elasped | timespan | 	The time it took to execute the test, e.g. "30s" or "1m 45s" |
| defects | string | A comma-separated list of defects to link to the test result |
| assigned_to | int | The ID of a user the test should be assigned to |

*Status ids can be passed as integer or string: ex: 1, 2, 4, 5 or Passed, Blocked, Retest, Failed*

***

### Getting needed information from Users, Projects, Runs or Tests
If you need gather any IDs for users, tests, runs, or projects we have also included easy ways to obtain these.

**Find user by email account:** `testrail_auth.get_user_by_email(email)`

Response Content:
```
{
	"email": "alexis@example.com",
	"id": 1,
	"is_active": true,
	"name": "Alexis Gonzalez"
}
```
**Find all projects:** `testrail_auth.get_projects()`

Response Content:
```
{
    "project_id": 1,
    "name": "New CBT project",
    "is_completed": false
}
```
**Find all test runs in project:** `testrail_auth.get_all_runs(project_id)`

Response Content:
```
{
    "run_id": 2,
    "suite_id": 3,
    "name": "Test Run 5/29/2019",
    "assignedto_id": 1
}
```
**Find all tests in test run:** `testrail_auth.get_all_tests(run_id)`

Response Content:
```
{
    "test_id": 4,
    "name": "Go to crossbrowsertesting.com",
    "status": "Untested"
}
```
