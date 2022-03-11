from test_algo.datafly_v1 import run

# testing dafly algo
def testfly():
    k = 4
    assert(run(k) >= k)