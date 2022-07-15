""" Print data statistics to stdout as markdown and latex tables
"""
import tempfile

import pandas as pd

from torch_pdb.datasets import PDBBindRefined, TMScoreBenchmark, GODataset, ECDataset, PfamDataset, RCSBDataset, AlphaFoldDataset
from torch_pdb.datasets.alphafold import AF_DATASET_NAMES

datasets = [
            RCSBDataset,
            PfamDataset,
            GODataset,
            ECDataset,
            PDBBindRefined,
            TMScoreBenchmark,
            ]

rows = []

unique_pdbs = set()
for i, dataset in enumerate(datasets):
    with tempfile.TemporaryDirectory() as tmp:
        ds = dataset(root=tmp)
        unique_pdbs |= {p['ID'] for p in ds.proteins}
        desc = ds.describe()
        rows.append(desc)

unique_af = set()
# do alphafold seaprately
for org in AF_DATASET_NAMES.keys():
    with tempfile.TemporaryDirectory() as tmp:
        ds = AlphaFoldDataset(root=tmp, organism=org)
        unique_af |= {p['ID'] for p in ds.proteins}
        desc = ds.describe()
        desc['name'] += f'_{org}'
        rows.append(desc)
    df = pd.DataFrame(rows)
    md = df.to_markdown(index=False)
    tx = df.to_latex(index=False, na_rep='-')

print(f"TOTAL RCSB: {len(unique_pdbs)}")
print(f"TOTAL AF: {len(unique_af)}")

df = pd.DataFrame(rows)
md = df.to_markdown(index=False)
tx = df.to_latex(index=False)

print(md)
print()
print(tx)
