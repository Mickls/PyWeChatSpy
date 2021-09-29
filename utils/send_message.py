from rpc_client_tools import RPCProxy

spy = RPCProxy()


def send_message(to_wx, content):
    spy.send_text(to_wx, content)
    # pass