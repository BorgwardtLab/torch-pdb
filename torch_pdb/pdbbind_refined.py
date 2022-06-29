# -*- coding: utf-8 -*-
import glob, torch
from torch_geometric.data import extract_tar, download_url
from torch_pdb import TorchPDBDataset

class PDBBindRefined(TorchPDBDataset):

    def __init__(self, version='2020', **kwargs):
        self.version = version
        super().__init__(**kwargs)

    def get_raw_files(self):
        return glob.glob(f'{self.root}/raw/files/*/*_protein.pdb')

    def get_id_from_filename(self, filename):
        return filename[:4]

    def download(self):
        download_url(f'https://pdbbind.oss-cn-hangzhou.aliyuncs.com/download/PDBbind_v{self.version}_refined.tar.gz', f'{self.root}/raw')
        extract_tar(f'{self.root}/raw/PDBbind_v{self.version}_refined.tar.gz', f'{self.root}/raw')
        os.rename(f'{self.root}/raw/refined-set', f'{self.root}/raw/files')
        self.download_complete()

    def add_protein_attributes(self, protein):
        pocket = self.pdb2df(f'{self.root}/raw/files/{protein["ID"]}/{protein["ID"]}_pocket.pdb')
        is_site = torch.zeros((len(pocket),))
        is_site[(
            torch.tensor(pocket['residue_number'].tolist()).unsqueeze(1) == protein['residue_index']
        ).sum(dim=1).nonzero()] = 1.
        protein['binding_site'] = is_site
        return protein
