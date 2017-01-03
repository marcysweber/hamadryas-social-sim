from completesimulation import SavannahSim, HamadryasSim
from multiprocessing import Process, Queue, JoinableQueue


class Runner(object):
    def run(self, class_name, duration, n_replicates):
        pass


class SerialRunner(Runner):
    def __init__(self, class_name, duration, n_replicates):
        self.class_name = class_name
        self.duration = duration
        self.n_replicates = n_replicates

    def run(self):
        ret = []
        for i in range(self.n_replicates):
            print "running replicate " + str(i) + " of " + str(self.n_replicates)
            ret.append(self.new_sim().run_simulation())
        return ret

    def new_sim(self):
        constructor = globals()[self.class_name]
        sim = constructor()
        sim.duration = self.duration
        return sim


def worker(in_q, out_q, new_sim_func):
    while True:
        ticket = in_q.get()
        try:
            out_q.put(new_sim_func().run_simulation())
            print "end of sim " + str(ticket)
        except ZeroDivisionError as e:
            print "Population went down to 0", e
        finally:
            in_q.task_done()


class ParallelRunner(SerialRunner):
    def __init__(self, class_name, duration, n_replicates, n_processes=2):
        self.n_processes = n_processes
        self.to_do_queue = JoinableQueue()
        self.done_queue = Queue()
        super(ParallelRunner, self).__init__(class_name, duration, n_replicates)

    def run(self):
        for i in range(self.n_replicates):
            self.to_do_queue.put(i)

        for i in range(self.n_processes):
            p = Process(target=worker, args=(self.to_do_queue, self.done_queue, self.new_sim))
            p.daemon = True
            p.start()

        print str(self.n_processes) + " processes launched"

        self.to_do_queue.join()

        ret = []
        while not self.done_queue.empty():
            ret.append(self.done_queue.get())

        return ret
