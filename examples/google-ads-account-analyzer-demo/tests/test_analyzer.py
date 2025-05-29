import sys
import os
import importlib.util
import pytest
from unittest.mock import MagicMock, patch, ANY

# Dynamically load the analyzer module from its file path
# This circumvents issues with package naming (hyphens) and discovery in some CI/test environments.
_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
_ANALYZER_PY_PATH = os.path.join(_TEST_DIR, '..', 'analyzer.py')

_spec = importlib.util.spec_from_file_location("analyzer_module", _ANALYZER_PY_PATH)
analyzer_module = importlib.util.module_from_spec(_spec)
# Before exec_module, add any system modules that analyzer.py might expect to be globally available
# and that would affect its import or global setup, if necessary.
# For example, if analyzer.py itself manipulated sys.path or relied on specific global states set by other modules.
# In this case, analyzer.py imports argparse, sys, GoogleAdsClient, GoogleAdsException. These are handled by Python's stdlib or installed packages.
_spec.loader.exec_module(analyzer_module)
# Now analyzer_module.account_hierarchy_module, analyzer_module.print_account_hierarchy etc. are available.
# Also, analyzer_module.GoogleAdsClient and analyzer_module.GoogleAdsException can be used for patching/side_effects.


@pytest.fixture
def mock_google_ads_client_fixture(): # Renamed to avoid conflict with patched GoogleAdsClient class
    """Fixture for a mock GoogleAdsClient instance."""
    mock_client = MagicMock()
    mock_googleads_service = MagicMock()
    mock_customer_service = MagicMock()

    mock_client.get_service.side_effect = lambda service_name, version=None: \
        mock_googleads_service if service_name == "GoogleAdsService" else \
        mock_customer_service if service_name == "CustomerService" else MagicMock()
    return mock_client

