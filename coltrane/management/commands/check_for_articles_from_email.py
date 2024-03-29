from base64 import b64decode
from datetime import datetime, date
from email.parser import FeedParser
from email.utils import parseaddr, parsedate
from optparse import make_option
import socket
import sys
import time
import pdb

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from coltrane.models import Resumen, MARKUP_HTML, MARKUP_MARKDOWN, MARKUP_REST, MARKUP_TEXTILE

MB_IMAP4 = 'IMAP4'
MB_POP3 = 'POP3'
ACCEPTABLE_TYPES = ('text/plain', 'text/html')

class MailboxHandler(object):

    def __init__(self, host, port, username, password, keyfile, certfile, ssl):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.keyfile = keyfile
        self.certfile = certfile
        self.ssl = ssl
        self._handle = None

        if self.port is None:
            if self.ssl:
                self.port = self.secure_port
            else:
                self.port = self.unsecure_port

    @staticmethod
    def get_handle(protocol, *args, **kwargs):
        """Returns an instance of a MailboxHandler based on the protocol"""

        if protocol == MB_IMAP4:
            return IMAPHandler(*args, **kwargs)
        elif protocol == MB_POP3:
            return POPHandler(*args, **kwargs)

        return None

    @property
    def secure_port(self):
        return -1

    @property
    def unsecure_port(self):
        return -1

    @property
    def handle(self):
        if not self._handle:
            self._handle = self.connect()

        return self._handle

    def parse_email(self, message):
        """Parses each email message"""

        fp = FeedParser()
        fp.feed(message)
        return fp.close()

    def connect(self):
        raise NotImplemented

    def fetch(self):
        raise NotImplemented

    def delete_messages(self, id_list):
        """Deletes a list of messages from the server"""

        for msg_id in id_list:
            self.delete_message(msg_id)

    def delete_message(self, msg_id):
        raise NotImplemented

    def disconnect(self):
        raise NotImplemented

class IMAPHandler(MailboxHandler):

    @property
    def secure_port(self):
        return 993

    @property
    def unsecure_port(self):
        return 143

    def connect(self):
        """Connects to and authenticates with an IMAP4 mail server"""

        import imaplib

        M = None
        try:
            if (self.keyfile and self.certfile) or self.ssl:
                M = imaplib.IMAP4_SSL(self.host, self.port, self.keyfile, self.certfile)
            else:
                M = imaplib.IMAP4(self.host, self.port)

            M.login(self.username, self.password)
            M.select()
        except socket.error, err:
            raise
        else:
            return M

    def fetch(self):
        """Fetches email messages from an IMAP4 server"""

        messages = {}

        typ, data = self.handle.search(None, 'ALL')
        for num in data[0].split():
            typ, data = self.handle.fetch(num, '(RFC822)')
            messages[num] = self.parse_email(data[0][1])

        return messages

    def delete_message(self, msg_id):
        """Deletes a message from the server"""

        self.handle.store(msg_id, '+FLAGS', '\\Deleted')

    def disconnect(self):
        """Closes the IMAP4 handle"""

        self.handle.expunge()
        self.handle.close()
        self.handle.logout()

class POPHandler(MailboxHandler):

    @property
    def secure_port(self):
        return 995

    @property
    def unsecure_port(self):
        return 110

    def connect(self):
        """Connects to and authenticates with a POP3 mail server"""

        import poplib

        M = None
        try:
            if (self.keyfile and self.certfile) or self.ssl:
                M = poplib.POP3_SSL(self.host, self.port, self.keyfile, self.certfile)
            else:
                M = poplib.POP3(self.host, self.port)

            M.user(self.username)
            M.pass_(self.password)
        except socket.error, err:
            raise
        else:
            return M

    def fetch(self):
        """Fetches email messages from a POP3 server"""

        messages = {}

        num = len(self.handle.list()[1])
        for i in range(num):
            message = '\n'.join([msg for msg in self.handle.retr(i + 1)[1]])
            messages[num] = self.parse_email(message)

        return messages

    def delete_message(self, msg_id):
        """Deletes a message from the server"""

        self.handle.dele(msg_id)

    def disconnect(self):
        """Closes the POP3 handle"""

        self.handle.quit()

