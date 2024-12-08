from authapp.models import User
from pharmacy_delivery.apps.orm.BaseManager import BaseManager


def user_context(request):
    """
    Adds user_id and username to the context, if the user is authenticated.
    """
    user_id = request.session.get('user_id')
    username = None

    if user_id:
        BaseManager.set_connection()
        users = User.objects.select('name', condition=f'id = {user_id}')
        result = users[0]
        if result:
            username = result['name']

    return {
        'user_id': user_id,
        'username': username,
    }
