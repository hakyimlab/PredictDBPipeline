#! /usr/bin/env python

import os
import re
import sys

def relavent_logfiles(tis):
    """Generator yielding output relevant log file name"""
    p = 'build_' + tis + '_model_chr[1-9][0-9]?_pos_mod_100_[0-9][0-9]?\.o.*'
    for file in os.listdir("../joblogs/"):
        if re.match(p, file):
            yield file


def check_job_logs(tis):
    """Checks all log files for a tissue to make sure they turn out ok

    Makes sure the model script processed all genes it set out to"""
    
    nfiles = 0
    nprobs = 0
    for file in relavent_logfiles(tis):
        nfiles += 1
        with open('../joblogs/' + file, 'r') as lf:
            # Go to last line.
            for line in lf:
                pass
            nums = line.strip().split(' / ')
            assert len(nums) == 2
            if nums[0] != nums[1] and nums[1] == '0':
                nprobs +=1
                print "Problem with %s" % file
                print nums
                if nprobs > 20:
                    print "Too many problems"
                    print "%i files check so far" % nfiles
                    return
    print "%i files found" % nfiles
    print "All check out"

if __name__ == "__main__":
    check_job_logs(sys.argv[1])
