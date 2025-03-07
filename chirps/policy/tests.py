"""Tests for the policy application."""

import re
from unittest import skip

from django.test import TestCase
from django.urls import reverse

from .forms import PolicyForm
from .models import Policy, Rule

cfixtures = ['policy/network.json']


def setUp(self):
    """Set up tests"""
    network_security_policy = Policy.objects.get(name='Network Security')
    current_policy_version = network_security_policy.current_version
    self.rules = Rule.objects.filter(policy=current_policy_version)
    self.test_string = 'Here is some network security information. The following {} is sensitive.'


def verify_pattern(self, rule_name, test_values, expected):
    """Verify test regex patterns."""
    rule = self.rules.get(name=rule_name)
    pattern = re.compile(rule.regex_test)

    for value in test_values:
        test_string = self.test_string.format(value)
        if expected:
            self.assertIsNotNone(pattern.search(test_string), value)
        else:
            self.assertIsNone(pattern.search(test_string), value)


def test_open_ports_pattern(self):
    """Verify that the Open Ports regex pattern matches valid port numbers."""
    valid_ports = ['80', '443', '22']
    self.verify_pattern('Open Ports', valid_ports, True)


def test_open_ports_pattern_invalid(self):
    """Verify that the Open Ports regex pattern does not match invalid port numbers."""
    invalid_ports = ['65536', 'abcd', '-1']
    self.verify_pattern('Open Ports', invalid_ports, False)


def test_firewall_configuration_pattern(self):
    """Verify that the Firewall Configuration regex pattern matches valid firewall rules."""
    valid_firewall_rules = [
        'allow from 192.168.1.1 to 10.0.0.1 port 80',
        'deny from any to 10.0.0.2 port any',
        'allow from 192.168.0.0 to any port 443',
    ]
    self.verify_pattern('Firewall Configuration', valid_firewall_rules, True)


def test_firewall_configuration_pattern_invalid(self):
    """Verify that the Firewall Configuration regex pattern does not match invalid firewall rules."""
    invalid_firewall_rules = [
        'allow from 192.168.1.1000 to 10.0.0.1 port 80',
        'deny from any to 10.0.0.2',
        'allow from 192.168.0.0 to any',
    ]
    self.verify_pattern('Firewall Configuration', invalid_firewall_rules, False)


def test_network_encryption_pattern(self):
    """Verify that the Network Encryption regex pattern matches valid encryption types."""
    valid_encryptions = ['none', 'WEP', 'WPA', 'WPA2', 'WPA3']
    self.verify_pattern('Network Encryption', valid_encryptions, True)


def test_network_encryption_pattern_invalid(self):
    """Verify that the Network Encryption regex pattern does not match invalid encryption types."""
    invalid_encryptions = ['WPA4', 'ABC', '123']
    self.verify_pattern('Network Encryption', invalid_encryptions, False)


def test_network_authentication_pattern(self):
    """Verify that the Network Authentication regex pattern matches valid authentication types."""
    valid_authentications = [
        'WEP',
        'WPA-PSK',
        'WPA2-PSK',
        'WPA3-PSK',
        'WPA-Enterprise',
        'WPA2-Enterprise',
        'WPA3-Enterprise',
    ]
    self.verify_pattern('Network Authentication', valid_authentications, True)


def test_network_authentication_pattern_invalid(self):
    """Verify that the Network Authentication regex pattern does not match invalid authentication types."""
    invalid_authentications = ['WPA4-PSK', 'WPA1-Enterprise', 'ABC', '123']
    self.verify_pattern('Network Authentication', invalid_authentications, False)


