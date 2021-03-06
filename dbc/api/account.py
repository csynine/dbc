import json
import time
import tornado.web

from dbc.block import get_block_by_id, get_last_block
from dbc.sync import sync
from dbc import account
from dbc.options import get_options
options = get_options()

class Account(tornado.web.RequestHandler):
    def post(self):
        '''
        generate a private key
        '''
        pk_hex = account.gen_private_key()
        self.write(pk_hex)

    def get(self, pk_hex=''):
        sign_content = self.get_argument('sign_content', '')
        if pk_hex and (not sign_content):
            public_k_hex = account.get_public_key(pk_hex)
            addr = account.get_addr(public_k_hex)
            self.write({"public_key":public_k_hex, "address":addr})
        elif pk_hex and sign_content:
            self.write({"signout": account.sign(pk_hex, sign_content)})
        else:
            self.set_status(404)
