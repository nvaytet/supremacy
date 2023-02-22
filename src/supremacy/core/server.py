from multiprocessing import Process

from xmlrpc.server import SimpleXMLRPCServer


class AiServer:

    def __init__(self, ai, number):

        self.number = number
        self.ai = ai
        self.ai.team = ai.creator
        self.ai.number = number
        self.port_number = 8000 + self.number
        self.server = SimpleXMLRPCServer(("localhost", self.port_number))
        print(f"Listening on port {self.port_number}...")
        self.server.register_function(self.run, f"run")
        self.server_process = Process(target=self.server.serve_forever)
        self.server_process.start()

    def run(self, *args, **kwargs):
        self.ai.run(*args, **kwargs)