class Command(BaseCommand):
    help = "Checks special e-mail inboxes for emails that should be posted as articles"

    option_list = BaseCommand.option_list + (
        make_option('--protocol', dest='protocol', default=MB_IMAP4, help='Protocol to use to check for email'),
        make_option('--host', dest='host', default=None, help='IP or name of mail server'),
        make_option('--port', dest='port', default=None, help='Port used to connect to mail server'),
        make_option('--keyfile', dest='keyfile', default=None, help='File containing a PEM formatted private key for SSL connections'),
        make_option('--certfile', dest='certfile', default=None, help='File containing a certificate chain for SSL connections'),
        make_option('--username', dest='username', default=None, help='Username to authenticate with mail server'),
        make_option('--password', dest='password', default=None, help='Password to authenticate with mail server'),
        make_option('--ssl', action='store_true', dest='ssl', default=False, help='Use to specify that the connection must be made using SSL'),
    )

    def log(self, message, level=2):
        if self.verbosity >= level:
            print message

    def handle(self, *args, **options):
        """Main entry point for the command"""

        # retrieve configuration options--give precedence to CLI parameters
        self.config = getattr(settings, 'ARTICLES_FROM_EMAIL', {})
        s = lambda k, d: self.config.get(k, d)

        protocol = options['protocol'] or s('protocol', MB_IMAP4)
        host = options['host'] or s('host', 'mail.yourhost.com')
        port = options['port'] or s('port', None)
        keyfile = options['keyfile'] or s('keyfile', None)
        certfile = options['certfile'] or s('certfile', None)
        username = options['username'] or s('user', None)
        password = options['password'] or s('password', None)
        ssl = options['ssl'] or s('ssl', False)

        self.verbosity = int(options.get('verbosity', 1))

        handle = None
        try:
            self.log('Creating mailbox handle')
            handle = MailboxHandler.get_handle(protocol, host, port, username, password, keyfile, certfile, ssl)

            self.log('Fetching messages')
            messages = handle.fetch()

            if len(messages):
                self.log('Creating articles')
                created = self.create_articles(messages)

                if len(created):
                    self.log('Deleting consumed messages')
                    handle.delete_messages(created)
                else:
                    self.log('No articles created')
            else:
                self.log('No messages fetched')
        except socket.error:
            self.log('Failed to communicate with mail server.  Please verify your settings.', 0)
        finally:
            if handle:
                try:
                    handle.disconnect()
                    self.log('Disconnected.')
                except socket.error:
                    # probably means we couldn't connect to begin with
                    pass

    def get_email_content(self, email):
        """Attempts to extract an email's content"""
        #pdb.set_trace()

        if email.is_multipart():
            self.log('Extracting email contents from multipart message')
            for subpart in email.walk():
                filename = subpart.get_filename()
                if filename:
                    self.log('Guardando anexo: %s' % filename)
                    print('Guardando anexo: %s' % filename)
                    data = subpart.get_payload(decode=True)
                    return data
                else:
                    if subpart.get_content_charset() == 'UTF-8':
                        data = subpart.get_payload(decode=True)
                        charset = subpart.get_content_charset('utf-8')
                        return data

#            magic_type = 'multipart/alternative'
#            payload_types = dict((p.get_content_type(), i) for i, p in enumerate(email.get_payload()))
#            if magic_type in payload_types.keys():
#                self.log('Found magic content type: %s' % magic_type)
#                index = payload_types[magic_type]
#                payload = email.get_payload()[index].get_payload()
#            else:
#                payload = email.get_payload()
#
#            for pl in payload:
#                if pl.get_filename() is not None:
#                    # it's an attached file
#                    #if pl.get_content_type() in ACCEPTABLE_TYPES:
#                    return pl.get_payload(decode=True)
#                    #continue
#
#                #if pl.get_content_type() in ACCEPTABLE_TYPES:
#                #    return pl.get_payload()
        else:
            return email.get_payload()

        return None

