import threading
var = None


class Var:
    def __init__(self, cf):
        self.cf = cf
        self.data = dict()
        self.lock = threading.Lock()
        self.data['symbol_index'] = cf.get('config', 'symbol_index')
        self.data['monitor_time'] = cf.get('config', 'monitor_time')
        for i in range(5):
            self.data['symbol'+str(i)] = cf.get('config', 'symbol'+str(i))

    def __setitem__(self, key, value):
        with self.lock:
            self.data[key] = value

    def __getitem__(self, key):
        with self.lock:
            return self.data.get(key)

    def __delitem__(self, key):
        with self.lock:
            del self.data[key]

    def save(self):
        try:
            with self.lock:
                self.cf.set('config', 'symbol_index', str(self.data['symbol_index']))
                self.cf.set('config', 'monitor_time', str(self.data['monitor_time']))
                for i in range(5):
                    self.cf.set('config', 'symbol'+str(i), self.data['symbol'+str(i)])
                self.cf.write(open('config.ini', 'w'))
        except Exception as e:
            print(e)
            print(self.data['symbol_index'])


def init(cf):
    global var
    var = Var(cf)
