import random, string, base64, json

from .core.database import User
from .core.FCrypto import WFLib

user = User()

class DataStruct(object):
    def __init__(self, d):
        if type(d)==dict:d=json.dumps(d)
        for k, v in json.loads(d).items():
            if isinstance(k, (list, tuple)):
                setattr(self, k, [DataStruct(x) if isinstance(x, dict) else x for x in v])
            else:
                setattr(self, k, DataStruct(v) if isinstance(v, dict) else v)

class FoxlyAPI:
    def __init__(self):
        self.wflib = WFLib("185.252.147.45:9999")
        self.email: str
        self.wflib.hash: str
        if user.get_session():self.wflib.hash = user.get_session().key_hash
        else: self.wflib.hash = ''.join(random.sample(string.ascii_letters+string.digits, 32))
    
    def send_data_to_server(self, data):
        self.wflib.send_data(data)

    def read_data_from_server(self):
        return DataStruct(self.wflib.read_data().decode())
    
    def get_session(self):
        return user.get_session()

    def send_code(self, email:str):
        data = self._make_request_data(
            'send_code',
            email=email,
            first_name="Test"
        )
        return self._send_and_read_data(data)
    
    def login(self, email:str, code:int):
        pub_key = open(f'keys/pub-system.pem', 'r').read()
        data = self._make_request_data(
            'login',
            email=email,
            code=code,
            first_name="NewUser",
            pub_key=base64.b64encode(pub_key.encode()).decode()
        )
        response_data = self._send_and_read_data(data)
        if response_data.status == 'succesfull':
            user.save_session(response_data.data)
            self.wflib.hash = user.get_session().key_hash
        return response_data
    
    def get_me(self):
        data = self._make_request_data(
            'get_me',
        )
        return self._send_and_read_data(data)
    
    def get_chats(self):
        data = self._make_request_data(
            'get_chats'
        )
        return self._send_and_read_data(data)
    
    def create_chat(self, chat_type, chat_name):
        data = self._make_request_data(
            'create_chat',
            chat_type=chat_type,
            chat_name=chat_name
        )
        return self._send_and_read_data(data)
    
    def _make_request_data(self, request_type, **kwargs):
        user_data = user.get_session()
        if user_data:return json.dumps({'type': request_type, 'hash': user_data.key_hash, 'token': user_data.token, **kwargs})
        else:return json.dumps({'type': request_type, **kwargs})
    
    def _send_and_read_data(self, data):
        self.send_data_to_server(data)
        return self.read_data_from_server()