import time


class Stopwatch:
    stopped = False
  
    def __init__(self):
        self.start_time = None

    def start(self) -> None:
        self.stopped = False
        self.start_time = time.time()

    def reset(self) -> None:
        self.start()

    def stop(self) -> float:
        if self.start_time is None:
            raise ValueError("Stopwatch has not been started.")

        elapsed_time = self.get_elapsed()
        # self.start_time = None
        self.stopped = True

        return elapsed_time

    def get_elapsed(self) -> float:
        return time.time() - self.start_time

    def has_stopped(self) -> bool:
        return self.stopped