class StandardPIIRegexTests(TestCase):
    """Test rule regex"""

    fixtures = ['policy/standard_pii.json']

    def setUp(self):
        """Set up tests"""
        standard_pii_policy = Policy.objects.get(name='Standard PII')
        current_policy_version = standard_pii_policy.current_version
        self.rules = Rule.objects.filter(policy=current_policy_version)
        self.test_string = 'Here is some information. The following {} is sensitive.'

    def verify_pattern(self, rule_name, test_values, expected):
        """Verify test regex patterns."""
        rule = self.rules.get(name=rule_name)
        pattern = re.compile(rule.regex_test)

        for value in test_values:
            test_string = self.test_string.format(value)
            if expected:
                self.assertIsNotNone(pattern.search(test_string), value)
            else:
                self.assertIsNone(pattern.search(test_string), value)

    def test_ssn_pattern(self):
        """Verify that the SSN regex pattern matches valid SSN numbers."""
        valid_ssn_numbers = ['123-45-6789', '987-65-4321', '001-23-4567']
        self.verify_pattern('SSN', valid_ssn_numbers, True)

    def test_ssn_pattern_invalid(self):
        """Verify that the SSN regex pattern does not match invalid SSN numbers."""
        invalid_ssn_numbers = ['123-45-678', '987-65-432A', '001-23-45 67']
        self.verify_pattern('SSN', invalid_ssn_numbers, False)

    def test_california_drivers_license_pattern(self):
        """Verify that the California driver's license pattern matches valid DL numbers"""
        valid_numbers = ['A1234567', 'Z7654321']
        self.verify_pattern("California Driver's License", valid_numbers, True)

    def test_california_drivers_license_pattern_invalid(self):
        """Verify that the California driver's license pattern matches valid DL numbers"""
        invalid_numbers = ['1234567A', '7654321Z']
        self.verify_pattern("California Driver's License", invalid_numbers, False)

    def test_uk_drivers_license_pattern(self):
        """Verify that the UK driver's license pattern matches valid DL numbers"""
        valid_numbers = ['ABCDE123456FG7HI', 'WXYZA987654JK5LM']
        self.verify_pattern("United Kingdom Driver's License", valid_numbers, True)

    def test_uk_drivers_license_pattern_invalid(self):
        """Verify that the UK driver's license pattern does not match invalid DL numbers"""
        invalid_numbers = ['ABCDE123456FGHIL', 'WXYZA987654JKLM5']
        self.verify_pattern("United Kingdom Driver's License", invalid_numbers, False)

    def test_uk_passport_number_pattern(self):
        """Verify that the UK passport number pattern does not match invalid passport numbers"""
        valid_numbers = ['1234567890GBR1234567U987654321', '0987654321GBP6543210F123456789']
        self.verify_pattern('United Kingdom Passport Number', valid_numbers, True)

    def test_uk_passport_number_pattern_invalid(self):
        """Verify that the UK passport number pattern does not match invalid passport numbers"""
        invalid_numbers = ['1234567890GB1234567U987654321', '0987654321GBP6543210X123456789']
        self.verify_pattern('United Kingdom Passport Number', invalid_numbers, False)

    def test_individual_taxpayer_identification_number_pattern(self):
        """Verify that the ITIN pattern matches valid ITIN numbers"""
        valid_numbers = ['912-78-1234', '987 81 5678']
        self.verify_pattern('Individual Taxpayer Identification Number', valid_numbers, True)

    def test_individual_taxpayer_identification_number_pattern_invalid(self):
        """Verify that the ITIN pattern does not match invalid ITIN numbers"""
        invalid_numbers = ['912-68-1234', '987 91 5678']
        self.verify_pattern('Individual Taxpayer Identification Number', invalid_numbers, False)

    def test_email_pattern(self):
        """Verify that the Email Addresses regex pattern matches valid email addresses."""
        valid_email_addresses = ['example@example.com', 'test.user@domain.co.uk', 'user+tag@example.org']
        self.verify_pattern('Email Addresses', valid_email_addresses, True)

    def test_email_pattern_invalid(self):
        """Verify that the Email Addresses regex pattern does not match invalid email addresses."""
        invalid_email_addresses = ['example@example', 'test.user@domain', 'user+tag@example@org']
        self.verify_pattern('Email Addresses', invalid_email_addresses, False)

    def test_phone_number_pattern(self):
        """Verify that the Phone Numbers regex pattern matches valid phone numbers."""
        valid_phone_numbers = ['123-456-7890', '987-654-3210', '555-123-4567']
        self.verify_pattern('Phone Numbers', valid_phone_numbers, True)

    def test_phone_number_pattern_invalid(self):
        """Verify that the Phone Numbers regex pattern does not match invalid phone numbers."""
        invalid_phone_numbers = ['123-45-6789', '987-65-432A', '001-23-45 67']
        self.verify_pattern('Phone Numbers', invalid_phone_numbers, False)

    def test_address_pattern(self):
        """Verify that the Address regex pattern matches valid addresses."""
        valid_addresses = [
            '123 Main Street, Los Angeles, CA 90001',
            '987 Elm Avenue, New York, NY 10001',
            '001 Oak Court, San Francisco, CA 94102',
        ]
        self.verify_pattern('Address', valid_addresses, True)

    def test_address_pattern_invalid(self):
        """Verify that the Address regex pattern does not match invalid addresses."""
        invalid_addresses = [
            '123 Main Street, Los Angeles, CA',
            '987 Elm Avenue, New York 10001',
            '001 Oak Court, San Francisco 94102',
        ]
        self.verify_pattern('Address', invalid_addresses, False)


