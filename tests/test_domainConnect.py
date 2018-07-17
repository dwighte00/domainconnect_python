from unittest import TestCase
from domainconnect import DomainConnect

oneandone_config = \
    dict(
        PROVIDER_ID='1and1',
        TEST_DOMAIN='connect.domains',
        SYNC_URL='https://domainconnect.1and1.com/sync',
        ASYNC_URL='https://domainconnect.1and1.com/async',
        ASYNC_SERVICE_IN_PATH=False,
        API_URL='https://api.domainconnect.1and1.com',
        CLIENT_SECRET='cd$;CVZRj#B8C@o3o8E4v-*k2H7S%)'
    )

godaddy_config = \
    dict(
        PROVIDER_ID='GoDaddy',
        TEST_DOMAIN='cuco240714it.today',
        SYNC_URL='https://dcc.godaddy.com/manage',
        ASYNC_URL='https://dcc.godaddy.com/manage',
        ASYNC_SERVICE_IN_PATH=True,
        API_URL='https://domainconnect.api.godaddy.com',
        CLIENT_SECRET='DomainConnectGeheimnisSecretString'
    )

configs = [oneandone_config, godaddy_config]


class TestDomainConnect(TestCase):

    def test_get_domain_connect_template_sync_url(self):
        for i in configs:
            with self.subTest(i=i):
                TestDomainConnect._test_get_domain_connect_template_sync_url(i)

    @staticmethod
    def _test_get_domain_connect_template_sync_url(config: dict):

        dc = DomainConnect()

        # simple test sync
        res, error = dc.get_domain_connect_template_sync_url(config['TEST_DOMAIN'], "exampleservice.domainconnect.org",
                                                             "template1",
                                                             params={"IP": "132.148.25.185",
                                                                     "RANDOMTEXT": "shm:1531371203:Hejo"})
        print(res)
        assert (error is None), "There is an error returned: {}".format(error)
        assert (res == config['SYNC_URL']
                + '/v2/domainTemplates/providers/exampleservice.domainconnect.org/services/template1/apply?domain='
                + config['TEST_DOMAIN'] + '&host=&IP=132.148.25.185&RANDOMTEXT=shm%3A1531371203%3AHejo'),\
            "URL is different than expected"

        # simple test sync with host
        res, error = dc.get_domain_connect_template_sync_url("justatest." + config['TEST_DOMAIN'],
                                                             "exampleservice.domainconnect.org",
                                                             "template1",
                                                             params={"IP": "132.148.25.185",
                                                                     "RANDOMTEXT": "shm:1531371203:Hejo"})
        print(res)
        assert(error is None), "There is an error returned: {}".format(error)
        assert(res == config['SYNC_URL']
               + '/v2/domainTemplates/providers/exampleservice.domainconnect.org/services/template1/apply?domain='
               + config['TEST_DOMAIN'] + '&host=justatest&IP=132.148.25.185&RANDOMTEXT=shm%3A1531371203%3AHejo'), \
            "URL is different than expected"

        # simple test sync with host and redirect uri and scope
        res, error = dc.get_domain_connect_template_sync_url("justatest." + config['TEST_DOMAIN'],
                                                             "exampleservice.domainconnect.org",
                                                             "template1",
                                                             params={"IP": "132.148.25.185",
                                                                     "RANDOMTEXT": "shm:1531371203:Hejo"},
                                                             redirect_uri="http://google.com", state="{name=value}")
        print(res)
        assert(error is None), "There is an error returned: {}".format(error)
        assert(res == config['SYNC_URL']
               + '/v2/domainTemplates/providers/exampleservice.domainconnect.org/services/template1/apply?domain='
               + config['TEST_DOMAIN']
               + '&host=justatest&IP=132.148.25.185&RANDOMTEXT=shm%3A1531371203%3AHejo'
                 '&redirect_uri=http%3A%2F%2Fgoogle.com&state=%7Bname%3Dvalue%7D'), \
            "URL is different than expected"

        # simple test template does not exits
        res, error = dc.get_domain_connect_template_sync_url(config['TEST_DOMAIN'], "exampleservice.domainconnect.org",
                                                             "template_not_exists",
                                                             params={"IP": "132.148.25.185",
                                                                     "RANDOMTEXT": "shm:1531371203:Hejo"})
        print(res)
        assert (error is not None), "There is no error returned and was expected"
        assert (res is None), "There was no url expected and came: {}".format(res)

    def test_get_domain_config(self):
        for i in configs:
            with self.subTest(i=i):
                TestDomainConnect._test_get_domain_config(i)

    @staticmethod
    def _test_get_domain_config(config: dict):
        dc = DomainConnect()
        res, error = dc.get_domain_config('testhost.' + config['TEST_DOMAIN'])
        assert (error is None), 'There is an error returned'
        assert (res.domain_root == config['TEST_DOMAIN']), 'Domain root wrong: {}'.format(res.domain_root)
        assert (res.host == 'testhost'), 'Host not correct: {}'.format(res.host)
        assert (res.urlSyncUX == config['SYNC_URL']), 'urlSyncUX not correct: {}'.format(res.urlSyncUX)
        assert (res.urlAsyncUX == config['ASYNC_URL']), 'urlAsyncUX not correct: {}'.format(res.urlAsyncUX)
        assert (res.urlAPI == config['API_URL']), 'urlAPI not correct: {}'.format(res.urlAPI)
        assert (res.providerName == config['PROVIDER_ID']), 'providerName not correct: {}'.format(res.providerName)

    def test_get_domain_connect_template_async_url(self):
        for i in configs:
            with self.subTest(i=i):
                TestDomainConnect._test_get_domain_connect_template_async_url(i)

    @staticmethod
    def _test_get_domain_connect_template_async_url(config: dict) -> None:
        dc = DomainConnect()

        # simple test sync without host
        res, error = dc.get_domain_connect_template_async_url(config['TEST_DOMAIN'],
                                                              "exampleservice.domainconnect.org",
                                                              "template2",
                                                              params={"IP": "132.148.25.185",
                                                                      "RANDOMTEXT": "shm:1531371203:Hejo"},
                                                              redirect_uri="https://exampleservice.domainconnect.org/"
                                                                           "async_oauth_response",
                                                              state="{name=value}")
        print(res)
        assert(error is None), "There is an error returned: {}".format(error)
        assert(res.asyncConsentUrl == config['ASYNC_URL']
               + '/v2/domainTemplates/providers/exampleservice.domainconnect.org'
                 '?client_id=exampleservice.domainconnect.org&scope=template2&domain='
               + config['TEST_DOMAIN']
               + '&host=&IP=132.148.25.185&RANDOMTEXT=shm%3A1531371203%3AHejo'
                 '&redirect_uri=https%3A%2F%2Fexampleservice.domainconnect.org%2F'
                 'async_oauth_response&state=%7Bname%3Dvalue%7D'), \
            "URL is different than expected: {}".format(res)

        # simple test sync with host
        res, error = dc.get_domain_connect_template_async_url(
            "justatest." + config['TEST_DOMAIN'],
            "exampleservice.domainconnect.org", "template2",
            params={"IP": "132.148.25.185", "RANDOMTEXT": "shm:1531371203:Hejo"},
            redirect_uri="https://exampleservice.domainconnect.org/async_oauth_response",
            state="{name=value}")
        print(res)
        assert(error is None), "There is an error returned"
        assert(res.asyncConsentUrl == config['ASYNC_URL']
               + '/v2/domainTemplates/providers/exampleservice.domainconnect.org'
                 '?client_id=exampleservice.domainconnect.org&scope=template2&domain='
               + config['TEST_DOMAIN']
               + '&host=justatest&IP=132.148.25.185&RANDOMTEXT=shm%3A1531371203%3AHejo'
                 '&redirect_uri=https%3A%2F%2Fexampleservice.domainconnect.org%2F'
                 'async_oauth_response&state=%7Bname%3Dvalue%7D'), \
            "URL is different than expected: {}".format(res[0])

        # simple test template does not exits
        res, error = dc.get_domain_connect_template_async_url(
            config['TEST_DOMAIN'], "exampleservice.domainconnect.org",
            "template_not_exists",
            params={"IP": "132.148.25.185", "RANDOMTEXT": "shm:1531371203:Hejo"},
            redirect_uri="https://exampleservice.domainconnect.org/async_oauth_response")
        print(res)
        assert (error is not None), "There is no error returned and was expected"
        assert (res is None), "There was no url expected: {}".format(res.asyncConsentUrl)

    def test_get_domain_connect_async_open_browser(self):
        for i in configs:
            with self.subTest(i=i):
                TestDomainConnect._test_open_domain_connect_template_asynclink(i)

    @staticmethod
    def _test_open_domain_connect_template_asynclink(config: dict) -> None:
        params = {"IP": "132.148.25.185",
                  "RANDOMTEXT": "shm:1531371203:Hejo async"}

        dc: DomainConnect = DomainConnect()
        context, error = dc.open_domain_connect_template_asynclink(
            'asyncpage.' + config['TEST_DOMAIN'],
            'exampleservice.domainconnect.org',
            'template2', params=params,
            redirect_uri='https://exampleservice.domainconnect.org/async_oauth_response',
            service_id_in_path=config['ASYNC_SERVICE_IN_PATH'])

        assert (error is None), "Error occured: {}".format(error)

        code = input("Please enter code: ")
        context.code = code
        context.client_secret = config['CLIENT_SECRET']

        ctx, error = dc.get_async_token(context)
        assert (error is None), "Error occured: {}".format(error)
        assert (ctx.access_token is not None), 'Access token missing'
        assert (ctx.access_token_expires_in is not None), 'Access token expiration data missing'

        res, error = dc.apply_domain_connect_template_async(context, params=params)
        assert error is None, 'Error on apply: {}'.format(error)
        assert res == 'Success', 'Wrong result: {}'.format(res)
