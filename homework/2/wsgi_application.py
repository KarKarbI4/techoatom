from events import events

class WSGIApplication:
    def __init__(self, environment, start_response):
        print('Get request')
        # setup_testing_defaults(environment)
        self.environment = environment
        self.start_response = start_response
        self.events = events(10, 7)
        self.headers = [
            ('Content-type', 'text/plain; charset=utf-8')
        ]

    def __iter__(self):
        print('Wait for response')
        if self.environment.get('PATH_INFO', '/') == '/':
            r = next(self.events)
            if r:
                yield from self.ok_response(r)
            else:
                self.no_content_response()
        else:
            self.not_found_response()
        print('Done')

    def not_found_response(self):
        print('Create response')
        print('Send headers')
        self.start_response('404 Not Found', self.headers)
        print('Headers is sent')

    def no_content_response(self):
        print('Create response')
        print('Send headers')
        self.start_response('204 No Content', self.headers)
        print('Headers is sent')
        # print('Send body')

    def ok_response(self, message):
        print('Create response')
        print('Send headers')
        self.start_response('200 OK', self.headers)
        print('Headers is sent')
        print('Send body')
        yield message.encode('utf-8')
        print('Body is sent')