# Garage
A collection of my experimental/funny/useful scripts.

* profiling.py
  - Used in [NoWog](https://github.com/ParinazAmeri/NoWog.git) projeck.
  - Extach operation infos from system.profile collection.
  - Display histogram of execution time of operations.
  - Usage:
  	- Read and edit configuration section in profiling.py
  	- run it without any args.
  - Dependencies: pymongo, matplotlib

* scheduler.py

	- Provide an interface for schedule and run jobs.
	- Support both single and multi thread.
	- Independent from action and arguments.
	- Store and plot execution time.
	- Simple usage example: in the code
	- Dependencies: Timer, sched, datetime
