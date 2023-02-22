from multiprocessing import Process, Queue

from xmlrpc.server import SimpleXMLRPCServer


class Playergroup:

    def __init__(self, players, number):

        self.number = number
        self.server = SimpleXMLRPCServer(("localhost", 8000 + self.number))
        print("Listening on port 8000...")
        self.server.register_function(self.run, f"run_group{self.number}")
        self.server_process = Process(target=self.server.serve_forever)
        self.server_process.start()

    def run(self, *args, **kwargs):
        for player in self.players:
            player.ai.run(*args, **kwargs)
