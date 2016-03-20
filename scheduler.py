#!/usr/bin/env python

"""A workload scheduler

This scheduler provide an interface for schedule and run jobs.

Feature:
	- Support both single and multi thread:
	- Use Thread.Timer between different thread, use sched.scheduler inside single thread.
	- Each Thread_ID represent a new thread.
	- Independent from action and arguments.

"""

__author__ 		= "Haipeng Guan"
__email__ 		= "guanhaipeng@gmail.com"

from threading import Timer
import time, sched
from datetime import datetime
from datetime import timedelta

class Scheduler(object):
	"""A workload scheduler.

	Attributes:
		sched_cache ({ID: [list]}): store job info.
		sched_queue ({ID: sched_queue}): a list of sched.scheduler instance
		timer_list [Timer]: a list of Timer instance.
		exec_time_cache ({ID: [datetime]}): store actual execution time
		time_scale_factor (float): factor used to scale execution time up/dowm
		starting_point (datetime): starting time point
		pending_jobs_size (int): unfinished job size

	"""
	def __init__(self, **kwargs):
		self.sched_cache = {}
		self.sched_queue = {}
		self.timer_list = []
		self.time_scale_factor = float(kwargs.get('time_scale_factor', 1.0))
		self.exec_time_cache = {}
		self.starting_point = None
		self.pending_jobs_size = 0


	def __start_timer(self, timer):
		timer.start()

	def __run_action(self, ID, action, argument):
		self.exec_time_cache[ID].append(datetime.now())
		self.pending_jobs_size -= 1
		return action(*argument)


	def add_job(self, thread_ID, delay, action, argument, priority=1):
		"""Add a new job

		Args:
			thread_ID (str): A new thread_ID will represent a new thread.
			delay, priority, action, argument: see: https://docs.python.org/2/library/sched.html
		"""
		if not thread_ID in self.sched_cache:
			self.sched_cache[thread_ID] = []
			self.exec_time_cache[thread_ID] = []
		self.sched_cache[thread_ID].append([delay, priority, action, argument])
		self.pending_jobs_size += 1

	def run(self):
		for ID in self.sched_cache:
			self.sched_queue[ID] = sched.scheduler(time.time, time.sleep)
			for elem in self.sched_cache[ID]:
				[delay, priority, action, argument] = elem
				self.sched_queue[ID].enter(delay*self.time_scale_factor+1.0, priority, self.__run_action, [ID, action, argument])
			self.timer_list.append(Timer(1.0, self.sched_queue[ID].run, []))
		self.start_dt = datetime.now() + timedelta(seconds=1.0)
		print 'starting time point: %s' % (self.start_dt)
		map(self.__start_timer, self.timer_list)

	def is_finish(self):
		return self.pending_jobs_size == 0

	def get_exec_time(self):
		return self.exec_time_cache

	def plot_exec_time(self, **kwargs):
		if not self.start_dt:
			raise RuntimeError('Execution uninitialized!')
		elif not self.is_finish():
			raise RuntimeError('Execution unfinished!')
		bins = int(kwargs.get('bins', 20))
		histtype = kwargs.get('histtype', 'step')
		xlabel = kwargs.get('xlabel', 'time (sec)')
		ylabel = kwargs.get('ylabel', '')
		title = kwargs.get('title', 'Execution Result')
		for ID in self.exec_time_cache:
			self.exec_time_cache[ID] = [(dt - self.start_dt).total_seconds() for dt in self.exec_time_cache[ID]]
		import matplotlib.pyplot as plt
		plt.hist(self.exec_time_cache.values(),
					bins=bins*len(self.exec_time_cache),
					label=self.exec_time_cache.keys(),
					histtype=histtype)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.title(title)
		plt.legend()
		plt.show()





# usage example:
def test():
	print '----------------------------------------------------'
	print 'This is a simple usage example:'
	print 'print 100 times datetime.now() fomr 0 to 15 seconds'
	print '----------------------------------------------------\n'

	def print_time(index=0):
		print '[%s] - %s' % (index, datetime.now())

	import numpy
	exec_time = numpy.random.uniform(0, 30, 100)

	s = Scheduler(time_scale_factor=0.5)
	for i in xrange(len(exec_time)):
		s.add_job('Default_ID', exec_time[i], print_time, [i])

	s.run()
	while not s.is_finish():
		time.sleep(1)
	s.plot_exec_time()


if __name__ == '__main__':
	test()