class FinanceRegexTests(TestCase):
    """Test rule regex"""

    fixtures = ['policy/finance.json']

    def setUp(self):
        """Set up tests"""
        finance_policy = Policy.objects.get(name='Finance')
        current_policy_version = finance_policy.current_version
        self.rules = Rule.objects.filter(policy=current_policy_version)
        self.test_string = 'Here is some information. The following {} is sensitive.'

    def verify_pattern(self, rule_name, test_values, expected):
        """Verify regex patterns."""
        rule = self.rules.get(name=rule_name)
        pattern = re.compile(rule.regex_test)

        for value in test_values:
            test_string = self.test_string.format(value)
            if expected:
                self.assertIsNotNone(pattern.search(test_string), value)
            else:
                self.assertIsNone(pattern.search(test_string), value)

    def test_citibank_routing_number_pattern(self):
        """Verify that the routing number regex pattern matches valid routing numbers."""
        valid_routing_numbers = ['321171184', '322271724']
        self.verify_pattern('Citibank Routing Number - California', valid_routing_numbers, True)

    def test_citibank_routing_number_pattern_invalid(self):
        """Verify that the routing number regex pattern matches valid routing numbers."""
        invalid_routing_numbers = ['321271184', '322171728']
        self.verify_pattern('Citibank Routing Number - California', invalid_routing_numbers, False)

    def test_bank_of_america_routing_number_pattern(self):
        """Verify that the routing number regex pattern matches valid routing numbers."""
        valid_routing_numbers = ['121009358', '026009593']
        self.verify_pattern('Bank of America Routing Number - California', valid_routing_numbers, True)

    def test_bank_of_america_routing_number_pattern_invalid(self):
        """Verify that the routing number regex pattern matches valid routing numbers."""
        invalid_routing_numbers = ['121019358', '026009594']
        self.verify_pattern('Bank of America Routing Number - California', invalid_routing_numbers, False)

    def test_chase_routing_number_pattern(self):
        """Verify that the routing number regex pattern matches valid routing numbers."""
        valid_routing_number = [322271627]
        self.verify_pattern('Chase Routing Number - California', valid_routing_number, True)

    def test_chase_routing_number_pattern_invalid(self):
        """Verify that the routing number regex pattern matches valid routing numbers."""
        invalid_routing_numbers = ['322271628', '222271627']
        self.verify_pattern('Chase Routing Number - California', invalid_routing_numbers, False)

    def test_bank_account_pattern(self):
        """Verify that the Bank Account Numbers regex pattern matches valid bank account numbers."""
        valid_bank_account_numbers = ['123-4567-8901234', '987-1234-5678901', '001-2345-6789012']
        self.verify_pattern('Bank Account', valid_bank_account_numbers, True)

    def test_bank_account_pattern_invalid(self):
        """Verify that the Bank Account regex pattern does not match invalid bank account numbers."""
        invalid_bank_account_numbers = ['123-456-78901234', '987-1234-56789A1', '001-2345-6789 012']
        self.verify_pattern('Bank Account', invalid_bank_account_numbers, False)

    def test_credit_card_pattern(self):
        """Verify that the Credit Card Numbers regex pattern matches valid credit card numbers."""
        valid_credit_cards = ['1234 5678 9012 3456', '9876-5432-1098-7654', '0011223344556677']
        self.verify_pattern('Credit Card', valid_credit_cards, True)

    def test_credit_card_pattern_invalid(self):
        """Verify that the Credit Card Numbers regex pattern does not match invalid credit card numbers."""
        invalid_credit_cards = ['1234 5678 9012', '9876-5432-1098 765A', '001122334455 667']
        self.verify_pattern('Credit Card', invalid_credit_cards, False)


class HealthRegexTests(TestCase):
    """Test rule regex"""

    fixtures = ['policy/health.json']

    def setUp(self):
        """Set up tests"""
        health_policy = Policy.objects.get(name='Health')
        current_policy_version = health_policy.current_version
        self.rules = Rule.objects.filter(policy=current_policy_version)
        self.test_string = 'Here is some information. The following {} is sensitive.'

    def verify_pattern(self, rule_name, test_values, expected):
        """Verify test regex patterns."""
        rule = self.rules.get(name=rule_name)
        pattern = re.compile(rule.regex_test)

        for value in test_values:
            test_string = self.test_string.format(value)
            if expected:
                self.assertIsNotNone(pattern.search(test_string), value)
            else:
                self.assertIsNone(pattern.search(test_string), value)

    def test_drug_code_pattern(self):
        """Verify that the regex pattern matches valid HIPAA PHI National Drug Code numbers."""
        valid_codes = ['1234-567-89', '12345-1234-12']
        self.verify_pattern('HIPAA PHI National Drug Code', valid_codes, True)

    def test_drug_code_pattern_invalid(self):
        """Verify that the regex pattern does not match invalid HIPAA PHI National Drug Code numbers."""
        invalid_codes = ['123-4567-89', '12345-12345-123']
        self.verify_pattern('HIPAA PHI National Drug Code', invalid_codes, False)


