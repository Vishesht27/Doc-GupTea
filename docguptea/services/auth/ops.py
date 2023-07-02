from .utils.auth_funcs import *
from .utils.JWTBearer import *
from docguptea.models import *
from docguptea.services.db.utils.DBQueries import DBQueries
from docguptea.core.Exceptions import *


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
    
    DBQueries.insert_to_database('auth', (data.username, Auth.get_password_hash(data.password), data.email), 
                                 ['username', 'password', 'email'])
    api_key = Auth.generate_api_key(data.username)
    DBQueries.insert_to_database('api_key', (data.username, api_key), ['username', 'apikey'])
    response_result.status = 'success'
    response_result.message = [f'User created successfully']   

def ops_login(data:LoginCreds):
    """Wrapper method to handle login process.

    Args:
        data: LoginCreds. User's credentials from the frontend to login to their account.

    Returns:
        TokenSchema. A Pydantic BaseModel to return the JWT tokens to the frontend.

    Raises:
        InvalidCredentialsException: If account with entered credentials does not exist.
    """
    # querying database to check if user already exist
    response_result = GeneralResponse.get_instance(data={},
                                      status="not_allowed",
                                      message=["Not authenticated"]
                                      )
    user = DBQueries.fetch_data_from_database('auth', ['username', 'password','isNewUser'], f"username='{data.username}'")

    if len(list(user)) == 0:
        # user with the entered credentials does not exist
        raise InvalidCredentialsException(response_result)
    user = list(user)[0]
    if not Auth.verify_password(data.password, user[1]) and Auth.verify_username(data.username, user[0]):
        # password is incorrect
        raise InvalidCredentialsException(response_result)
    
    if (user[2]):
        # user is logging in for the first time
        DBQueries.update_data_in_database('auth','isNewUser',f"username='{data.username}'","0")
        return TokenSchema(access_token=Auth.create_access_token(data.username),
                             refresh_token=Auth.create_refresh_token(data.username),
                             api_key=Auth.generate_api_key(data.username))
    # password is correct
    return TokenSchema(access_token=Auth.create_access_token(data.username), 
                       refresh_token=Auth.create_refresh_token(data.username),
                       api_key="")

def ops_regenerate_api_key(username:str):

    new_key=APIKey(api_key=Auth.generate_api_key(username))
    DBQueries.update_data_in_database('api_key','apikey',f"username='{username}'",new_key.api_key)
    return new_key