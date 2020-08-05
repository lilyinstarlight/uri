# address to listen on
addr = ('', 8000)

# log locations
log = '/var/log/uri/uri.log'
http_log = '/var/log/uri/http.log'

# template directory to use
import os.path
template = os.path.dirname(__file__) + '/html'

# where service is located
service = 'https://uri.lily.flowers'

# where store is located
store = 'https://store.lily.flowers'

# interval for storing redirections
interval = 604800  # 1 week
