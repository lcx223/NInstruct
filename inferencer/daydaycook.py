from typing import Dict, Any, List

from utils import load_pickle, preprocess_text
from inferencer import BaseInferencer
import re

class DaydaycookInferencer(BaseInferencer):
    def __init__(self,
                 types: List[str],
                 **kwargs) -> None:
        super().__init__(types=types)
        ...

    def decomp_components(self, components) -> Dict[str, Any]:
        components_nested = {}
        components_flat = {}
        for i in components:
            if type(i) == dict:
                for k, v in i.items():
                    d = {}
                    for j in v:
                        assert isinstance(j, dict)
                        d.update(j)
                    components_nested[k] = d
            elif type(i) == str:
                pos = i.find(':') 
                if pos != -1:
                    components_flat[i[:pos].strip()] = i[pos+1:].strip()
            else:
                raise ValueError(f"Unknown type of component: {type(i)}")             
        return components_nested, components_flat
    
    def merge_img_preview(self, title_img, preview, title_img_type):
        if isinstance(title_img, list):
            if isinstance(preview, list):
                img =  title_img + preview
            else:
                img =  title_img + [preview]
        else:
            if isinstance(preview, list):
                img =  [title_img] + preview
            else:
                img =  [title_img, preview]
        if isinstance(title_img_type, list):
            img_type = title_img_type + ['normal']
        else:
            img_type = [title_img_type, 'normal']
        return img, img_type
    

    def load(self,
             file_name: str,
             **kwargs) -> Dict[str, Any]:
        cur_data = load_pickle(file_name)
        components_nested, components_flat = self.decomp_components(cur_data['components'])
        img, img_type = self.merge_img_preview(cur_data['title_img'], cur_data['preview'], cur_data['title_img_type'])
        cur_data = {
            'id': cur_data['id'],
            'title': cur_data['title'],
            'img': img,
            'type':img_type,
            'description': cur_data['description'],
            'components_nested': components_nested, # will contain ''一般食材', '醬汁材料'...(食材类的)
            'components_flat': components_flat, # will contain '烹饪时间'，'份量'等
            'steps': cur_data['steps'],
            'comments': cur_data['comments'],
        }

        # NOTE: 完善类型检查
        assert isinstance(cur_data['title'], str)
        def assert_str_or_list_of_str(text):
            assert isinstance(text, str) \
                or isinstance(text, list) and all(isinstance(i, str) for i in text)
        assert_str_or_list_of_str(cur_data['img'])
        assert_str_or_list_of_str(cur_data['type'])
        assert isinstance(cur_data['description'], str)
        assert isinstance(cur_data['components_nested'], dict) \
            and all(isinstance(value, dict) for value in cur_data['components_nested'].values())
        assert all(isinstance(i, dict) and 'description' in i and 'img' in i for i in cur_data['steps'])

        # 文本预处理
        cur_data['title'] = preprocess_text(cur_data['title'])
        cur_data['description'] = preprocess_text(cur_data['description'])
        for key1, inner_dict in cur_data['components_nested'].items():
            for key2, value in inner_dict.items():
                cur_data['components_nested'][key1][key2] = preprocess_text(value)
        for key in cur_data['components_flat'].keys():
            cur_data['components_flat'][key] = preprocess_text(cur_data['components_flat'][key])
        for i in range(len(cur_data['steps'])):
            cur_data['steps'][i]['description'] = preprocess_text(cur_data['steps'][i]['description'])
        # print(cur_data)
        return cur_data