class CredentialsRegexTests(TestCase):
    """Test rule regex"""

    fixtures = ['policy/credentials.json']

    def setUp(self):
        """Set up tests"""
        credentials_policy = Policy.objects.get(name='Credentials')
        current_policy_version = credentials_policy.current_version
        self.rules = Rule.objects.filter(policy=current_policy_version)
        self.test_string = 'Here is some information. The following {} is sensitive.'

    def verify_pattern(self, rule_name, test_values, expected):
        """Verify test regex patterns."""
        rule = self.rules.get(name=rule_name)
        pattern = re.compile(rule.regex_test)

        for value in test_values:
            test_string = self.test_string.format(value)
            if expected:
                self.assertIsNotNone(pattern.search(test_string), value)
            else:
                self.assertIsNone(pattern.search(test_string), value)

    def test_facebook_access_token_pattern(self):
        """Verify that the Facebook regex pattern matches valid Facebook access tokens."""
        valid_tokens = ['EAACEdEose0cBA123abcXYZ', 'EAACEdEose0cBA987defMNO']
        self.verify_pattern('Facebook Access Token', valid_tokens, True)

    def test_facebook_access_token_pattern_invalid(self):
        """Verify that the Facebook regex pattern does not match invalid Facebook access tokens."""
        invalid_tokens = ['EAAEdEose0cBA123abcXYZ', 'EAACEdEose0cBA_123abc']
        self.verify_pattern('Facebook Access Token', invalid_tokens, False)

    def test_google_youtube_api_key_pattern(self):
        """Verify that the regex pattern matches valid Google Youtube API Keys."""
        valid_keys = ['AIza12345abcdeFGHIJklmnoPQRSTUvwxyz12345', 'AIza98765ABCDEfghijKLMNOqrstuvwxyz98765']
        self.verify_pattern('Google YouTube API Key', valid_keys, True)

    def test_google_youtube_api_key_pattern_invalid(self):
        """Verify that the regex pattern does not match invalid Google Youtube API Keys."""
        invalid_keys = ['AIza_12345abcdeFGHIJklmnoPQRSTUvwxyz12', 'AIZa12345abcdeFGHIJklmnoPQRSTUvwxyz12345']
        self.verify_pattern('Google YouTube API Key', invalid_keys, False)

    def test_twitter_access_token_pattern(self):
        """Verify that the regex pattern matches valid Twitter access tokens."""
        valid_tokens = [
            '12-1a2B3c4D5e6F7g8H9i0JkLmNoPQrStUvWxYzABCD1234567890',
            '45-0a1B2c3D4e5F6g7H8i9JKLMnOpQRsTuVwXyZ2345678901AbCd',
        ]
        self.verify_pattern('Twitter Access Token', valid_tokens, True)

    def test_twitter_access_token_pattern_invalid(self):
        """Verify that the regex pattern does not match invalid Twitter access tokens."""
        invalid_tokens = ['123-abcdefghijklmno', '9876-qrstuvwxyzabcde']
        self.verify_pattern('Twitter Access Token', invalid_tokens, False)

    def test_mailgun_api_key_pattern(self):
        """Verify that the regex pattern matches valid MailGun API keys."""
        valid_keys = ['key-12345abcdeFGHIJklmnoPQRSTUvwxyz123', 'key-98765ABCDEfghijKLMNOqrstuvwxyz987']
        self.verify_pattern('MailGun API Key', valid_keys, True)

    def test_mailgun_api_key_pattern_invalid(self):
        """Verify that the regex pattern does not match invalid MailGun API keys."""
        invalid_keys = ['key_12345abcdeFGHIJklmnoPQRSTUvwxyz123', 'key-12345abcdeFGHIJklmnoPQRSTU']
        self.verify_pattern('MailGun API Key', invalid_keys, False)

    def test_oauth_secret_pattern(self):
        """Verify that the regex pattern matches valid OAuth secrets."""
        valid_secrets = ['1a2b3c4d5e6F7G8H9I0JkLmN-OpQ_rStU', 'A1b2C3d4E5f6G7h8I9j0K_LmN-oPQrStU']
        self.verify_pattern('OAuth Secret', valid_secrets, True)

    def test_oauth_secret_pattern_invalid(self):
        """Verify that the regex pattern does not match invalid OAuth secrets."""
        invalid_secrets = ['123 abcXYZ-_456 defGHI', '123abcXYZ-_456defG']
        self.verify_pattern('OAuth Secret', invalid_secrets, False)

    def test_oauth_auth_code_pattern(self):
        """Verify that the regex pattern matches valid OAuth auth codes."""
        valid_codes = ['4/123abcXYZ-_', '4/987defMNO_-']
        self.verify_pattern('OAuth Auth Code', valid_codes, True)

    def test_oauth_auth_code_pattern_invalid(self):
        """Verify that the regex pattern does not match invalid OAuth auth codes."""
        invalid_codes = ['4_123abcXYZ-_', '4123 abcXYZ']
        self.verify_pattern('OAuth Auth Code', invalid_codes, False)

    def test_pgp_header_pattern(self):
        """Verify that the regex pattern matches valid PGP headers."""
        valid_headers = ['-----BEGIN PGP MESSAGE-----', '-----END PGP MESSAGE-----']
        self.verify_pattern('PGP Header', valid_headers, True)

    def test_pgp_header_pattern_invalid(self):
        """Verify that the regex pattern does not match invalid PGP headers."""
        valid_headers = ['----BEGIN PGP MESSAGE-----', '-----END PGP MESSAGE----']
        self.verify_pattern('PGP Header', valid_headers, False)


