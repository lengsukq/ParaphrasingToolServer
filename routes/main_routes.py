from . import main
from response_utils import make_response

@main.route('/')
def hello_world():
    return make_response(data="Hello World!", message="Welcome to the API")
