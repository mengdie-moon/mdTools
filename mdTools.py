"""
@Author   : 梦蝶
@Contact  : 3257053519@qq.com
@CallMe   : 3257053519
@Copyright: (c) 2025 by 梦蝶, Inc. All Rights Reserved.
"""
from mainTools import mdTools_main
from mouseTools import mdTools_mouse
from popupTools import mdTools_popup
from screenshotTools import mdTools_screenshot
from typing import Optional, Union, Callable

class mdTools:
    def __init__(self):
        self.mainTool = mdTools_main()
        # 鼠标操作
        self.mouse = mdTools_mouse()
        # 弹窗
        self.popup = mdTools_popup()
        # 截屏
        self.screenshot = mdTools_screenshot()

    def randomPassword(self, length: int = 10, isNumber: bool = True, isStr: bool = True, isNotation: bool = False) -> str:
        return self.mainTool.randomPassword(length, isNumber, isStr, isNotation)

    def base64_encode(self, data: str | bytes, url_safe: bool = False, encoding: str = 'utf-8') -> str:
        return self.mainTool.base64_encode(data, url_safe, encoding)

    def base64_decode(self, encoded_data: str | bytes, url_safe: bool = False, encoding: str = 'utf-8') -> str | bytes:
        return self.mainTool.base64_decode(encoded_data, url_safe, encoding)

    def base64_encode_file(self, file_path: str, url_safe: bool = False, encoding: str = 'utf-8', output_file: str = None) -> str | None:
        return self.mainTool.base64_encode_file(file_path, url_safe, encoding, output_file)

    def base64_decode_file(self, file_path: str, url_safe: bool = False, encoding: str = 'utf-8', output_file: str = None) -> str | bytes | None:
        return self.mainTool.base64_decode_file(file_path, url_safe, encoding, output_file)

    def md5_hash(self, data: str | bytes, encoding: str = 'utf-8') -> str:
        return self.mainTool.md5_hash(data, encoding)

    def md5_hash_file(self, input_file: str,  output_file: str = None, chunk_size: int = 8192) -> str | None:
        return self.mainTool.md5_hash_file(input_file, output_file, chunk_size)
            
    def random_user_agent(self, num: int = 1, devices: list = ["pc", "mobile", "tablet"], browsers: list = ["chrome", "firefox", "safari", "edge"], device_weights: list = None) -> str | list:
       return self.mainTool.random_user_agent(num, devices, browsers, device_weights)
    
    def random_ip(self, num: int = 1) -> str | list:
        return self.mainTool.random_ip(num)
    
    def mouse_move(self, x: int = 0, y: int = 0 ) -> True:
       return self.mouse.mouse_move(x, y)
    
    def mouse_click(self, button: str = 'left', x: Optional[int] = None, y: Optional[int] = None) -> bool:
       return self.mouse.mouse_click(button, x, y)
    
    def mouse_double_click(self, button: str = 'left', x: Optional[int] = None, y: Optional[int] = None) -> bool:
       return self.mouse.mouse_click(button, x, y)

    def mouse_scroll(self, pixels: int, direction: str = 'down') -> bool:
        return self.mouse.mouse_scroll(pixels, direction)
    
    def mouse_get_CurrentLocation(self, wait_time: float = 0) -> tuple[int, int]:
        return self.mouse.mouse_get_CurrentLocation(wait_time)
    
    def mouse_down(self, button: str = 'left') -> bool:
        return self.mouse.mouse_down(button)
    
    def mouse_up(self, button: str = 'left') -> bool:
        return self.mouse.mouse_up(button)

    def mouse_drag(self, dx: int, dy: int, button: str = 'left', x: Optional[int] = None, y: Optional[int] = None) -> bool:
        return self.mouse.mouse_drag(dx, dy, button, x, y)

    def mouse_write(self, message: str, interval: float = 0.0) -> bool:
        return self.mouse.mouse_write(message, interval)
    
    def MPopup_messagebox(self, content: str, title: Optional[str] = "提示", type: str = "info") -> Union[bool, None]:
        return self.popup.MPopup_messagebox(content, title, type)
    
    def MPopup_prompt(self, content: str, title: str = "Prompt Popup", isPassword: bool = False, validate: Optional[Callable[[str], bool]] = None) -> Optional[str]:
        return self.popup.MPopup_prompt(content, title, isPassword, validate)
    
    def cleanup(self):
        self.popup.cleanup()

    def md_screenshot(self, x: int, y: int, e_x: int, e_y: int, filename: str, path: Optional[str] = None) -> str:
        return self.screenshot.md_screenshot(x, y, e_x, e_y, filename, path)

    def md_full_screenshot(self, filename: str, path: Optional[str] = None, wait_time: float = 0) -> str:
        return self.screenshot.md_full_screenshot(filename, path, wait_time)
