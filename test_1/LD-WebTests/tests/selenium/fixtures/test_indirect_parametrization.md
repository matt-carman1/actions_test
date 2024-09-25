Indirect parametrization to:
    1. Parametrize logging into LD with different users
    2. Parametrize creating or duplicating an LR with one user and logging into LD with a different user.
    3. Create or Duplicate an LR with one user and then login with a specific set of users. Repeat creating or 
    duplicating LR with another user and logging into LD with a specific set of users.
    4. Run the same test with different value of a given ld property.


# Simple implementation of the login_to_livedesign fixture parametrization
```@pytest.mark.parametrize('login_to_livedesign',
                         [("userB", "userB"), ("demo", "demo")], indirect=True)
def test_indirect_parametrization(request, selenium, login_to_livedesign):
```


# 2*2 parametrization of the test. This would result in 4 test cases.
```
live_report_to_duplicate = {'livereport_name': 'Scatterplot Data', 'livereport_id': '877'}


test_user_one= ("userB", "userB")
test_user_two = ("demo", "demo")

@pytest.mark.parametrize('login_to_livedesign', [("userC", "userC"), ("userA", "userA")], indirect=True)
@pytest.mark.parametrize('ld_api_client',
                          [test_user_one, test_user_two], indirect=True)
def test_indirect_parametrization_api(selenium, duplicate_live_report, open_project):
```



# Another example to parametrize the test with different value of a feature flag.
```python
@pytest.mark.parametrize('customized_server_config', [{'COLUMN_TREE_SEARCH_LENGTH': 3},
                                                       {'COLUMN_TREE_SEARCH_LENGTH': 5}], indirect=True)
@pytest.mark.usefixtures("customized_server_config")
def test_indirect_parametrization_ld_properties(selenium):
```



