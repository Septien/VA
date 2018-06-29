"""
Group all performance tests.
"""

import unittest
import pc_perf
import lp_perf
import pp_perf
import hist_perf
import scp_perf
import splom_perf

def masterSuite():
    """ """
    #---------------------------------------------------- csv 
    # pc
    suite = unittest.TestSuite()
    suite.addTest(pc_perf.PCElNinocsvsuite())
    suite.addTest(pc_perf.PCForest10csvsuite())
    suite.addTest(pc_perf.PCForestcsvsuite())

    # lp
    suite.addTest(lp_perf.LPElNinocsvsuite())
    suite.addTest(lp_perf.LPForest10csvsuite())
    suite.addTest(lp_perf.LPForestcsvsuite())

    # pp
    suite.addTest(pp_perf.PPElNinocsv_suite())
    suite.addTest(pp_perf.PPForest10csv_suite())
    suite.addTest(pp_perf.PPForestcsv_suite())

    # hist
    suite.addTest(hist_perf.HElNinocsv_suite())
    suite.addTest(hist_perf.HForest10csv_suite())
    suite.addTest(hist_perf.HForestcsv_suite())

    # scp
    suite.addTest(scp_perf.SCPElNinocsv_suite())
    suite.addTest(scp_perf.SCPForest10csv_suite())
    suite.addTest(scp_perf.SCPForestcsv_suite())

    # splom
    suite.addTest(splom_perf.SPLOMElNinocsv_suite())
    suite.addTest(splom_perf.SPLOMForest10csv_suite())
    suite.addTest(splom_perf.SPLOMForestcsv_suite())

    #---------------------------------------------------- db
    # pc db
    suite.addTest(pc_perf.PCElNinodbsuite())
    suite.addTest(pc_perf.PCForest10dbsuite())
    suite.addTest(pc_perf.PCForestdbsuite())

    # lp
    suite.addTest(lp_perf.LPElNinodbsuite())
    suite.addTest(lp_perf.LPForest10dbsuite())
    suite.addTest(lp_perf.LPForestdbsuite())

    # pp
    suite.addTest(pp_perf.PPElNinodb_suite())
    suite.addTest(pp_perf.PPForest10db_suite())
    suite.addTest(pp_perf.PPForestdb_suite())

    # hist
    suite.addTest(hist_perf.HElNinodb_suite())
    suite.addTest(hist_perf.HForest10db_suite())
    suite.addTest(hist_perf.HForestdb_suite())

    # scp
    suite.addTest(scp_perf.SCPElNinodb_suite())
    suite.addTest(scp_perf.SCPForest10db_suite())
    suite.addTest(scp_perf.SCPForestdb_suite())

    # splom
    suite.addTest(splom_perf.SPLOMElNinodb_suite())
    suite.addTest(splom_perf.SPLOMForest10db_suite())
    suite.addTest(splom_perf.SPLOMForestdb_suite())

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(masterSuite())
