"""
Collection of functions to help interact with jenkins python API
"""
import jenkins

JENKINS_URL = 'https://oldjenkins.dev.bb.schrodinger.com'
JENKINS_JOB_NAME = 'selenium-testserver-2023.3.x'  # Auto-updated by version_bumper.py


def get_host(jobname=JENKINS_JOB_NAME, jenkins_server=JENKINS_URL):
    """
    Function to get host of running selenium testserver

    Note: It should be fine for multiple people to use the same testserver, as
    long as they are not changing test data.

    :param jobname: name of jenkins job
    :return: LD_SERVER host URL
    """
    # Initialize jenkins server object
    server = jenkins.Jenkins(jenkins_server)

    # Grab last build number from jenkins server
    try:
        build_number = server.get_job_info(jobname)['lastBuild']['number']
    except jenkins.JenkinsException as e:
        raise jenkins.JenkinsException(
            '{}\nProblem connecting to Jenkins server. Please ensure VPN connection.'.format(e))

    for subtractor in range(build_number):
        # Grab further information about this specific build
        try:
            build = server.get_build_info(jobname, build_number - subtractor)
        except jenkins.JenkinsException as ex:
            print('No servers available')
            print(ex)
            break

        # Test server is running when this is building, so set url in this case
        if build['building']:
            get_jenkins_parameters(build)
            build_node = build['builtOn']
            return 'http://{}:8080/'.format(build_node)

    # Raise error if no host is available
    raise RuntimeError('No selenium test server running.\nNavigate to: '
                       'https://jenkins.dev.bb.schrodinger.com/job/selenium-'
                       'testserver/ and start a testserver, or set LD_SERVER '
                       'env variable to an active server.')


def get_jenkins_parameters(build_info):
    """
    Function to print out Selenium Testserver info when pytest "-s" flag is
    enabled

    :param build_info: jenkins.Jenkins.get_build_info()
    """

    # Grab value for actions, parameters are nested deeply under
    actions = build_info['actions']

    # Loop thru action list and grab parameters
    param_info = (action.get('parameters') for action in actions if action.get('parameters'))
    params = next(param_info)

    # Print out name/value for each specified parameter
    print("Selenium Testserver Info:")
    for param in params:
        param_name = param['name']
        param_val = param['value']
        print("{}: {}".format(param_name, param_val))
