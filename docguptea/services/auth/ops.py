from .utils.auth_funcs import *
from .utils.JWTBearer import *
from docguptea.models import GeneralResponse, UserAuth
from docguptea.services.db.utils.DBQueries import DBQueries


def ops_signup(response_result: GeneralResponse, data: UserAuth):
    """Wrapper method to handle signup process.

    Args:
        response_result: FrontendResponseModel. A TypedDict to return the
                         response captured from the API to the frontend.
        data: UserAuth. New user's prospective credentials from the frontend
                        to create their account.

    Raises:
        ExistingUserException: If account with entered AADHAR Number already exists.
    """
        # querying database to check if user already exist
    user = DBQueries.fetch_data_from_database('auth', ['username', 'email'], f"username='{data.username}' OR email='{data.email}'")
    if len(list(user)) != 0:
        # user with the entered credentials already exists
        raise ExistingUserException(response_result)
    
    DBQueries.insert_to_database('auth', (data.username, Auth.get_password_hash(data.password), data.email))
    api_key = Auth.generate_api_key(data.username)
    DBQueries.insert_to_database('api_key', (data.username, api_key))
    response_result.status = 'success'
    response_result.message = [f'User with this AADHAR NO created successfully']         
