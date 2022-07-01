# -*- coding: utf-8 -*-
import torch, os
from torch_geometric.data import InMemoryDataset, Data
from torch_geometric.utils import from_scipy_sparse_matrix
from biopandas.pdb import PandasPdb
from tqdm import tqdm
import numpy as np
from sklearn.neighbors import kneighbors_graph, radius_neighbors_graph
from torch_pdb.embeddings import one_hot

three2one = {'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L', 'MET': 'M', 'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R', 'SER': 'S', 'THR': 'T', 'VAL': 'V', 'TRP': 'W', 'TYR': 'Y'}

class TorchPDBDataset(InMemoryDataset):
    def __init__(self,
            root,
            name,
            node_embedding      = one_hot,
            graph_construction  = 'eps',
            eps                 = 8,
            k                   = 5,
            weighted_edges      = False,
            only_single_chain   = False,
            check_sequence      = False,
            ):
        self.root = root
        self.name = name
        self.node_embedding = node_embedding
        self.graph_construction = graph_construction
        self.eps = eps
        self.k = k
        self.weighted_edges = weighted_edges
        self.only_single_chain = only_single_chain
        self.check_sequence = check_sequence
        super().__init__(root)
        self._download() # some weird quirk requires this if .process() is not defined on the lowest inheritance level, might want to look into this at some point
        self._process()
        self.data, self.slices = torch.load(self.processed_paths[0])

    def get_raw_files(self):
        ''' Returns a list of all valid PDB files.
        Implement me! '''
        raise NotImplementedError

    def get_id_from_filename(self, filename):
        ''' Takes in raw filename `xyz_abc.pdb` and returns a PDBID.
        Implement me! '''
        raise NotImplementedError

    def download(self):
        ''' Dumps data to /raw and /raw/files/*.pdb.
        Implement me! '''
        raise NotImplementedError

    def add_protein_attributes(self, protein):
        ''' Implement me! '''
        return protein

    @property
    def raw_file_names(self):
        return ['done.txt']

    @property
    def processed_file_names(self):
        return [f'{self.name}.pt']

    def download_complete(self):
        print('Download complete.')
        with open(f'{self.root}/raw/{self.raw_file_names[0]}','w') as file:
            file.write('done.')

    def process(self):
        proteins = self.parse_pdbs()
        data_list = [self.graph2pyg(self.protein2graph(p), info=p) for p in tqdm(proteins, desc='Converting proteins to graphs')]
        print('Saving...')
        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])
        print('Dataset ready.')

    def parse_pdbs(self):
        structs = []
        for path in tqdm(self.get_raw_files(), desc='Parsing PDB files'):
            df = self.pdb2df(path)
            if not self.validate(df):
                continue
            protein = {
                'ID': self.get_id_from_filename(os.path.basename(path)),
                'sequence': ''.join(df['residue_name']),
                'residue_index': torch.tensor(df['residue_number'].tolist()).int(),
                'chain_id': df['chain_id'].tolist(),
                'coords': torch.tensor(df.apply(lambda row: (row['x_coord'], row['y_coord'], row['z_coord']), axis=1).to_list()).long(),
            }
            protein = self.add_protein_attributes(protein)
            structs.append(protein)
        return structs

    def pdb2df(self, path):
        df = PandasPdb().read_pdb(path).df['ATOM']
        df = df[df['atom_name'] == 'CA']
        df['residue_name'] = df['residue_name'].map(lambda x: three2one[x])
        df = df.sort_values('residue_number')
        return df

    def validate(self, df):
        # check if single chain protein
        if self.only_single_chain and len(df['chain_id'].unique()) > 1:
            return False
        # check if sequence and structure are consistent
        if self.check_sequence and not np.array_equal(df.index, np.arange(1,len(df)+1)):
            return False
        return True

    def protein2graph(self, protein):
        nodes = self.node_embedding(protein['sequence'])
        if self.graph_construction == 'eps':
            mode = 'distance' if self.weighted_edges else 'connectivity'
            adj = radius_neighbors_graph(protein['coords'], radius=self.eps, mode=mode)
        elif self.graph_construction == 'knn':
            adj = kneighbors_graph(protein['coords'], k=self.k)
        return (nodes, adj)

    def graph2pyg(self, graph, info={}):
        nodes = torch.Tensor(graph[0]).float()
        edges = from_scipy_sparse_matrix(graph[1])
        return Data(x=nodes, edge_index=edges[0].long(), edge_attr=edges[1].unsqueeze(1).float(), **info)
