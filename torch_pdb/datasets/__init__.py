from .dataset import TorchPDBDataset
from .rcsb import RCSBDataset
from .ec import ECDataset
from .go import GODataset
from .pdbbind_refined import PDBBindRefined
from .pfam import PfamDataset
from .tmscore_benchmark import TMScoreBenchmark
from .alphafold import AlphaFoldDataset

__all__ = [
    'TorchPDBDataset',
    'RCSBDataset',
    'ECDataset',
    'GODataset',
    'PDBBindRefined',
    'PramDataset',
    'TMScoreBenchmark',
    'AlphaFoldDataset'
    ]

classes = __all__