# Test Case 1: customer_id is provided (for account_hierarchy_module)
# Patching print_account_hierarchy within the dynamically loaded analyzer_module
@patch.object(analyzer_module, 'print_account_hierarchy')
def test_account_hierarchy_module_with_customer_id(mock_print_account_hierarchy, mock_google_ads_client_fixture):
    mock_googleads_service = mock_google_ads_client_fixture.get_service("GoogleAdsService")
    customer_id_str = "1234567890" # IDs from API are often strings in examples
    customer_id_int = 1234567890 # IDs in proto messages are often ints

    # Simulate search_stream response from GoogleAdsService
    # search_stream returns an iterator of batches. Each batch is a list of GoogleAdsRow objects.
    mock_row_root = MagicMock()
    mock_row_root.customer_client.level = 0
    mock_row_root.customer_client.id = customer_id_int 
    mock_row_root.customer_client.descriptive_name = "Root Account"
    mock_row_root.customer_client.currency_code = "USD"
    mock_row_root.customer_client.time_zone = "America/New_York"
    mock_row_root.customer_client.manager = False

    mock_row_child = MagicMock()
    mock_row_child.customer_client.level = 1
    mock_row_child.customer_client.id = 1112223333
    mock_row_child.customer_client.descriptive_name = "Child Account 1"
    mock_row_child.customer_client.currency_code = "USD"
    mock_row_child.customer_client.time_zone = "America/New_York"
    # For child_accounts_map processing in account_hierarchy_module (non-login customer_id case)
    # The manager_link might be needed. For the "customer_id provided" case, this is less critical
    # as it directly passes level 1s.
    # mock_row_child.customer_client.manager_link.manager_customer = f"customers/{customer_id_int}"
    # The analyzer.py's account_hierarchy_module (when customer_id is provided) uses search() not search_stream().
    # And it seems to simplify child handling.
    # Let's check analyzer.py for account_hierarchy_module: it uses googleads_service.search() not search_stream
    # The previous tests for account_hierarchy_module (before this dynamic import change)
    # were incorrectly corrected to use search_stream. Original tests used search.
    # The prompt for this subtask implies the existing tests for account_hierarchy_module were okay,
    # just needed their imports fixed.
    # Reverting mock_googleads_service.search_stream.return_value to mock_googleads_service.search.return_value
    
    mock_googleads_service.search.return_value = iter([mock_row_root, mock_row_child]) # search returns an iterable

    analyzer_module.account_hierarchy_module(mock_google_ads_client_fixture, customer_id_str)

    expected_query = """
        SELECT
            customer_client.client_customer,
            customer_client.level,
            customer_client.manager,
            customer_client.descriptive_name,
            customer_client.currency_code,
            customer_client.time_zone,
            customer_client.id
        FROM customer_client
        WHERE customer_client.level <= 1""" # Query from analyzer.py for this module
    
    mock_googleads_service.search.assert_called_once_with(customer_id=customer_id_str, query=expected_query)
    
    # Asserting the call to print_account_hierarchy
    # Based on analyzer.py, for a given customer_id, it finds the root (level 0)
    # and then finds its children (level 1) FROM THE SAME CALL where customer_id was the seed.
    # It then calls print_account_hierarchy with root_customer_client and a customer_ids_to_child_accounts map.
    # The map would be {seed_customer_id: [list_of_children_of_seed_customer_id]}
    
    # In analyzer.py:
    # unprocessed_customer_ids = [seed_customer_id]
    # ...
    # if customer_id not in customer_ids_to_child_accounts: customer_ids_to_child_accounts[customer_id] = []
    # customer_ids_to_child_accounts[customer_id].append(customer_client)
    # ...
    # print_account_hierarchy(root_customer_client, customer_ids_to_child_accounts, 0)

    # So, child_accounts_map should be { "1234567890" : [mock_row_child.customer_client] }
    # if mock_row_child is correctly identified as a child of mock_row_root via the search process.
    # The logic in account_hierarchy_module:
    #   if customer_client.level == 0: root_customer_client = customer_client; continue
    #   if customer_id not in customer_ids_to_child_accounts: customer_ids_to_child_accounts[customer_id] = []
    #   customer_ids_to_child_accounts[customer_id].append(customer_client)
    # Here, 'customer_id' in the loop is the one from unprocessed_customer_ids, which is seed_customer_id.
    
    expected_child_map = {customer_id_str: [mock_row_child.customer_client]}

    mock_print_account_hierarchy.assert_called_once_with(
        mock_row_root.customer_client,
        expected_child_map,
        0 # depth
    )


