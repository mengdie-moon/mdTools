"""
@Author   : 梦蝶
@Contact  : 3257053519@qq.com
@CallMe   : 3257053519
@Copyright: (c) 2025 by 梦蝶, Inc. All Rights Reserved.
"""

# 注意Mac, Linux系统部分适配,有些操作需要自信额外安装依赖
# Attention Mac, Partial adaptation to Linux system, some operations require confidence and additional installation of dependencies

import platform
import os
import time
import ctypes
from typing import Optional
from mdToolsError import ToolsEorror

class mdTools_mouse:
    def __init__(self):
        pass
    def mouse_move(self, x: int = 0, y: int = 0 ) -> bool:
        """
        移动鼠标到指定坐标
        :param x: 目标X坐标（默认0）
        :param y: 目标Y坐标（默认0）
        :return: 操作成功返回True
        """
        if not isinstance(x, int):
            raise ToolsEorror(f"ToolsError: The x-coordinate must be a floating-point number, which is actually passed in {type(x)}")
        if not isinstance(y, int):
            raise ToolsEorror(f"ToolsError: The y-coordinate must be a floating-point number, which is actually passed in {type(y)}")
        system = platform.system()
        
        if system == 'Windows':
            ctypes.windll.user32.SetCursorPos(x, y)
            return True
        elif system == 'Darwin':
            script = f'''
            tell application "System Events"
                set position of first item of processes whose frontmost is true to {{{x}, {y}}}
                delay 0.1
            end tell
            '''
            os.system(f"osascript -e '{script}'")
            return True

        elif system == 'Linux':
            os.system(f"xdotool mousemove {x} {y}")
            return True
        else:
            raise ToolsEorror("ToolsError: Unsupported operating system")
        
    def _validate_coordinates(self, x: Optional[int], y: Optional[int]) -> None:
        """验证坐标有效性"""
        if (x is not None and y is None) or (y is not None and x is None):
            raise ToolsEorror("ToolsError: Coordinates require both x and y values")
        if x is not None and not isinstance(x, int):
            raise ToolsEorror(f"ToolsError: X coordinate must be integer, got {type(x)}")
        if y is not None and not isinstance(y, int):
            raise ToolsEorror(f"ToolsError: Y coordinate must be integer, got {type(y)}")

    def mouse_click(self, button: str = 'left', x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """
        执行鼠标单击操作
        :param button: 鼠标按键（left/right/middle，默认left）
        :param x: 点击位置X坐标（可选）
        :param y: 点击位置Y坐标（可选）
        :return: 操作成功返回True
        """
        """执行鼠标单击操作"""
        self._validate_coordinates(x, y)
        if button.lower() not in ['left', 'right', 'middle']:
            raise ToolsEorror(f"ToolsError: Invalid button type: {button}")

        # 处理坐标移动
        if x is not None and y is not None:
            self.mouse_move(x, y)
            time.sleep(0.03)

        system = platform.system()
        try:
            if system == 'Windows':
                btn_map = {
                    'left': (0x0002, 0x0004),
                    'right': (0x0008, 0x0010),
                    'middle': (0x0020, 0x0040)
                }
                down, up = btn_map[button.lower()]
                ctypes.windll.user32.mouse_event(down, 0, 0, 0, 0)
                ctypes.windll.user32.mouse_event(up, 0, 0, 0, 0)

            elif system == 'Darwin':
                btn_map = {
                    'left': 'left',
                    'right': 'right',
                    'middle': 'middle'
                }
                script = f'''
                tell application "System Events"
                    mouse down the {btn_map[button]} button
                    mouse up the {btn_map[button]} button
                end tell
                '''
                os.system(f"osascript -e '{script}'")

            elif system == 'Linux':
                btn_map = {
                    'left': 1,
                    'middle': 2,
                    'right': 3
                }
                os.system(f"xdotool click {btn_map[button.lower()]}")
            
            return True
        except KeyError:
            raise ToolsEorror(f"ToolsError: Unsupported button for {system} system")
        except Exception as e:
            raise ToolsEorror(f"ToolsError: Operation failed: {str(e)}")

    def mouse_double_click(self, button: str = 'left', x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """
        执行鼠标双击操作
        :param button: 鼠标按键（left/right/middle，默认left）
        :param x: 双击位置X坐标（可选）
        :param y: 双击位置Y坐标（可选）
        :return: 操作成功返回True
        """
        """执行鼠标双击操作"""
        self._validate_coordinates(x, y)
        if button.lower() not in ['left', 'right', 'middle']:
            raise ToolsEorror(f"ToolsError: Invalid button type: {button}")

        # 处理坐标移动
        if x is not None and y is not None:
            self.mouse_move(x, y)
            time.sleep(0.03)

        system = platform.system()
        try:
            if system == 'Windows':
                btn_map = {
                    'left': (0x0002, 0x0004),
                    'right': (0x0008, 0x0010),
                    'middle': (0x0020, 0x0040)
                }
                down, up = btn_map[button.lower()]
                for _ in range(2):
                    ctypes.windll.user32.mouse_event(down, 0, 0, 0, 0)
                    ctypes.windll.user32.mouse_event(up, 0, 0, 0, 0)
                    time.sleep(0.05)

            elif system == 'Darwin':
                btn_map = {
                    'left': 'left',
                    'right': 'right',
                    'middle': 'middle'
                }
                script = f'''
                tell application "System Events"
                    mouse down the {btn_map[button]} button
                    mouse up the {btn_map[button]} button
                    delay 0.1
                    mouse down the {btn_map[button]} button
                    mouse up the {btn_map[button]} button
                end tell
                '''
                os.system(f"osascript -e '{script}'")

            elif system == 'Linux':
                btn_map = {
                    'left': 1,
                    'middle': 2,
                    'right': 3
                }
                os.system(f"xdotool click --repeat 2 {btn_map[button.lower()]}")

            return True
        except KeyError:
            raise ToolsEorror(f"ToolsError: Unsupported button for {system} system")
        except Exception as e:
            raise ToolsEorror(f"ToolsError: Operation failed: {str(e)}")    
        
    def mouse_scroll(self, pixels: int, direction: str = 'down') -> bool:
        """
        模拟鼠标滚轮滚动
        :param pixels: 滚动像素值（正整数）
        :param direction: 滚动方向（up/down，默认down）
        :return: 操作成功返回True
        """
        """模拟鼠标滚轮滚动
        :param pixels: 滚动像素值（正整数）
        :param direction: 滚动方向 up/down，默认向下
        """
        # 参数验证
        if not isinstance(pixels, int) or pixels <= 0:
            raise ToolsEorror(f"ToolsError: Pixels must be positive integer, got {pixels}")
        direction = direction.lower()
        if direction not in ['up', 'down']:
            raise ToolsEorror(f"ToolsError: Invalid direction: {direction}")

        system = platform.system()
        try:
            if system == 'Windows':
                WHEEL_DELTA = 120
                num_events = (pixels + WHEEL_DELTA - 1) // WHEEL_DELTA
                delta = 120 if direction == 'up' else -120
                for _ in range(num_events):
                    ctypes.windll.user32.mouse_event(0x0800, 0, 0, delta, 0)
                    time.sleep(0.01)

            elif system == 'Darwin':
                LINE_STEP = 40
                repeats = (pixels + LINE_STEP - 1) // LINE_STEP
                script = f'''
                tell application "System Events"
                    repeat {repeats} times
                        scroll wheel "{direction}" by 1
                    end repeat
                end tell'''
                os.system(f"osascript -e '{script}'")

            elif system == 'Linux':
                CLICK_STEP = 120
                clicks = (pixels + CLICK_STEP - 1) // CLICK_STEP
                btn = 4 if direction == 'up' else 5
                os.system(f"xdotool click --repeat {clicks} {btn}")
            else:
                raise ToolsEorror("ToolsError: Unsupported operating system")
            return True
        except Exception as e:
            raise ToolsEorror(f"ToolsError: Scroll failed: {str(e)}")
        
    def mouse_get_CurrentLocation(self, wait_time: float = 0) -> tuple[int, int]:
        """
        获取当前鼠标位置
        :param wait_time: 获取位置前等待时间（秒，默认0）
        :return: 返回当前鼠标坐标元组(x, y)
        """
        """获取当前鼠标坐标"""
        time.sleep(wait_time)
        system = platform.system()
        try:
            if system == 'Windows':
                class POINT(ctypes.Structure):
                    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
                point = POINT()
                ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
                return (point.x, point.y)
            
            elif system == 'Darwin':
                script = '''
                tell application "System Events"
                    set mousePos to get the position of the mouse
                end tell
                return mousePos
                '''
                output = os.popen(f"osascript -e '{script}'").read().strip()
                x, y = output.split(', ')
                return (int(x), int(y))
            
            elif system == 'Linux':
                output = os.popen('xdotool getmouselocation').read().strip()
                x = output.split('x:')[1].split()[0]
                y = output.split('y:')[1].split()[0]
                return (int(x), int(y))
            
            else:
                raise ToolsEorror("ToolsError: Unsupported operating system")
        except Exception as e:
            raise ToolsEorror(f"ToolsError: Get position failed: {str(e)}")

    def mouse_down(self, button: str = 'left') -> bool:
        """
        按下鼠标按键
        :param button: 鼠标按键（left/right/middle，默认left）
        :return: 操作成功返回True
        """
        """按下鼠标按钮"""
        if button.lower() not in ['left', 'right', 'middle']:
            raise ToolsEorror(f"ToolsError: Invalid button type: {button}")
        
        system = platform.system()
        try:
            if system == 'Windows':
                btn_map = {
                    'left': 0x0002,
                    'right': 0x0008,
                    'middle': 0x0020
                }
                ctypes.windll.user32.mouse_event(btn_map[button.lower()], 0, 0, 0, 0)
            
            elif system == 'Darwin':
                btn_map = {
                    'left': 'left',
                    'right': 'right',
                    'middle': 'middle'
                }
                script = f'''
                tell application "System Events"
                    mouse down the {btn_map[button]} button
                end tell
                '''
                os.system(f"osascript -e '{script}'")
            
            elif system == 'Linux':
                btn_map = {
                    'left': 1,
                    'middle': 2,
                    'right': 3
                }
                os.system(f"xdotool mousedown {btn_map[button.lower()]}")
            
            else:
                raise ToolsEorror("ToolsError: Unsupported operating system")
            return True
        except Exception as e:
            raise ToolsEorror(f"ToolsError: Mouse down failed: {str(e)}")

    def mouse_up(self, button: str = 'left') -> bool:
        """
        释放鼠标按键
        :param button: 鼠标按键（left/right/middle，默认left）
        :return: 操作成功返回True
        """
        """释放鼠标按钮"""
        if button.lower() not in ['left', 'right', 'middle']:
            raise ToolsEorror(f"ToolsError: Invalid button type: {button}")
        
        system = platform.system()
        try:
            if system == 'Windows':
                btn_map = {
                    'left': 0x0004,
                    'right': 0x0010,
                    'middle': 0x0040
                }
                ctypes.windll.user32.mouse_event(btn_map[button.lower()], 0, 0, 0, 0)
            
            elif system == 'Darwin':
                btn_map = {
                    'left': 'left',
                    'right': 'right',
                    'middle': 'middle'
                }
                script = f'''
                tell application "System Events"
                    mouse up the {btn_map[button]} button
                end tell
                '''
                os.system(f"osascript -e '{script}'")
            
            elif system == 'Linux':
                btn_map = {
                    'left': 1,
                    'middle': 2,
                    'right': 3
                }
                os.system(f"xdotool mouseup {btn_map[button.lower()]}")
            
            else:
                raise ToolsEorror("ToolsError: Unsupported operating system")
            return True
        except Exception as e:
            raise ToolsEorror(f"ToolsError: Mouse up failed: {str(e)}")

    def mouse_drag(self, dx: int, dy: int, button: str = 'left', x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """
        执行鼠标拖拽操作
        :param dx: X方向拖拽距离
        :param dy: Y方向拖拽距离
        :param button: 鼠标按键（left/right/middle，默认left）
        :param x: 起始位置X坐标（可选）
        :param y: 起始位置Y坐标（可选）
        :return: 操作成功返回True
        """
        """模拟鼠标拖动操作
        :param dx: 水平移动像素（正数向右，负数向左）
        :param dy: 垂直移动像素（正数向下，负数向上）
        :param button: 使用的鼠标按钮（默认左键）
        :param x: 起始坐标X（可选）
        :param y: 起始坐标Y（可选）
        """
        if not isinstance(dx, int) or not isinstance(dy, int):
            raise ToolsEorror("ToolsError: dx/dy must be integers")
        if dx == 0 and dy == 0:
            raise ToolsEorror("ToolsError: At least one of dx/dy must be non-zero")
        
        if x is not None and y is not None:
            self.mouse_move(x, y)
        
        system = platform.system()
        try:
            self.mouse_down(button)
            time.sleep(0.05)
            
            if system == 'Windows':
                steps = max(abs(dx), abs(dy))
                step_x = dx / steps
                step_y = dy / steps
                for _ in range(steps):
                    ctypes.windll.user32.mouse_event(0x0001, int(step_x), int(step_y), 0, 0)
                    time.sleep(0.01)
            
            elif system == 'Darwin':
                current_x, current_y = self.mouse_get_CurrentLocation()
                self.mouse_move(current_x + dx, current_y + dy)
            
            elif system == 'Linux':
                os.system(f"xdotool mousemove_relative -- {dx} {dy}")
            
            else:
                raise ToolsEorror("ToolsError: Unsupported operating system")
            
            time.sleep(0.1)
            self.mouse_up(button)
            return True
        
        except Exception as e:
            self.mouse_up(button)
            raise ToolsEorror(f"ToolsError: Drag failed: {str(e)}")
        
    def mouse_write(self, message: str, interval: float = 0.0) -> bool:
        """
        模拟键盘输入文本
        :param message: 要输入的文本内容
        :param interval: 字符间输入间隔（秒，默认0.0）
        :return: 操作成功返回True
        """
        """模拟键盘输入文本
        :param message: 要输入的字符串
        :param interval: 字符输入间隔时间（秒）
        """
        if not isinstance(message, str):
            raise ToolsEorror(f"ToolsError: The message must be of string type, current type:{type(message)}")
        if not isinstance(interval, (int, float)) or interval < 0:
            raise ToolsEorror(f"ToolsError: The interval time must be non negative, current value:{interval}")

        system = platform.system()
        try:
            if system == 'Windows':
                return self._windows_write(message, interval)
            elif system == 'Darwin':
                return self._macos_write(message, interval)
            elif system == 'Linux':
                return self._linux_write(message, interval)
            else:
                raise ToolsEorror("ToolsError: Unsupported operating system")
        except Exception as e:
            raise ToolsEorror(f"ToolsError: Input failed: {str(e)}")

    def _windows_write(self, message: str, interval: float) -> bool:
        """Windows实现"""
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        if hwnd == 0:
            raise ToolsEorror("ToolsError: Unable to obtain activity window")
        thread_id = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, None)
        current_thread_id = ctypes.windll.kernel32.GetCurrentThreadId()
        ctypes.windll.user32.AttachThreadInput(current_thread_id, thread_id, True)

        try:
            for char in message:
                ctypes.windll.user32.PostMessageW(hwnd, 0x102, ord(char), 0)
                time.sleep(interval)
        finally:
            ctypes.windll.user32.AttachThreadInput(current_thread_id, thread_id, False)
        return True

    def _macos_write(self, message: str, interval: float) -> bool:
        """macOS实现"""
        escape_map = {'"': r'\"', '\\': r'\\', '$': r'\$', '`': r'\`'}
        escaped = message.translate(str.maketrans(escape_map))
        script = f'''
        tell application "System Events"
            keystroke "{escaped}"
        end tell
        '''
        os.system(f"osascript -e '{script}'")
        time.sleep(max(0.1, len(message) * interval))
        return True

    def _linux_write(self, message: str, interval: float) -> bool:
        """Linux实现"""
        safe_msg = message.replace("'", r"'\''")
        delay = int(interval * 1000)
        os.system(f"xdotool type --delay {delay} '{safe_msg}'")
        return True

