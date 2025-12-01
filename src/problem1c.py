import datetime
from enum import Enum
from typing import Set, Tuple


class Operation(Enum):
    VIEW_OWN_ACCOUNT_BALANCE = 'View your own account balance'
    VIEW_ANY_ACCOUNT_BALANCE = 'View any account balance'
    VIEW_OWN_INVESTMENT_PORTFOLIO = 'View your own investment portfolio'
    VIEW_ANY_INVESTMENT_PORTFOLIO = 'View any investment portfolio'
    MODIFY_OWN_INVESTMENT_PORTFOLIO = 'Modify your own investment portfolio'
    MODIFY_ANY_INVESTMENT_PORTFOLIO = 'Modify any investment portfolio'
    VIEW_FINANCIAL_ADVISOR_CONTACT_INFO = 'View Financial Advisor contact info'
    VIEW_FINANCIAL_PLANNER_CONTACT_INFO = 'View Financial Planner contact info'
    VIEW_MONEY_MARKET_INSTRUMENTS = 'View money market instruments'
    VIEW_PRIVATE_CONSUMER_INSTRUMENTS = 'View private consumer instruments'


class Role(Enum):
    CLIENT = 'Client'
    PREMIUM_CLIENT = 'Premium Client'
    EMPLOYEE = 'Employee'
    FINANCIAL_ADVISOR = 'Financial Advisor'
    FINANCIAL_PLANNER = 'Financial Planner'
    TELLER = 'Teller'


# Explicitely define allowable operations for each role
AUTHORIZATION_MATRIX: dict[Role, Set[Operation]] = {
    Role.CLIENT: {
        Operation.VIEW_OWN_ACCOUNT_BALANCE,
        Operation.VIEW_OWN_INVESTMENT_PORTFOLIO,
        Operation.VIEW_FINANCIAL_ADVISOR_CONTACT_INFO
    },
    Role.PREMIUM_CLIENT: {
        Operation.MODIFY_OWN_INVESTMENT_PORTFOLIO,
        Operation.VIEW_FINANCIAL_PLANNER_CONTACT_INFO
    },
    Role.EMPLOYEE: {
        Operation.VIEW_ANY_ACCOUNT_BALANCE,
        Operation.VIEW_ANY_INVESTMENT_PORTFOLIO
    },
    Role.FINANCIAL_ADVISOR: {
        Operation.MODIFY_ANY_INVESTMENT_PORTFOLIO,
        Operation.VIEW_PRIVATE_CONSUMER_INSTRUMENTS
    },
    Role.FINANCIAL_PLANNER: {
        Operation.MODIFY_ANY_INVESTMENT_PORTFOLIO,
        Operation.VIEW_MONEY_MARKET_INSTRUMENTS,
        Operation.VIEW_PRIVATE_CONSUMER_INSTRUMENTS
    },
    Role.TELLER: set()  # No unique permissions
}

FULL_DAY_START = datetime.time(0, 0, 0)
FULL_DAY_END = datetime.time(23, 59, 59)
BUSINESS_HOURS_START = datetime.time(9, 0, 0)
BUSINESS_HOURS_END = datetime.time(17, 0, 0)

# Explicitely define active times for each role
ROLE_ACTIVE_TIMES: dict[Role, Tuple[datetime.time, datetime.time]] = {
    Role.CLIENT: (FULL_DAY_START, FULL_DAY_END),
    Role.PREMIUM_CLIENT: (FULL_DAY_START, FULL_DAY_END),
    Role.EMPLOYEE: (FULL_DAY_START, FULL_DAY_END),
    Role.FINANCIAL_ADVISOR: (FULL_DAY_START, FULL_DAY_END),
    Role.FINANCIAL_PLANNER: (FULL_DAY_START, FULL_DAY_END),
    Role.TELLER: (BUSINESS_HOURS_START, BUSINESS_HOURS_END)
}


def get_authorized_operations(roles: Set[Role]) -> Set[Operation]:
    """
    Get the complete set of allowable operations, i.e., the union of operations
    associated with each active role (multi-role composition). By default, a
    user has no authorized_operations.
    """
    # Completely deny system access if a single role is inactive
    for role in roles:
        if not is_active(role):
            return set()

    # Grant permissions (union of all operations associated with each role)
    authorized_operations: Set[Operation] = set()
    for role in roles:
        authorized_operations.update(AUTHORIZATION_MATRIX[role])

    return authorized_operations


def is_active(role: Role) -> bool:
    """
    Check if a role (and its associated permissions) is currently active, i.e.,
    if a user with the specified role should have system access at this time.
    """
    start_time, end_time = ROLE_ACTIVE_TIMES[role]
    curr_time = datetime.datetime.now().time()
    return curr_time >= start_time and curr_time <= end_time