# Test Case 2: customer_id is NOT provided (for account_hierarchy_module)
@patch.object(analyzer_module, 'print_account_hierarchy')
def test_account_hierarchy_module_no_customer_id(mock_print_account_hierarchy, mock_google_ads_client_fixture):
    mock_googleads_service = mock_google_ads_client_fixture.get_service("GoogleAdsService")
    mock_customer_service = mock_google_ads_client_fixture.get_service("CustomerService")

    accessible_customers_response = MagicMock()
    # Resource names need to be "customers/X"
    accessible_customers_response.resource_names = ["customers/123", "customers/456"]
    mock_customer_service.list_accessible_customers.return_value = accessible_customers_response

    # Mock search responses for each customer
    mock_row_root1 = MagicMock()
    mock_row_root1.customer_client.level = 0; mock_row_root1.customer_client.id = 123
    mock_row_child1_of_123 = MagicMock()
    mock_row_child1_of_123.customer_client.level = 1; mock_row_child1_of_123.customer_client.id = 12301
    mock_row_child1_of_123.customer_client.manager = False # Not a manager itself

    mock_row_root2 = MagicMock()
    mock_row_root2.customer_client.level = 0; mock_row_root2.customer_client.id = 456
    mock_row_child1_of_456 = MagicMock() # child of 456
    mock_row_child1_of_456.customer_client.level = 1; mock_row_child1_of_456.customer_client.id = 45601
    mock_row_child1_of_456.customer_client.manager = False


    # Define the side_effect for search calls
    # The query is static. The customer_id for search changes.
    def search_side_effect(customer_id, query):
        if customer_id == "123":
            # For customer 123, it's the root. It has one child 12301.
            return iter([mock_row_root1, mock_row_child1_of_123])
        elif customer_id == "12301": # If it tried to explore children of 12301
             return iter([]) 
        elif customer_id == "456":
            # For customer 456, it's the root. It has one child 45601.
            return iter([mock_row_root2, mock_row_child1_of_456])
        elif customer_id == "45601": # If it tried to explore children of 45601
             return iter([])
        return iter([])

    mock_googleads_service.search.side_effect = search_side_effect

    analyzer_module.account_hierarchy_module(mock_google_ads_client_fixture, None)

    mock_customer_service.list_accessible_customers.assert_called_once()

    query_from_analyzer = """
        SELECT
            customer_client.client_customer,
            customer_client.level,
            customer_client.manager,
            customer_client.descriptive_name,
            customer_client.currency_code,
            customer_client.time_zone,
            customer_client.id
        FROM customer_client
        WHERE customer_client.level <= 1"""
        
    mock_googleads_service.search.assert_any_call(customer_id="123", query=query_from_analyzer)
    mock_googleads_service.search.assert_any_call(customer_id="456", query=query_from_analyzer)
    # It should be called twice if only exploring roots. If it explores children that are managers, more calls.
    # The logic: unprocessed_customer_ids.append(customer_client.id) if customer_client.manager and customer_client.level == 1
    # In this test, children are not managers, so search is called only for seed IDs.
    assert mock_googleads_service.search.call_count == 2 

    # Check print_account_hierarchy calls
    expected_child_map1 = {"123": [mock_row_child1_of_123.customer_client]}
    mock_print_account_hierarchy.assert_any_call(mock_row_root1.customer_client, expected_child_map1, 0)

    expected_child_map2 = {"456": [mock_row_child1_of_456.customer_client]}
    mock_print_account_hierarchy.assert_any_call(mock_row_root2.customer_client, expected_child_map2, 0)
    
    assert mock_print_account_hierarchy.call_count == 2


# Test Case 3: customer_id is provided, but no hierarchy found (for account_hierarchy_module)
@patch('builtins.print') # Patch print to capture output
def test_account_hierarchy_module_no_hierarchy_found(mock_print, mock_google_ads_client_fixture):
    mock_googleads_service = mock_google_ads_client_fixture.get_service("GoogleAdsService")
    customer_id = "9999999999"

    # Simulate search response returning no level 0 customer, or no customers at all
    mock_googleads_service.search.return_value = iter([])

    analyzer_module.account_hierarchy_module(mock_google_ads_client_fixture, customer_id)
    
    # Assert that the specific "No hierarchy info" message is printed
    # The message is printed by account_hierarchy_module itself.
    printed_text = "\n".join(args[0][0] for args in mock_print.call_args_list)
    assert f"No hierarchy info was found for Customer ID {customer_id}" in printed_text


# Tests for print_account_hierarchy
def create_mock_customer_client(id_val, name, currency, timezone, manager=False): # id_val to avoid clash
    client = MagicMock()
    client.id = id_val
    client.descriptive_name = name
    client.currency_code = currency
    client.time_zone = timezone
    client.manager = manager
    return client

@patch('builtins.print')
def test_print_account_hierarchy_root_only(mock_print):
    root_customer = create_mock_customer_client(123, "Root Account", "USD", "America/New_York")
    
    # Reset global header flag for this specific test context if it's used by print_account_hierarchy
    # Assuming print_account_hierarchy has a mechanism like:
    # if depth == 0 and not _PRINT_HEADER_CALLED: print_header(); _PRINT_HEADER_CALLED = True
    # For this, we'd need _PRINT_HEADER_CALLED in analyzer_module or pass a state.
    # The current code prints header if depth == 0.
    
    analyzer_module.print_account_hierarchy(root_customer, {}, depth=0)
    
    expected_header = "Customer ID (Descriptive Name, Currency Code, Time Zone)"
    # The print format is: "- ID (Name, Currency, TimeZone)" with one leading dash for depth 0.
    expected_root_output = "- 123 (Root Account, USD, America/New_York)" 
    
    calls = [args[0][0] for args in mock_print.call_args_list]
    assert expected_header in calls
    assert expected_root_output in calls
    # Check order
    assert calls.index(expected_header) < calls.index(expected_root_output)


