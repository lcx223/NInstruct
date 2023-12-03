from inferencer.base import BaseInferencer
from inferencer.meichichina import MeishiChinaInferencer
from inferencer.daydaycook import DaydaycookInferencer
from inferencer.douguo import DouGuoInferencer
from inferencer.xiachufang import XiachufangInferencer
from inferencer.xinshipu import XinshipuInferencer

__all__ = [
    'BaseInferencer',
    'MeishiChinaInferencer',
    'DaydaycookInferencer',
    'DouGuoInferencer',
    'XiachufangInferencer',
    'XinshipuInferencer'
    ]

EXP_STR2CLASS_NAME = {
    'meishichina': 'MeishiChinaInferencer',
    'daydaycook': 'DaydaycookInferencer',
    'douguo':'DouGuoInferencer',
    'xiachufang': 'XiachufangInferencer',
    'xinshipu': 'XinshipuInferencer'
}