if __name__ == "__main__":
    import unittest
    from unittest.mock import patch
    import datetime as real_datetime

    class TestAccessControl(unittest.TestCase):
        def test_single_role_operations(self):
            actual = get_authorized_operations({Role.CLIENT})
            expected = {
                Operation.VIEW_OWN_ACCOUNT_BALANCE,
                Operation.VIEW_OWN_INVESTMENT_PORTFOLIO,
                Operation.VIEW_FINANCIAL_ADVISOR_CONTACT_INFO
            }
            self.assertEqual(actual, expected)

            actual = get_authorized_operations({Role.EMPLOYEE})
            expected = {
                Operation.VIEW_ANY_ACCOUNT_BALANCE,
                Operation.VIEW_ANY_INVESTMENT_PORTFOLIO
            }
            self.assertEqual(actual, expected)

        def test_multi_role_operations(self):
            actual = get_authorized_operations(
                {Role.CLIENT, Role.PREMIUM_CLIENT})
            expected = {
                Operation.VIEW_OWN_ACCOUNT_BALANCE,
                Operation.VIEW_OWN_INVESTMENT_PORTFOLIO,
                Operation.VIEW_FINANCIAL_ADVISOR_CONTACT_INFO,
                Operation.MODIFY_OWN_INVESTMENT_PORTFOLIO,
                Operation.VIEW_FINANCIAL_PLANNER_CONTACT_INFO
            }
            self.assertEqual(actual, expected)

            actual = get_authorized_operations(
                {Role.EMPLOYEE, Role.FINANCIAL_ADVISOR})
            expected = {
                Operation.VIEW_ANY_ACCOUNT_BALANCE,
                Operation.VIEW_ANY_INVESTMENT_PORTFOLIO,
                Operation.MODIFY_ANY_INVESTMENT_PORTFOLIO,
                Operation.VIEW_PRIVATE_CONSUMER_INSTRUMENTS
            }
            self.assertEqual(actual, expected)

            actual = get_authorized_operations(
                {Role.EMPLOYEE, Role.FINANCIAL_PLANNER})
            expected = {
                Operation.VIEW_ANY_ACCOUNT_BALANCE,
                Operation.VIEW_ANY_INVESTMENT_PORTFOLIO,
                Operation.MODIFY_ANY_INVESTMENT_PORTFOLIO,
                Operation.VIEW_MONEY_MARKET_INSTRUMENTS,
                Operation.VIEW_PRIVATE_CONSUMER_INSTRUMENTS
            }
            self.assertEqual(actual, expected)

        @patch('__main__.datetime.datetime')
        def test_active_role(self, mock_datetime):
            mock_datetime.now.return_value.time.return_value = real_datetime.time(
                9, 0, 0)  # 9:00:00 am
            actual = get_authorized_operations({Role.EMPLOYEE, Role.TELLER})
            expected = {
                Operation.VIEW_ANY_ACCOUNT_BALANCE,
                Operation.VIEW_ANY_INVESTMENT_PORTFOLIO
            }
            self.assertEqual(actual, expected)

            mock_datetime.now.return_value.time.return_value = real_datetime.time(
                12, 0, 0)  # 12:00:00 pm
            actual = get_authorized_operations({Role.EMPLOYEE, Role.TELLER})
            expected = {
                Operation.VIEW_ANY_ACCOUNT_BALANCE,
                Operation.VIEW_ANY_INVESTMENT_PORTFOLIO
            }
            self.assertEqual(actual, expected)

            mock_datetime.now.return_value.time.return_value = real_datetime.time(
                17, 0, 0)  # 5:00:00 pm
            actual = get_authorized_operations({Role.EMPLOYEE, Role.TELLER})
            expected = {
                Operation.VIEW_ANY_ACCOUNT_BALANCE,
                Operation.VIEW_ANY_INVESTMENT_PORTFOLIO
            }
            self.assertEqual(actual, expected)

        @patch('__main__.datetime.datetime')
        def test_inactive_role(self, mock_datetime):
            mock_datetime.now.return_value.time.return_value = real_datetime.time(
                8, 59, 59)  # 8:59:59 am
            actual = get_authorized_operations({Role.EMPLOYEE, Role.TELLER})
            expected = set()
            self.assertEqual(actual, expected)

            mock_datetime.now.return_value.time.return_value = real_datetime.time(
                20, 0, 0)  # 8:00:00 pm
            actual = get_authorized_operations({Role.EMPLOYEE, Role.TELLER})
            expected = set()
            self.assertEqual(actual, expected)

            mock_datetime.now.return_value.time.return_value = real_datetime.time(
                17, 0, 1)  # 5:00:01 pm
            actual = get_authorized_operations({Role.EMPLOYEE, Role.TELLER})
            expected = set()
            self.assertEqual(actual, expected)

    unittest.main()
