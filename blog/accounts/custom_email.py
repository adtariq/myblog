from django.core.mail.backends.smtp import EmailBackend


class GmailBackend(EmailBackend):
    def __init__(self, **kwargs):
        kwargs['host'] = 'smtp.gmail.com'
        kwargs['port'] = 587
        kwargs['use_tls'] = True
        kwargs['username'] = 'adtariq69@gmail.com'
        kwargs['password'] = 'Allahdit#2'

        super().__init__(**kwargs)