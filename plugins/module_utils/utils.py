
idoit_argument_spec = dict(type="dict", required=True, options=dict(
    api_key=dict(type="str", required=True, no_log=True),
    user=dict(type="str", required=True),
    password=dict(type="str", required=True, no_log=True),
    jrpc_url=dict(type="str", required=True, no_log=True)
))
state_arguement_spec = dict(choices=['present', 'absent'], default='present')