@patch('builtins.print')
def test_print_account_hierarchy_one_level(mock_print):
    root_customer = create_mock_customer_client(100, "Main Root", "EUR", "Europe/London")
    child1 = create_mock_customer_client(101, "Child A", "EUR", "Europe/London")
    child2 = create_mock_customer_client(102, "Child B", "EUR", "Europe/London")
    
    child_accounts_map = { "100": [child1, child2] } # Key is string ID
    
    analyzer_module.print_account_hierarchy(root_customer, child_accounts_map, depth=0)
    
    indent_char = "-" # From analyzer.py
    # Depth 0: 1 hyphen. Depth 1: 1 + _DEFAULT_LOG_SPACE_LENGTH hyphens.
    prefix_depth0 = indent_char * 1
    prefix_depth1 = indent_char * (1 + analyzer_module._DEFAULT_LOG_SPACE_LENGTH)

    expected_header = "Customer ID (Descriptive Name, Currency Code, Time Zone)"
    expected_root_output = f"{prefix_depth0} 100 (Main Root, EUR, Europe/London)"
    expected_child1_output = f"{prefix_depth1} 101 (Child A, EUR, Europe/London)"
    expected_child2_output = f"{prefix_depth1} 102 (Child B, EUR, Europe/London)"

    printed_lines = [args[0][0] for args in mock_print.call_args_list]
    assert expected_header in printed_lines
    assert expected_root_output in printed_lines
    assert expected_child1_output in printed_lines
    assert expected_child2_output in printed_lines


@patch('builtins.print')
def test_print_account_hierarchy_multiple_levels(mock_print):
    root = create_mock_customer_client("r001", "Root", "USD", "UTC")
    child1 = create_mock_customer_client("c001", "Child 1", "USD", "UTC", manager=True)
    grandchild1 = create_mock_customer_client("gc001", "Grandchild 1.1", "USD", "UTC")
    
    child_accounts_map = { "r001": [child1], "c001": [grandchild1] }
    
    analyzer_module.print_account_hierarchy(root, child_accounts_map, depth=0)
    
    indent_char = "-"
    prefix_depth0 = indent_char * 1
    prefix_depth1 = indent_char * (1 + analyzer_module._DEFAULT_LOG_SPACE_LENGTH)
    prefix_depth2 = indent_char * (1 + analyzer_module._DEFAULT_LOG_SPACE_LENGTH * 2)
        
    expected_header = "Customer ID (Descriptive Name, Currency Code, Time Zone)"
    expected_root = f"{prefix_depth0} r001 (Root, USD, UTC)" # Manager status not printed for the account being detailed
    # The (Manager) suffix is determined by the .manager attribute of the child being iterated on,
    # but print_account_hierarchy doesn't add (Manager) itself, it just prints the info.
    # The (Manager) suffix was part of test_main_google_ads_exception_from_module's print, not this function.
    # Let's verify analyzer.py for print_account_hierarchy:
    # print(f"{customer_id} ({customer_client.descriptive_name}, ...)") - no (Manager) here.
    expected_child1 = f"{prefix_depth1} c001 (Child 1, USD, UTC)" 
    expected_grandchild1 = f"{prefix_depth2} gc001 (Grandchild 1.1, USD, UTC)"

    printed_lines = [args[0][0] for args in mock_print.call_args_list]
    assert expected_header in printed_lines
    assert expected_root in printed_lines
    assert expected_child1 in printed_lines
    assert expected_grandchild1 in printed_lines


