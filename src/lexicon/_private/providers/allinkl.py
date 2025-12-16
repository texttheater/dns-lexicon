from urllib.parse import quote


import mechanicalsoup # type: ignore


from lexicon.interfaces import Provider as BaseProvider


def _q(s):
    """UTF-8 encode and URL-quote a string"""
    return quote(s.encode("UTF-8"))


class Provider(BaseProvider):

    @staticmethod
    def get_nameservers():
        return ["ns5.kasserver.com", "ns6.kasserver.com"]

    @staticmethod
    def configure_parser(parser):
        parser.add_argument("--username", help="KAS login")
        parser.add_argument("--password", help="KAS password")

    def authenticate(self):
        self.browser = mechanicalsoup.StatefulBrowser()
        self.browser.open("https://kasbeta.all-inkl.com/login")
        self.browser.select_form()
        self.browser["loginname"] = self._get_provider_option("username")
        self.browser["passwort"] = self._get_provider_option("password")
        self.browser.submit_selected().raise_for_status()

    def create_record(self, rtype, name, content):
        url = f"https://kasbeta.all-inkl.com/tools/dns-settings/create?zone={_q(self.domain)}&l={_q(self._get_provider_option('username'))}"
        self.browser.open(url)
        self.browser.select_form('form[method="post"]')
        self.browser["record_name"] = name
        self.browser["record_type"] = rtype
        self.browser["record_data"] = content
        self.browser.submit_selected().raise_for_status()

    def list_records(self, rtype=None, name=None, content=None):
        raise UnsupportedOperation()

    def update_record(self, identifier, rtype, name, content):
        raise UnsupportedOperation()

    def delete_record(self, identifier=None, rtype=None, name=None, content=None):
        raise UnsupportedOperation()
