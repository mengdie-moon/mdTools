"""mdTools - 一个多功能的Python工具包

@Author   : 梦蝶
@Contact  : 3257053519@qq.com
@CallMe   : 3257053519
@Copyright: (c) 2025 by 梦蝶, Inc. All Rights Reserved.
"""

__version__ = '1.0.0'
__author__ = '梦蝶'

from .mainTools import mdTools_main
from .mouseTools import mdTools_mouse
from .popupTools import mdTools_popup
from .screenshotTools import mdTools_screenshot
from .mdToolsError import mdToolsErros, ToolsEorror

__all__ = [
    'mdTools_main',
    'mdTools_mouse',
    'mdTools_popup',
    'mdTools_screenshot',
    'mdToolsErros',
    'ToolsEorror'
]