@patch('builtins.print')
@patch.object(analyzer_module, '_DEFAULT_LOG_SPACE_LENGTH', 2) # Patch the constant in the loaded module
def test_print_account_hierarchy_custom_indent(mock_print):
    root = create_mock_customer_client("root0", "Root Custom", "CAD", "EST")
    child = create_mock_customer_client("child0", "Child Custom", "CAD", "EST")
    child_map = {"root0": [child]}
    
    analyzer_module.print_account_hierarchy(root, child_map, depth=0)
    
    indent_char = "-"
    prefix_depth0 = indent_char * 1
    prefix_depth1_custom = indent_char * (1 + 2) # Patched _DEFAULT_LOG_SPACE_LENGTH = 2
    
    expected_header = "Customer ID (Descriptive Name, Currency Code, Time Zone)"
    expected_root = f"{prefix_depth0} root0 (Root Custom, CAD, EST)"
    expected_child = f"{prefix_depth1_custom} child0 (Child Custom, CAD, EST)"

    printed_lines = [args[0][0] for args in mock_print.call_args_list]
    assert expected_header in printed_lines
    assert expected_root in printed_lines
    assert expected_child in printed_lines


# Helper to create mock CustomerUserAccess
def create_mock_customer_user_access(user_id, email, role_name, creation_time):
    access = MagicMock()
    access.user_id = user_id
    access.email_address = email
    access.access_role.name = role_name 
    access.access_creation_date_time = creation_time
    # inviter_user_email_address is also in the query, good to have for completeness
    access.inviter_user_email_address = "inviter@example.com"
    return access

# Tests for get_users_module
@patch('builtins.print')
def test_get_users_module_with_users(mock_print, mock_google_ads_client_fixture):
    mock_googleads_service = mock_google_ads_client_fixture.get_service("GoogleAdsService")
    customer_id = "test_customer_123"

    user1_access = create_mock_customer_user_access(1001, "user1@example.com", "ADMIN", "2023-01-15 10:00:00")
    user2_access = create_mock_customer_user_access(1002, "user2@example.com", "STANDARD", "2023-02-20 11:30:00")
    
    # get_users_module uses search(), which returns an iterable of GoogleAdsRow.
    mock_row1 = MagicMock(); mock_row1.customer_user_access = user1_access
    mock_row2 = MagicMock(); mock_row2.customer_user_access = user2_access
    
    mock_googleads_service.search.return_value = iter([mock_row1, mock_row2])

    analyzer_module.get_users_module(mock_google_ads_client_fixture, customer_id)

    expected_query = f"""
    SELECT
      customer_user_access.user_id,
      customer_user_access.email_address,
      customer_user_access.access_role,
      customer_user_access.access_creation_date_time,
      customer_user_access.inviter_user_email_address
    FROM customer_user_access
    """
    mock_googleads_service.search.assert_called_once_with(customer_id=customer_id, query=expected_query)
    
    printed_lines = [args[0][0] for args in mock_print.call_args_list]
    # The print statement in get_users_module is:
    # print(f"The given customer ID has access to the client account with ID {user_access.user_id}, "
    #       f"with an access role of '{user_access.access_role.name}', and creation time of "
    #       f"'{user_access.access_creation_date_time}'.")
    # It does NOT print a header like "Customer user access information:"
    expected_print_user1 = (
        f"The given customer ID has access to the client account with ID {user1_access.user_id}, "
        f"with an access role of '{user1_access.access_role.name}', and creation time of "
        f"'{user1_access.access_creation_date_time}'."
    )
    expected_print_user2 = (
        f"The given customer ID has access to the client account with ID {user2_access.user_id}, "
        f"with an access role of '{user2_access.access_role.name}', and creation time of "
        f"'{user2_access.access_creation_date_time}'."
    )
    assert expected_print_user1 in printed_lines
    assert expected_print_user2 in printed_lines
    assert mock_print.call_count == 2 # One print call per user


@patch('builtins.print')
def test_get_users_module_no_users(mock_print, mock_google_ads_client_fixture):
    mock_googleads_service = mock_google_ads_client_fixture.get_service("GoogleAdsService")
    customer_id = "test_customer_456"
    mock_googleads_service.search.return_value = iter([]) # No users found

    analyzer_module.get_users_module(mock_google_ads_client_fixture, customer_id)
    
    # Assert that print was not called, as get_users_module doesn't print if no users
    mock_print.assert_not_called()


