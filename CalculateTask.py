import queue
import threading


class CalculateTask(threading.Thread):

    def __init__(self, thread_id, start, end):
        super().__init__()
        self.thread_id = thread_id
        self.calculated_numbers : queue.LifoQueue = queue.LifoQueue(0)
        self.test_range = range(2, 9)
        self.range_to_search = range(start, end)
        self.setDaemon(True)
        self.running = True

    def run(self):
        for number in self.range_to_search:
            number_is_prime = True
            for testNumber in self.test_range:
                if testNumber != number and number % testNumber == 0:
                    number_is_prime = False
                    break
            if number_is_prime:
                self.insert_number(number)
        self.running = False

    def insert_number(self, number):
        self.calculated_numbers.put(number)

    def getName(self):
        return "Thread " + str(self.thread_id)
