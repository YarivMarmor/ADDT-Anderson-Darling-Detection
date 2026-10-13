import unittest
from pathlib import Path
import sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from add_core import analyze
from add_io import load_values,default_parameters,transform
EXAMPLES=Path(__file__).resolve().parents[1]/'examples'
class TestADD(unittest.TestCase):
    def test_normal(self):
        raw=load_values(next(EXAMPLES.glob('data_mu=5*')))
        self.assertEqual(len(raw),1000)
        a,b=default_parameters(raw,0)
        vals=transform(raw,0,a,b)
        results=analyze(vals,0)
        self.assertEqual(len(results),1000)
        self.assertEqual(results[-1].ad_right,0)
        self.assertTrue(all(np.isfinite([r.ad_left,r.ad_right,r.ad_difference]).all() for r in results))
    def test_uniform(self):
        raw=load_values(next(EXAMPLES.glob('data_mu=100*')))
        self.assertEqual(len(raw),1000)
        a,b=default_parameters(raw,1)
        vals=transform(raw,1,a,b)
        self.assertGreaterEqual(vals.min(),0)
        self.assertLessEqual(vals.max(),1)
        self.assertEqual(len(analyze(vals,1)),1000)
    def test_exponential(self):
        raw=np.array([1.,2.,4.,8.])
        a,_=default_parameters(raw,2)
        vals=transform(raw,2,a)
        self.assertEqual(len(analyze(vals,2)),4)
    def test_invalid(self):
        with self.assertRaises(ValueError):transform([1.,2.],1,5.,4.)
        with self.assertRaises(ValueError):transform([1.,2.],0,0.,0.)
if __name__=='__main__':unittest.main()
