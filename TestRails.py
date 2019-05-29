import requests
import json

class TestRail:

    #Username, authkey(password or API key), url
    def __init__(self, username, authkey, rail_url):
        #Account credentials
        self.username = username
        self.authkey = authkey

        #API URL
        self.testrail_url = "https://"+rail_url+"/index.php?/api/v2/"

        #Headers used in requests
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic Auth',
        }

    #Get user by email
    def get_user_by_email(self, email):

        #URL for request
        url = self.testrail_url+"get_user_by_email&email="+email

        request = requests.get(
            url,
            auth = (self.username, self.authkey),
            headers = self.headers
        )

        return json.loads(request.content)

    #Get projects
    def get_projects(self):

        #URL for get request
        url = self.testrail_url+"get_projects"

        #Send GET request
        request = requests.get(
            url,
            auth = (self.username, self.authkey),
            headers = self.headers,
        )

        #If valid request
        if request.status_code == 200:
            project_list_results = json.loads(request.content)

            project_list = []

            #Parse list and keep only whats useful
            for project in project_list_results:
                details = {
                    'project_id': project['id'],
                    'name': project['name'],
                    'is_completed': project['is_completed']
                }

                #Add results to list
                project_list.append(details)

            result = project_list

        else:
            result = json.loads(request.content)

        #Send back results
        return result

    #Get all test runs for a project
    def get_all_runs(self, project_id):

        #URL for GET request
        url = self.testrail_url+"get_runs/"+str(project_id)

        #Send post request to TestRail
        request = requests.get(
            url,
            auth = (self.username, self.authkey),
            headers = self.headers,
        )

        #If valid request
        if request.status_code == 200:
            all_runs_results = json.loads(request.content)

            all_runs_list = []

            #Parse list and keep only whats useful
            for run in all_runs_results:

                details = {
                    'run_id': run['id'],
                    'suite_id': run['suite_id'],
                    'name': run['name'],
                    'assignedto_id': run['assignedto_id']
                }

                #Add results to list
                all_runs_list.append(details)

            result = all_runs_list

        else:
            result = json.loads(request.content)

        #Send back results
        return result

    #Get all tests for a run
    def get_all_tests(self, run_id):

        #URL for get request
        url = self.testrail_url+"get_tests/"+str(run_id)

        #Send post request to TestRail
        request = requests.get(
            url,
            auth = (self.username, self.authkey),
            headers = self.headers,
        )

        #If valid request
        if request.status_code == 200:
            all_tests_results = json.loads(request.content)

            all_tests_list = []

            status_codes = {
                '1': 'Passed',
                '2': 'Blocked',
                '3': 'Untested',
                '4': 'Retest',
                '5': 'Failed'
            }

            #Parse list and keep only whats useful
            for test in all_tests_results:

                status = str(test['status_id'])

                status = status_codes.get(status)

                details = {
                    'test_id': test['id'],
                    'name': test['title'],
                    'status': status
                }

                #Add results to list
                all_tests_list.append(details)

            result = all_tests_list

        else:
            result = json.loads(request.content)

        #Send back results
        return result


    #Add test results to run
    def add_result(self, test_id, status_id, comment = None, version = None, elaspsed = None, defects = None, assignedto_id = None):

        #URL for post request
        url = self.testrail_url+"add_result/"+str(test_id)

        #Check/format of status code
        status_codes = {
            'passed': 1,
            'blocked': 2,
            'retest': 4,
            'failed': 5,
            '1': 1,
            '2': 2,
            '4': 4,
            '5': 5
        }

        #Format status id and check if valid
        status_id = str(status_id).lower()
        status_id = status_codes.get(status_id, False)

        #If status code is valid
        if status_id is not False:

            #Parameters
            params = {
                'status_id': int(status_id),
            }

            if comment is not None:
                params['comment'] = str(comment)

            if version is not None:
                params['version'] = str(version)

            if defects is not None:
                params['defects'] = str(defects)

            if assignedto_id is not None:
                params['assignedto_id'] = int(assignedto_id)

            #Format params for JSON
            params = json.dumps(params)

            #Send post request to TestRail
            request = requests.post(
                url,
                auth = (self.username, self.authkey),
                headers = self.headers,
                data = params,
            )

            if request.status_code == 200:

                result = "Updated test id: "+ str(test_id)

            else:
                result = json.loads(request.content)

        else:
            result = "You provided an invalid status code"

        return result
