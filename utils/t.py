from threading import Thread


class Threads():
    def __init__(self, func, maxThreadNum=24, autoStart=False):
        self.func = func
        self.maxThreadNum = maxThreadNum
        self.threads = []
        self.autoStart = autoStart

    def add(self, *args, **kwargs):
        t = Thread(target=self.func, args=args, kwargs=kwargs)
        self.threads.append(t)
        if self.autoStart:
            t.start()
        if len(self.threads) == self.maxThreadNum:
            self.starAndJoin()

    def star(self):
        for t in self.threads:
            t.start()

    def join(self):
        if len(self.threads):
            self.threads[-1].join()
            self.threads = []

    def starAndJoin(self):
        self.star()
        self.join()