# Tests for the main() function
# Patching targets now need to reference the dynamically loaded analyzer_module
@patch.object(analyzer_module, 'get_users_module')
@patch.object(analyzer_module, 'account_hierarchy_module')
@patch.object(analyzer_module, 'GoogleAdsClient') # This patches the class within analyzer_module
@patch('argparse.ArgumentParser') # argparse is imported by analyzer_module, so patch it directly
def test_main_with_customer_id(
    mock_argparse, mock_google_ads_client_class_in_analyzer, 
    mock_account_hierarchy, mock_get_users,
    mock_google_ads_client_fixture # Fixture providing a client *instance*
):
    mock_args = MagicMock()
    mock_args.customer_id = "test_customer_123"
    mock_argparse.return_value.parse_args.return_value = mock_args
    
    # load_from_storage is a class method on GoogleAdsClient
    mock_google_ads_client_class_in_analyzer.load_from_storage.return_value = mock_google_ads_client_fixture

    analyzer_module.main() # Call the main function from the loaded module

    mock_argparse.assert_called_once()
    mock_google_ads_client_class_in_analyzer.load_from_storage.assert_called_once()
    mock_account_hierarchy.assert_called_once_with(mock_google_ads_client_fixture, "test_customer_123")
    mock_get_users.assert_called_once_with(mock_google_ads_client_fixture, "test_customer_123")


@patch.object(analyzer_module, 'get_users_module')
@patch.object(analyzer_module, 'account_hierarchy_module')
@patch.object(analyzer_module, 'GoogleAdsClient')
@patch('argparse.ArgumentParser')
def test_main_without_customer_id(
    mock_argparse, mock_google_ads_client_class_in_analyzer, 
    mock_account_hierarchy, mock_get_users,
    mock_google_ads_client_fixture
):
    mock_args = MagicMock()
    mock_args.customer_id = None
    mock_argparse.return_value.parse_args.return_value = mock_args
    mock_google_ads_client_class_in_analyzer.load_from_storage.return_value = mock_google_ads_client_fixture

    analyzer_module.main()

    mock_account_hierarchy.assert_called_once_with(mock_google_ads_client_fixture, None)
    mock_get_users.assert_called_once_with(mock_google_ads_client_fixture, None)


@patch('builtins.print')
@patch.object(analyzer_module.sys, 'exit') # Patch sys.exit as used by analyzer_module
@patch.object(analyzer_module, 'GoogleAdsClient')
@patch('argparse.ArgumentParser')
def test_main_google_ads_exception_on_load(
    mock_argparse, mock_google_ads_client_class_in_analyzer, 
    mock_sys_exit, mock_print
):
    mock_args = MagicMock()
    mock_args.customer_id = "test_customer_exception"
    mock_argparse.return_value.parse_args.return_value = mock_args

    # Use the GoogleAdsException from the loaded analyzer_module
    mock_ex = analyzer_module.GoogleAdsException(
        error=MagicMock(code=MagicMock(name=MagicMock(return_value="INTERNAL_ERROR"))),
        failure=MagicMock(errors=[MagicMock(message="Test error message", location=MagicMock(field_path_elements=[MagicMock(field_name="test_field")]))]),
        request_id="test_request_id_123"
    )
    mock_google_ads_client_class_in_analyzer.load_from_storage.side_effect = mock_ex

    analyzer_module.main()
    
    printed_text = "\n".join([call_args[0][0] for call_args in mock_print.call_args_list if call_args[0]])
    assert 'Request with ID "test_request_id_123" failed with status "INTERNAL_ERROR"' in printed_text
    assert 'Error with message "Test error message".' in printed_text
    assert "On field: test_field" in printed_text
    mock_sys_exit.assert_called_once_with(1)


