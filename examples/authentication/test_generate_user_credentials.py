import unittest
from unittest import mock

# Import the script to be tested
import generate_user_credentials

# Mock google_auth_oauthlib.flow.Flow
@mock.patch('generate_user_credentials.Flow')
class MockFlow:
    @staticmethod
    def from_client_secrets_file(client_secrets_file, scopes, redirect_uri):
        mock_flow_instance = mock.Mock()
        mock_flow_instance.authorization_url.return_value = ('https://accounts.google.com/o/oauth2/auth?scope=test_scope&redirect_uri=http://localhost:8080/&response_type=code&client_id=test_client_id', 'test_state')
        mock_flow_instance.fetch_token.return_value = {'access_token': 'test_access_token'}
        return mock_flow_instance

# Mock socket.socket
@mock.patch('socket.socket')
class MockSocket:
    def __init__(self, *args, **kwargs):
        self.mock_socket_instance = mock.Mock()

    def __enter__(self):
        return self.mock_socket_instance

    def __exit__(self, *args):
        pass

    def bind(self, address):
        return self.mock_socket_instance.bind(address)

    def listen(self, backlog):
        return self.mock_socket_instance.listen(backlog)

    def accept(self):
        mock_conn = mock.Mock()
        # Simulate receiving a request with a code and state
        mock_conn.recv.return_value = b'GET /?code=test_auth_code&state=test_state HTTP/1.1\r\nHost: localhost:8080\r\n\r\n'
        return mock_conn, ('127.0.0.1', 12345)

    def recv(self, bufsize):
        return self.mock_socket_instance.recv(bufsize)

    def sendall(self, data):
        return self.mock_socket_instance.sendall(data)

    def close(self):
        return self.mock_socket_instance.close()

# Replace the actual classes with mocks for the entire module
generate_user_credentials.Flow = MockFlow
socket_socket_patcher = mock.patch('socket.socket', MockSocket)

