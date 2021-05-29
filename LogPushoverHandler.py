from logging.handlers import HTTPHandler
from logging import makeLogRecord


class LogPushoverHandler(HTTPHandler):
    priorities =    {
                    'DEBUG':    -2,
                    'INFO':     -1,
                    'WARNING':  -1,
                    'ERROR':    0,
                    'CRITICAL': 1
                    }
    def __init__(self, **kwargs):
        HTTPHandler.__init__(
                            self,
                            host = 'api.pushover.net',
                            url = '/1/messages.json',
                            method = 'POST',
                            secure = True
                            )
        self.params = kwargs
        if 'priorities' not in self.params:
            self.params['priorities'] = self.priorities

    def emit(self, record):
        record_dict = self.mapLogRecord(record)
        record_dict['priority'] = self.params['priorities'][record_dict['levelname']]
        record_dict['timestamp'] = record_dict['created']
        record_dict['message'] = self.format(record)
        for key, value in self.params.items():
            record_dict[key] = value
        record = makeLogRecord(record_dict)
        HTTPHandler.emit(self,record)
