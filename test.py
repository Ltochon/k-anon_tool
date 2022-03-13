from test_algo.datafly_v1 import read_file, run
import pandas as pd
# testing dafly algo
def testfly():
    df = read_file('test_algo/data/adult.csv', ';')
    k = 4
    qid = ["3"]
    assert(run(df,k,qid) >= k)