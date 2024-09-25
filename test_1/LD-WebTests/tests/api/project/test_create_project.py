import pytest
from ldclient.models import Project
from requests import RequestException
from library.utils import make_unique_name


@pytest.fixture()
def actual_create_project_response(ld_client, request):
    """
    Create Project using create_project function.

    :param ld_client: ldclient
    :param request: SubRequest w/ param field for ldclient.models.Project to create in LD
    :return: ldclient.models.Project and RequestException, Project if successfully created or
                                                           RequestException if unsuccessful
    """
    success = False
    try:
        response = ld_client.create_project(request.param)
        success = True
    except RequestException as e:
        response = e
    # passing error/Success response in the response
    yield response

    # Archive the project so it doesn't interfere with other tests
    if success:
        response.active = 'N'
        ld_client.update_project(response.id, response)


class TestCreateProject:
    """
    Test for Creating Project with positive test data and negative test data and Validation.
    """

    # Positive Project Test data(Project should create)
    project_with_name_description_alternate_ID = Project(id="578",
                                                         name=make_unique_name("Project"),
                                                         description='This is my project.',
                                                         alternate_id='pr')
    project_with_name_description = Project(id="578",
                                            name=make_unique_name("Project"),
                                            description='This is my project.')

    # Negative Project Test data (Project should not create (400 bad request))
    project = Project(id="578")
    project_with_name = Project(id="578", name='ProjectTwo')
    project_with_description = Project(id="578", description='This is my project.')
    project_with_alternate_ID = Project(id="578", alternate_id='pr')
    project_with_name_alternate_ID = Project(id="578", name='ProjectThree', alternate_id='pr')
    project_with_description_alternate_ID = Project(id="578", description='This is my project.', alternate_id='pr')

    @pytest.mark.parametrize(
        "expected_project, actual_create_project_response, status_code",
        [(project_with_name_description_alternate_ID, project_with_name_description_alternate_ID, 'NA'),
         (project_with_name_description, project_with_name_description, 'NA'),
         (project_with_name, project_with_name, '400'), (project_with_description, project_with_description, '400'),
         (project_with_alternate_ID, project_with_alternate_ID, '400'),
         (project_with_name_alternate_ID, project_with_name_alternate_ID, '400'),
         (project_with_description_alternate_ID, project_with_description_alternate_ID, '400'),
         (project, project, '400')],
        indirect=["actual_create_project_response"])
    def test_create_project(self, expected_project, actual_create_project_response, status_code):
        """
        Test create project function. Verifies the Project and response with expected Project

        1. Create Project using expected_project fixture.
        2. Verify that project throws the appropriate error for the negative test data
        3. Verify that project gets created for positive test data

        :param expected_project: ldclient.models.Project, expected project to be created
        :param actual_create_project_response: ldclient.models.Project or RequestException, actual project response
        object for success response otherwise Exception
        :param status_code: string, status code for negative tests
        """

        if status_code != 'NA':
            # validating error for negative test data, should get RequestException for negative testdata.
            assert isinstance(actual_create_project_response, RequestException), \
                "Livereport is created with negative test data: {}".format(expected_project)
            # validating error response
            assert str(actual_create_project_response.response) == '<Response [{}]>'.format(status_code)
            return

        # Validating response for positive test data
        assert isinstance(actual_create_project_response, Project), \
            "Project not created with test data: {}, and got error: {}".format(expected_project, actual_create_project_response)
        assert actual_create_project_response.name == expected_project.name, \
            "Project name is not matching with the response name"
        assert actual_create_project_response.active == expected_project.active, \
            "Project active variable is not matching with the response active variable "
        assert actual_create_project_response.alternate_id == expected_project.alternate_id, \
            "Project alternate ID is not matching with the response alternate ID "
        assert actual_create_project_response.default_template_id == str(expected_project.default_template_id), \
            "Project default template id is not matching with the response default template id"
        assert actual_create_project_response.description == expected_project.description, \
            "Project description is not matching with the response description "
        assert actual_create_project_response.restricted == expected_project.restricted, \
            "Project restricted variable is not matching with the response restricted variable "
        assert actual_create_project_response.keep_styles == expected_project.keep_styles, \
            "Project keep styles variable is not matching with the response keep styles variable "
        assert actual_create_project_response.therapeutic_area == expected_project.therapeutic_area, \
            "Project therapeutic area is not matching with the response therapeutic area "
        assert actual_create_project_response.project_lead == expected_project.project_lead, \
            "Project lead is not matching with the response lead. "
