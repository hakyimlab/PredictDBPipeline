#! /usr/bin/env python

import os
import re
import sys

def relavent_logfiles(jobs_dir):
    """Generator yielding output relevant log file name"""
    p = '.*_model_chr[1-9][0-9]?\.o.*'
    for file in os.listdir("../joblogs/" + jobs_dir):
        if re.match(p, file):
            yield file


def check_job_logs(jobs_dir):
    """Checks all log files in a jobs log directory to make sure they
    turn out ok.

    Makes sure the model script processed all genes it set out to"""
    
    nfiles = 0
    nprobs = 0
    for file in relavent_logfiles(jobs_dir):
        nfiles += 1
        if os.stat('../joblogs/' + jobs_dir + file).st_size == 0:
            # File is empty
            nprobs += 1
            print "%s is empty." % file
        with open('../joblogs/' + jobs_dir + file, 'r') as lf:
            # Go to last line.
            for line in lf:
                pass
            nums = line.strip().split(' / ')
            assert len(nums) == 2
            if nums[0] != nums[1] or nums[1] == '0':
                nprobs +=1
                print "Problem with %s" % file
                print nums
                if nprobs > 20:
                    print "Too many problems"
                    print "%i files check so far" % nfiles
                    return
    print "%i files found" % nfiles
    print "%i check out" % (nfiles - nprobs)

if __name__ == "__main__":
    check_job_logs(sys.argv[1])
