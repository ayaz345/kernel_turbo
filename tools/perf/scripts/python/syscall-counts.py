# system call counts
# (c) 2010, Tom Zanussi <tzanussi@gmail.com>
# Licensed under the terms of the GNU GPL License version 2
#
# Displays system-wide system call totals, broken down by syscall.
# If a [comm] arg is specified, only syscalls called by [comm] are displayed.

import os
import sys

sys.path.append(os.environ['PERF_EXEC_PATH'] + \
	'/scripts/python/Perf-Trace-Util/lib/Perf/Trace')

from perf_trace_context import *
from Core import *
from Util import syscall_name

usage = "perf script -s syscall-counts.py [comm]\n";

if len(sys.argv) > 2:
	sys.exit(usage)

for_comm = sys.argv[1] if len(sys.argv) > 1 else None
syscalls = autodict()

def trace_begin():
	print "Press control+C to stop and show the summary"

def trace_end():
	print_syscall_totals()

def raw_syscalls__sys_enter(event_name, context, common_cpu,
	common_secs, common_nsecs, common_pid, common_comm,
	id, args):
	if for_comm is not None:
		if common_comm != for_comm:
			return
	try:
		syscalls[id] += 1
	except TypeError:
		syscalls[id] = 1

def print_syscall_totals():
    if for_comm is not None:
	    print "\nsyscall events for %s:\n\n" % (for_comm),
    else:
	    print "\nsyscall events:\n\n",

    print "%-40s  %10s\n" % ("event", "count"),
    print "%-40s  %10s\n" % ("----------------------------------------", \
                                 "-----------"),

    for id, val in sorted(syscalls.iteritems(), key = lambda(k, v): (v, k), \
				  reverse = True):
	    print "%-40s  %10d\n" % (syscall_name(id), val),