#    def get_titulo(fecha_publicacion):
#        strfecha = str(fecha_publicacion)
#        dia = strfecha[8:]
#        mes = strfecha[5:7]
#        if dia == '01': strdia = '1'
#        elif dia == '02': strdia = '2'
#        elif dia == '03': strdia = '3'
#        elif dia == '04': strdia = '4'
#        elif dia == '05': strdia = '5'
#        elif dia == '06': strdia = '6'
#        elif dia == '07': strdia = '7'
#        elif dia == '08': strdia = '8'
#        elif dia == '09': strdia = '9'
#        if mes == '01': strmes = 'Enero'
#        elif mes == '02': strmes = 'Febrero'
#        elif mes == '03': strmes = 'Marzo'
#        elif mes == '04': strmes = 'Abril'
#        elif mes == '05': strmes = 'Mayo'
#        elif mes == '06': strmes = 'Junio'
#        elif mes == '07': strmes = 'Julio'
#        elif mes == '08': strmes = 'Agosto'
#        elif mes == '09': strmes = 'Septiembre'
#        elif mes == '10': strmes = 'Octubre'
#        elif mes == '11': strmes = 'Noviembre'
#        elif mes == '12': strmes = 'Diciembre'
#        return ("LPDH " + strdia + " de " + strmes + " de " + strfecha[0:4])
    def create_articles(self, emails):
        """Attempts to post new articles based on parsed email messages"""

        created = []
        site = Site.objects.get_current()

        ack = self.config.get('acknowledge', False)
        #autopost = self.config.get('autopost', False)

        # make sure we have a valid default markup
        markup = self.config.get('markup', MARKUP_HTML)
        if markup not in (MARKUP_HTML, MARKUP_MARKDOWN, MARKUP_REST, MARKUP_TEXTILE):
            markup = MARKUP_HTML

        for num, email in emails.iteritems():

            name, sender = parseaddr(email['From'])

            try:
                autor = User.objects.get(email=sender, is_active=True)
            except User.DoesNotExist:
                # unauthorized sender
                self.log('Not processing message from unauthorized sender.', 0)
                continue

            # get the attributes for the article
            #titulo = email.get('Subject', '--- article from email ---')
            fnumserial = open('/home/nacho/laprensadehoy/numserial','r')
            numero = fnumserial.readline()
            fnumserial.close()
            newnumero = int(numero) + 1
            num_serie = int(numero)
            strnewnumero = str(newnumero)
            fnumserial = open('/home/nacho/laprensadehoy/numserial','w')
            fnumserial.write(strnewnumero)
            fnumserial.close()

            contenido = self.get_email_content(email)
            try:
                # try to grab the timestamp from the email message
                #fecha_publicacion = datetime.fromtimestamp(time.mktime(parsedate(email['Date'])))
                fecha_publicacion2 = datetime.now()
                fecha_publicacion = date.today()
                strfecha = str(fecha_publicacion)
                dia = strfecha[8:]
                mes = strfecha[5:7]
                if dia == '01': strdia = '1'
                elif dia == '02': strdia = '2'
                elif dia == '03': strdia = '3'
                elif dia == '04': strdia = '4'
                elif dia == '05': strdia = '5'
                elif dia == '06': strdia = '6'
                elif dia == '07': strdia = '7'
                elif dia == '08': strdia = '8'
                elif dia == '09': strdia = '9'
                else : strdia = dia
                if mes == '01': strmes = 'Enero'
                elif mes == '02': strmes = 'Febrero'
                elif mes == '03': strmes = 'Marzo'
                elif mes == '04': strmes = 'Abril'
                elif mes == '05': strmes = 'Mayo'
                elif mes == '06': strmes = 'Junio'
                elif mes == '07': strmes = 'Julio'
                elif mes == '08': strmes = 'Agosto'
                elif mes == '09': strmes = 'Septiembre'
                elif mes == '10': strmes = 'Octubre'
                elif mes == '11': strmes = 'Noviembre'
                elif mes == '12': strmes = 'Diciembre'
                titulo = "LPDH " + strdia + " de " + strmes + " de " + strfecha[0:4]
                #titulo = get_titulo(fecha_publicacion)
            except StandardError, err:
                self.log("An error occurred when I tried to convert the email's timestamp into a datetime object: %s" % (err,))
                fecha_publicacion2 = datetime.now()
                fecha_publicacion = date.today()
                strfecha = str(fecha_publicacion)
                dia = strfecha[8:]
                mes = strfecha[5:7]
                if dia == '01': strdia = '1'
                elif dia == '02': strdia = '2'
                elif dia == '03': strdia = '3'
                elif dia == '04': strdia = '4'
                elif dia == '05': strdia = '5'
                elif dia == '06': strdia = '6'
                elif dia == '07': strdia = '7'
                elif dia == '08': strdia = '8'
                elif dia == '09': strdia = '9'
                else : strdia = dia
                if mes == '01': strmes = 'Enero'
                elif mes == '02': strmes = 'Febrero'
                elif mes == '03': strmes = 'Marzo'
                elif mes == '04': strmes = 'Abril'
                elif mes == '05': strmes = 'Mayo'
                elif mes == '06': strmes = 'Junio'
                elif mes == '07': strmes = 'Julio'
                elif mes == '08': strmes = 'Agosto'
                elif mes == '09': strmes = 'Septiembre'
                elif mes == '10': strmes = 'Octubre'
                elif mes == '11': strmes = 'Noviembre'
                elif mes == '12': strmes = 'Diciembre'
                titulo = "LPDH " + strdia + " de " + strmes + " de " + strfecha[0:4]
                #titulo = get_titulo(fecha_publicacion)

            # post the article
            article = Resumen(
                autor=autor,
                titulo=titulo,
                num_serie=num_serie,
                contenido=contenido,
                #markup=markup,
                fecha_publicacion=fecha_publicacion2,
                status=1,
            )

            try:
                article.save()
                self.log('Article created.')
                created.append(num)
            except StandardError, err:
                # log it and move on to the next message
                self.log('Error creating article: %s' % (err,), 0)
                continue
#            else:
#
#                # handle attachments
#                if email.is_multipart():
#                    files = [pl for pl in email.get_payload() if pl.get_filename() is not None]
#                    for att in files:
#                        obj = Attachment(
#                            article=article,
#                            caption=att.get_filename(),
#                        )
#                        obj.attachment.save(obj.caption, ChunkyString(att.get_payload()))
#                        obj.save()
#
#                created.append(num)

            if ack:
                # notify the user when the article is posted
                subject = u'%s: %s' % (_("Article Posted"), titulo)
                message = _("""Your email (%(titulo)s) has been posted as an article on %(site_name)s.

    http://%(domain)s%(article_url)s""") % {
                    'titulo': titulo,
                    'site_name': site.name,
                    'domain': site.domain,
                    'article_url': article.get_absolute_url(),
                }

                self.log('Sending acknowledgment email to %s' % (autor.email,))
                autor.email_user(subject, message)

        return created

class ChunkyString(str):
    """Makes is possible to easily chunk attachments"""

    def chunks(self):
        i = 0
        decoded = b64decode(self)
        while True:
            l = i
            i += 1024
            yield decoded[l:i]

            if i > len(decoded):
                raise StopIteration

