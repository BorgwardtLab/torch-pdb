import unittest, tempfile
from torch_pdb import PDBBindRefined, TMScoreBenchmark, GODataset, ECDataset, PfamDataset, RCSBDataset

class Dummy(unittest.TestCase):

    def test_pdbbind(self):
        with tempfile.TemporaryDirectory() as tmp:
            ds = PDBBindRefined(root=tmp, name='test')

    def test_tm(self):
        with tempfile.TemporaryDirectory() as tmp:
            ds = TMScoreBenchmark(root=tmp, name='test')

    def test_go(self):
        with tempfile.TemporaryDirectory() as tmp:
            ds = GODataset(root=tmp, name='test')

    def test_ec(self):
        with tempfile.TemporaryDirectory() as tmp:
            ds = ECDataset(root=tmp, name='test')

    def test_pfam(self):
        with tempfile.TemporaryDirectory() as tmp:
            ds = PfamDataset(root=tmp, name='test')

    def test_rcsb(self):
        with tempfile.TemporaryDirectory() as tmp:
            ds = RCSBDataset(root=tmp, name='test')

if __name__ == '__main__':
    unittest.main()