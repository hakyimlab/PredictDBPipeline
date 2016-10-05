#!/usr/bin/env python
import sys

import check_job_logs

p = '.*_model_chr[1-9][0-9]?_pos_mod_100_[0-9][0-9]?\.o.*'
check_job_logs.check_job_logs(sys.argv[1],p)