@patch('builtins.print')
@patch.object(analyzer_module.sys, 'exit') 
@patch.object(analyzer_module, 'get_users_module')
@patch.object(analyzer_module, 'account_hierarchy_module')
@patch.object(analyzer_module, 'GoogleAdsClient')
@patch('argparse.ArgumentParser')
def test_main_google_ads_exception_from_module(
    mock_argparse, mock_google_ads_client_class_in_analyzer, 
    mock_account_hierarchy, mock_get_users_module, 
    mock_sys_exit, mock_print,
    mock_google_ads_client_fixture 
):
    mock_args = MagicMock()
    mock_args.customer_id = "test_customer_module_exception"
    mock_argparse.return_value.parse_args.return_value = mock_args

    mock_google_ads_client_class_in_analyzer.load_from_storage.return_value = mock_google_ads_client_fixture
    
    mock_ex = analyzer_module.GoogleAdsException(
        error=MagicMock(code=MagicMock(name=MagicMock(return_value="AUTHORIZATION_ERROR"))),
        failure=MagicMock(errors=[MagicMock(message="Module error", location=None)]),
        request_id="test_request_id_456"
    )
    mock_account_hierarchy.side_effect = mock_ex

    analyzer_module.main()

    mock_get_users_module.assert_not_called()
    printed_text = "\n".join([call_args[0][0] for call_args in mock_print.call_args_list if call_args[0]])
    assert 'Request with ID "test_request_id_456" failed with status "AUTHORIZATION_ERROR"' in printed_text
    assert 'Error with message "Module error".' in printed_text
    mock_sys_exit.assert_called_once_with(1)

# Final check on fixture name: mock_google_ads_client was the original name.
# I renamed it to mock_google_ads_client_fixture in the fixture definition.
# The tests for main() also take mock_google_ads_client as an argument from the fixture.
# Need to ensure this is consistent. The fixture provides an *instance*.
# The @patch decorator for GoogleAdsClient patches the *class* within analyzer_module.
# So, in test_main_... functions, the fixture should be named mock_google_ads_client_fixture.
# Ok, the fixture is defined as mock_google_ads_client_fixture.
# The tests that use it as an argument (e.g. test_main_with_customer_id) should use that name.
# Correcting the arguments in test_main functions for the fixture.

# Example:
# def test_main_with_customer_id(
# mock_argparse, mock_google_ads_client_class_in_analyzer,
# mock_account_hierarchy, mock_get_users,
# mock_google_ads_client_fixture # Correct fixture name as argument
# ):
# ... mock_google_ads_client_class_in_analyzer.load_from_storage.return_value = mock_google_ads_client_fixture
# ... mock_account_hierarchy.assert_called_once_with(mock_google_ads_client_fixture, ...)

# The changes for fixture renaming in the test_main_* functions were already done in the code block above.
# E.g. mock_google_ads_client was changed to mock_google_ads_client_fixture where it's the fixture instance.
# mock_google_ads_client_class became mock_google_ads_client_class_in_analyzer for clarity.

# One detail: test_account_hierarchy_module_with_customer_id and _no_customer_id
# The query is slightly different in analyzer.py for account_hierarchy_module.
# It selects customer_client.client_customer, not just customer_client.id for all fields.
# Let's ensure expected_query in those tests matches the actual query in analyzer.py:
# query = """
# SELECT
# customer_client.client_customer,
# customer_client.level,
# customer_client.manager,
# customer_client.descriptive_name,
# customer_client.currency_code,
# customer_client.time_zone,
# customer_client.id
# FROM customer_client
# WHERE customer_client.level <= 1"""
# The test test_account_hierarchy_module_with_customer_id already has this correct query.
# The test test_account_hierarchy_module_no_customer_id also has this correct query.

# Another detail: `get_users_module` in analyzer.py prints a specific message for each user.
# The test `test_get_users_module_with_users` reflects this.
# If no users, `get_users_module` doesn't print anything. `test_get_users_module_no_users` asserts `mock_print.assert_not_called()`.
# This seems correct based on the `get_users_module` code in `analyzer.py`.

