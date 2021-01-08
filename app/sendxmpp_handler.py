#!/usr/bin/env python3
# app/sendxmpp_handler.py

from logging import Handler
from os import popen


class SENDXMPPHandler(Handler):
    def __init__(
            self,
            logging_xmpp_server,
            logging_xmpp_sender,
            logging_xmpp_password,
            logging_xmpp_recipient,
            logging_xmpp_command,
            logging_xmpp_use_tls
    ):
        Handler.__init__(self)
        self.logging_xmpp_server = logging_xmpp_server
        self.logging_xmpp_sender = logging_xmpp_sender
        self.logging_xmpp_password = logging_xmpp_password
        self.logging_xmpp_recipient = logging_xmpp_recipient
        self.logging_xmpp_command = logging_xmpp_command
        self.logging_xmpp_use_tls = logging_xmpp_use_tls

    '''
    This works on Debian 10 with flask running under gunicorn3 as a systemd service, hack as necessary
    echo '<message>' | /usr/bin/sendxmpp -t -u <sender> -j <server> -p <password> <recipient@example.com>
    '''
    def emit(self, record):
        try:
            message = self.format(record)

            shell_command = "echo '{}' | {} -u {} -j {} -p {} {}".format(
                message,
                self.logging_xmpp_command,
                self.logging_xmpp_sender,
                self.logging_xmpp_server,
                self.logging_xmpp_password,
                self.logging_xmpp_recipient
            )
            if self.logging_xmpp_use_tls == '1':
                shell_command += ' -t'

            p = popen(shell_command, "w")
            status = p.close()
            if status:
                print("sendxmpp_handler exit status", status)

        except Exception:
            self.handleError(record)
