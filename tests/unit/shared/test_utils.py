from app.shared.role_enum import RoleEnum

def test_role_enum_values():
    assert RoleEnum.ADMIN.value == 1
    assert RoleEnum.USER.value == 2