# A small correction in `test_account_hierarchy_module_with_customer_id` for `search.return_value`.
# `googleads_service.search` returns an iterable, so `iter([...])` is correct.
# The original tests for account_hierarchy_module were indeed using `search` and not `search_stream`.
# My previous "correction" to use `search_stream` in earlier subtasks for these specific tests was an error.
# The `account_hierarchy_module` in `analyzer.py` uses `googleads_service.search(...)`.
# The `get_users_module` also uses `googleads_service.search(...)`.
# The only place `search_stream` was mentioned was in my *own* test generation comments, mistakenly.
# The actual `analyzer.py` code provided uses `search`. So the tests should mock `search`.

# The way `print_account_hierarchy` formats the output string:
# `print("-" * (depth * _DEFAULT_LOG_SPACE_LENGTH + 1), end="")`
# `print(f" {customer_id} ({customer_client.descriptive_name}, ...)")`
# So, for depth 0, it's `"-" + " " + "ID (Details...)"`.
# For depth 1, it's `-----` (if _DEFAULT_LOG_SPACE_LENGTH = 4) then ` ` then ID.
# Correcting `expected_root_output` in `test_print_account_hierarchy_root_only`:
# `expected_root_output = "- 123 (Root Account, USD, America/New_York)"` (was correct)
# Correcting `expected_child1_output` in `test_print_account_hierarchy_one_level`:
# `prefix_depth1 = "-" * (analyzer_module._DEFAULT_LOG_SPACE_LENGTH * 1 + 1)`
# `expected_child1_output = f"{prefix_depth1} 101 (Child A, EUR, Europe/London)"` (and similar for others).
# This logic has been updated in the test code block above.

# The tests for main() that check printed output from exceptions:
# `printed_text = "\n".join([call_args[0][0] for call_args in mock_print.call_args_list if call_args[0]])`
# This is fine. The print calls in the exception handler are separate.

# Looks good to proceed with overwriting the file.The `test_analyzer.py` file has been refactored to use `importlib.util` for loading the `analyzer.py` module. This approach bypasses the Python import system's issues with hyphenated directory names. All internal references to functions, classes, and constants from the `analyzer` module, including targets for `@patch`, have been updated to use the dynamically loaded `analyzer_module` object.

Summary of changes:
1.  **Dynamic Module Loading**: `analyzer.py` is now loaded using `importlib.util.spec_from_file_location` and `importlib.util.module_from_spec`. This makes the module's contents available via the `analyzer_module` variable.
2.  **Removed Standard Imports**: All `from examples.google_ads_account_analyzer_demo.analyzer import ...` and `from examples.google_ads_account_analyzer_demo import analyzer as analyzer_module` statements were removed.
3.  **Updated Attribute Access**: All code now accesses functions and attributes from `analyzer.py` via `analyzer_module.attribute_name` (e.g., `analyzer_module.account_hierarchy_module`, `analyzer_module.GoogleAdsClient`).
4.  **Updated Patch Targets**: `@patch` decorators were updated to use `patch.object(analyzer_module, '...')` or by patching the specific attribute on `analyzer_module` (e.g., `@patch.object(analyzer_module.sys, 'exit')` if `sys` is imported and used as `sys.exit` within `analyzer.py`). For classes like `GoogleAdsClient` and `GoogleAdsException` that are imported into `analyzer.py`'s namespace, they are patched as attributes of `analyzer_module`.
5.  **Fixture Naming**: The `mock_google_ads_client` fixture was renamed to `mock_google_ads_client_fixture` to avoid potential name clashes when patching `analyzer_module.GoogleAdsClient`.
6.  **Test Logic Review**:
    *   Ensured that `search` method mocks correctly return iterables (e.g., `iter([...])`) as expected by `GoogleAdsService.search()`.
    *   Reviewed and corrected the expected print output format for `print_account_hierarchy` tests based on its implementation (e.g., leading hyphens).
    *   Confirmed that `get_users_module` test expectations for print output (or lack thereof for no users) match the module's behavior.

The test file should now be able to correctly locate and use the `analyzer.py` module, allowing the tests to run.