@skip('Disabling until pagination is re-added to the policy application.')
class PolicyPaginationTests(TestCase):
    """Test the policy application pagination."""

    fixtures = ['policy/employee.json', 'policy/network.json', 'policy/sensitive_data.json']

    def setUp(self):
        """Login the user before performing any tests."""
        self.client.post(
            reverse('signup'),
            {'username': 'admin', 'email': 'admin@mantiumai.com', 'password1': 'admin', 'password2': 'admin'},
        )

    def test_dashboard_no_pagination(self):
        """Verify that no pagination widget is displayed when there are less than 25 items."""
        response = self.client.get(reverse('policy_dashboard'))

        # No pagination widget should be present
        # Ensure the element ID is not found
        self.assertNotContains(response, 'chirps-pagination-widget', status_code=200)

        # All 3 scans should be present (look for the element IDs)
        for scan_id in ['100', '200', '300']:
            self.assertContains(response, f'chirps-policy-{scan_id}', status_code=200)

    def test_dashboard_pagination(self):
        """Verify that the 3 pages are available and that the pagination widget is displayed."""
        # First page
        response = self.client.get(reverse('policy_dashboard'), {'item_count': 1})
        self.assertContains(response, 'chirps-pagination-widget', status_code=200)
        self.assertContains(response, 'chirps-policy-100', status_code=200)

        # Second page
        response = self.client.get(reverse('policy_dashboard'), {'item_count': 1, 'page': 2})
        self.assertContains(response, 'chirps-pagination-widget', status_code=200)
        self.assertContains(response, 'chirps-policy-200', status_code=200)

        # Third page
        response = self.client.get(reverse('policy_dashboard'), {'item_count': 1, 'page': 3})
        self.assertContains(response, 'chirps-pagination-widget', status_code=200)
        self.assertContains(response, 'chirps-policy-300', status_code=200)

    def test_dashboard_last_page(self):
        """If the page number exceeds the number of pages, verify that the last page is returned"""
        response = self.client.get(reverse('policy_dashboard'), {'item_count': 1, 'page': 100})
        self.assertContains(response, 'chirps-pagination-widget', status_code=200)
        self.assertContains(response, 'chirps-policy-300', status_code=200)


class PolicyCreateForm(TestCase):
    """Test the custom logic in the policy create form."""

    def test_single_rule(self):
        """Verify that a single rule is parsed correctly."""
        rule_data = {
            'rule_name': 'Test Rule',
            'rule_query_string': 'Test Query String',
            'rule_regex': 'Test Regex',
            'rule_severity': 'Test Severity',
        }

        form = PolicyForm(
            data={
                'name': 'Test Policy',
                'description': 'Test Description',
                'rule_name_0': 'Test Rule',
                'rule_query_string_0': 'Test Query String',
                'rule_regex_0': 'Test Regex',
                'rule_severity_0': 'Test Severity',
            }
        )

        form.full_clean()
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.cleaned_data['rules']), 1)
        self.assertEqual(form.cleaned_data['rules'][0], rule_data)
