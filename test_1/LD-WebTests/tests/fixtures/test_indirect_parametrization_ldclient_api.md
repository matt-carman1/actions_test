

```
@pytest.mark.parametrize('ld_api_client', [("userB", "userB"), ("demo", "demo")], indirect=True)
def test_indirect_parametrization(ld_api_client):
```