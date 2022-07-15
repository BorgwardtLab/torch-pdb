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
        # unique_pdbs |= {p.name for p in ds}
        desc = ds.describe()
        rows.append(desc)

print(f"TOTAL PDB : {len(unique_pdbs)}")
unique_af = set()
# do alphafold seaprately
for org in AF_DATASET_NAMES.keys():
    print(org)
    with tempfile.TemporaryDirectory() as tmp:
        ds = AlphaFoldDataset(root=tmp, organism=org)
        unique_pdbs |= {p.name for p in ds}
        desc = ds.describe()
        desc['name'] += f'_{org}'
        print(desc)
        rows.append(desc)
    df = pd.DataFrame(rows)
    md = df.to_markdown(index=False)
    tx = df.to_latex(index=False, na_rep='-')
    print(md)
    print()
    print(tx)

print(f"TOTAL AF: {len(unique_af)}")

df = pd.DataFrame(rows)
md = df.to_markdown(index=False)
tx = df.to_latex(index=False)

print(md)
print()
print(tx)
