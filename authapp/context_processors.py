from authapp.models import User, Role
from pharmacy_delivery.apps.orm.BaseManager import BaseManager


def user_context(request):
    """
    Adds user_id and username to the context, if the user is authenticated.
    """
    user_id = request.session.get('user_id')
    username = None
    role_name = None

    if user_id:
        BaseManager.set_connection()
        users = User.objects.select('name', 'role_id', condition=f'id = {user_id}')
        result = users[0]
        if result:
            username = result['name']
            role_id = result['role_id']
            print(f'=== role id is {role_id}')
            roles = Role.objects.select('name', condition=f'id = {role_id}')
            print(f'roles are {roles}')
            role = roles[0]
            if role:
                role_name = role['name']
                print(f'role_name {role_name}')


    return {
        'user_id': user_id,
        'username': username,
        'role': role_name,
    }