class TestGenerateUserCredentials(unittest.TestCase):
    def setUp(self):
        # Start patchers
        self.mock_flow_patcher = mock.patch('generate_user_credentials.Flow', MockFlow)
        self.mock_socket_patcher = mock.patch('socket.socket', MockSocket)
        self.MockFlow = self.mock_flow_patcher.start()
        self.MockSocket = self.mock_socket_patcher.start()

    def tearDown(self):
        # Stop patchers
        self.mock_flow_patcher.stop()
        self.mock_socket_patcher.stop()

    def test_parse_raw_query_params_valid_request(self):
        raw_request = b"GET /?code=test_code&state=test_state HTTP/1.1\r\nHost: localhost\r\n\r\n"
        expected = {'code': 'test_code', 'state': 'test_state'}
        self.assertEqual(generate_user_credentials.parse_raw_query_params(raw_request), expected)

    def test_parse_raw_query_params_no_query_parameters_path_only(self):
        raw_request = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        expected = {}
        self.assertEqual(generate_user_credentials.parse_raw_query_params(raw_request), expected)

    def test_parse_raw_query_params_no_query_parameters_empty_after_qmark(self):
        raw_request = b"GET /? HTTP/1.1\r\nHost: localhost\r\n\r\n"
        # query_string becomes "", pairs becomes [['']], params becomes {'': ''}
        expected = {'': ''}
        self.assertEqual(generate_user_credentials.parse_raw_query_params(raw_request), expected)

    def test_parse_raw_query_params_url_encoded_chars(self):
        raw_request = b"GET /?name=test%20name&value=test%26value HTTP/1.1\r\nHost: localhost\r\n\r\n"
        # parse_raw_query_params itself does not unquote
        expected = {'name': 'test%20name', 'value': 'test%26value'}
        self.assertEqual(generate_user_credentials.parse_raw_query_params(raw_request), expected)

    def test_parse_raw_query_params_malformed_request_post(self):
        raw_request = b"POST /?code=test_code HTTP/1.1\r\nHost: localhost\r\n\r\n"
        expected = {} # Regex only matches GET
        self.assertEqual(generate_user_credentials.parse_raw_query_params(raw_request), expected)

    def test_parse_raw_query_params_malformed_request_no_space(self):
        raw_request = b"GET /?code=test_codeHTTP/1.1\r\nHost: localhost\r\n\r\n"
        expected = {} # Regex requires a space after query params part
        self.assertEqual(generate_user_credentials.parse_raw_query_params(raw_request), expected)

    @mock.patch('builtins.print')
    @mock.patch('sys.exit')
    @mock.patch('generate_user_credentials.parse_raw_query_params')
    @mock.patch('socket.socket')
    def test_get_authorization_code_success(self, mock_socket_class, mock_parse_params, mock_sys_exit, mock_print):
        # Configure socket mock
        mock_socket_instance = mock.Mock()
        mock_conn = mock.Mock()
        mock_socket_instance.accept.return_value = (mock_conn, ('127.0.0.1', 12345))
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance

        # Configure parse_raw_query_params mock
        mock_parse_params.return_value = {'code': 'test_auth_code', 'state': 'matching_state_token'}

        auth_code = generate_user_credentials.get_authorization_code('matching_state_token')

        self.assertEqual(auth_code, 'test_auth_code')
        mock_socket_instance.bind.assert_called_once_with(('localhost', 8080))
        mock_socket_instance.listen.assert_called_once_with(1)
        mock_socket_instance.accept.assert_called_once()
        mock_conn.recv.assert_called_once()
        mock_conn.sendall.assert_called_once() # Check that a response is sent
        # The exact content of sendall can be checked if necessary, e.g. mock_conn.sendall.assert_called_with(b"HTTP/1.1 200 OK\r\n...")
        mock_conn.close.assert_called_once()
        mock_sys_exit.assert_not_called()
        mock_print.assert_any_call("Authorization code received: test_auth_code")


    @mock.patch('builtins.print')
    @mock.patch('sys.exit')
    @mock.patch('generate_user_credentials.parse_raw_query_params')
    @mock.patch('socket.socket')
    def test_get_authorization_code_no_code_parameter(self, mock_socket_class, mock_parse_params, mock_sys_exit, mock_print):
        # Configure socket mock
        mock_socket_instance = mock.Mock()
        mock_conn = mock.Mock()
        mock_socket_instance.accept.return_value = (mock_conn, ('127.0.0.1', 12345))
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance

        # Configure parse_raw_query_params mock
        mock_parse_params.return_value = {'error': 'some_error', 'state': 'matching_state_token'}

        generate_user_credentials.get_authorization_code('matching_state_token')

        mock_socket_instance.bind.assert_called_once_with(('localhost', 8080))
        mock_socket_instance.listen.assert_called_once_with(1)
        mock_socket_instance.accept.assert_called_once()
        mock_conn.recv.assert_called_once()
        # Check that a response is sent even in error cases before exit
        mock_conn.sendall.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_sys_exit.assert_called_once_with(1)
        mock_print.assert_any_call("Error: Could not retrieve authorization code. Query parameters: {'error': 'some_error', 'state': 'matching_state_token'}")


    @mock.patch('builtins.print')
    @mock.patch('sys.exit')
    @mock.patch('generate_user_credentials.parse_raw_query_params')
    @mock.patch('socket.socket')
    def test_get_authorization_code_state_mismatch(self, mock_socket_class, mock_parse_params, mock_sys_exit, mock_print):
        # Configure socket mock
        mock_socket_instance = mock.Mock()
        mock_conn = mock.Mock()
        mock_socket_instance.accept.return_value = (mock_conn, ('127.0.0.1', 12345))
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance

        # Configure parse_raw_query_params mock
        mock_parse_params.return_value = {'code': 'test_auth_code', 'state': 'mismatched_state_token'}

        generate_user_credentials.get_authorization_code('correct_state_token')

        mock_socket_instance.bind.assert_called_once_with(('localhost', 8080))
        mock_socket_instance.listen.assert_called_once_with(1)
        mock_socket_instance.accept.assert_called_once()
        mock_conn.recv.assert_called_once()
        # Check that a response is sent even in error cases before exit
        mock_conn.sendall.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_sys_exit.assert_called_once_with(1)
        mock_print.assert_any_call("Error: State token mismatch. Expected 'correct_state_token' but received 'mismatched_state_token'.")

    @mock.patch('builtins.print')
    @mock.patch('generate_user_credentials.get_authorization_code')
    @mock.patch('generate_user_credentials.Flow') # Patches the class
    @mock.patch('generate_user_credentials.hashlib.sha256')
    @mock.patch('generate_user_credentials.os.urandom')
    def test_main_default_scope(self, mock_os_urandom, mock_hashlib_sha256, MockFlowClass, mock_get_auth_code, mock_print):
        # Configure mocks
        mock_os_urandom.return_value = b'test_urandom_bytes_default'
        
        mock_sha256_instance = mock.Mock()
        mock_sha256_instance.hexdigest.return_value = 'predictable_state_default'
        mock_hashlib_sha256.return_value = mock_sha256_instance

        mock_get_auth_code.return_value = 'dummy_auth_code_default'

        mock_flow_instance = mock.Mock()
        mock_flow_instance.authorization_url.return_value = 'dummy_auth_url_default'
        # Simulate credentials object structure
        mock_credentials = mock.Mock()
        mock_credentials.refresh_token = 'test_refresh_token_default'
        mock_flow_instance.credentials = mock_credentials
        MockFlowClass.from_client_secrets_file.return_value = mock_flow_instance

        # Call the main function
        default_scopes = ['https://www.googleapis.com/auth/adwords']
        generate_user_credentials.main('client_secrets_default.json', default_scopes)

        # Assertions
        mock_os_urandom.assert_called_once_with(32)
        mock_hashlib_sha256.assert_called_once_with(b'test_urandom_bytes_default')
        mock_sha256_instance.hexdigest.assert_called_once()

        MockFlowClass.from_client_secrets_file.assert_called_once_with(
            'client_secrets_default.json',
            scopes=default_scopes,
            redirect_uri='http://localhost:8080/'
        )
        mock_flow_instance.authorization_url.assert_called_once_with(
            state='predictable_state_default',
            access_type="offline",
            prompt="consent"
        )
        mock_print.assert_any_call("Visit the following URL to authorize your application: dummy_auth_url_default")
        mock_get_auth_code.assert_called_once_with('predictable_state_default')
        mock_flow_instance.fetch_token.assert_called_once_with(code='dummy_auth_code_default')
        mock_print.assert_any_call("Your refresh token is: test_refresh_token_default")
        mock_print.assert_any_call(
            "Add this refresh token to your google-ads.yaml file: \n"
            "refresh_token: test_refresh_token_default"
        )

    @mock.patch('builtins.print')
    @mock.patch('generate_user_credentials.get_authorization_code')
    @mock.patch('generate_user_credentials.Flow') # Patches the class
    @mock.patch('generate_user_credentials.hashlib.sha256')
    @mock.patch('generate_user_credentials.os.urandom')
    def test_main_with_additional_scopes(self, mock_os_urandom, mock_hashlib_sha256, MockFlowClass, mock_get_auth_code, mock_print):
        # Configure mocks
        mock_os_urandom.return_value = b'test_urandom_bytes_additional'

        mock_sha256_instance = mock.Mock()
        mock_sha256_instance.hexdigest.return_value = 'predictable_state_additional'
        mock_hashlib_sha256.return_value = mock_sha256_instance
        
        mock_get_auth_code.return_value = 'dummy_auth_code_additional'

        mock_flow_instance = mock.Mock()
        mock_flow_instance.authorization_url.return_value = 'dummy_auth_url_additional'
        mock_credentials = mock.Mock()
        mock_credentials.refresh_token = 'test_refresh_token_additional'
        mock_flow_instance.credentials = mock_credentials
        MockFlowClass.from_client_secrets_file.return_value = mock_flow_instance

        # Call the main function
        additional_scopes = ['https://www.googleapis.com/auth/adwords', 'scope1', 'scope2']
        generate_user_credentials.main('client_secrets_additional.json', additional_scopes)

        # Assertions
        mock_os_urandom.assert_called_once_with(32)
        mock_hashlib_sha256.assert_called_once_with(b'test_urandom_bytes_additional')
        mock_sha256_instance.hexdigest.assert_called_once()

        MockFlowClass.from_client_secrets_file.assert_called_once_with(
            'client_secrets_additional.json',
            scopes=additional_scopes,
            redirect_uri='http://localhost:8080/'
        )
        mock_flow_instance.authorization_url.assert_called_once_with(
            state='predictable_state_additional',
            access_type="offline",
            prompt="consent"
        )
        mock_print.assert_any_call("Visit the following URL to authorize your application: dummy_auth_url_additional")
        mock_get_auth_code.assert_called_once_with('predictable_state_additional')
        mock_flow_instance.fetch_token.assert_called_once_with(code='dummy_auth_code_additional')
        mock_print.assert_any_call("Your refresh token is: test_refresh_token_additional")
        mock_print.assert_any_call(
            "Add this refresh token to your google-ads.yaml file: \n"
            "refresh_token: test_refresh_token_additional"
        )

if __name__ == '__main__':
    unittest.main()
