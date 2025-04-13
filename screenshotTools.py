"""
@Author   : 梦蝶
@Contact  : 3257053519@qq.com
@CallMe   : 3257053519
@Copyright: (c) 2025 by 梦蝶, Inc. All Rights Reserved.
"""
from mdToolsError import ToolsEorror
from ctypes import wintypes
import struct
import ctypes
import os
import time
from typing import Optional
import zlib
import platform
import tkinter as tk
from tkinter import Tk

# 弥补缺失的部分
class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ('biSize', wintypes.DWORD),
        ('biWidth', wintypes.LONG),
        ('biHeight', wintypes.LONG),
        ('biPlanes', wintypes.WORD),
        ('biBitCount', wintypes.WORD),
        ('biCompression', wintypes.DWORD),
        ('biSizeImage', wintypes.DWORD),
        ('biXPelsPerMeter', wintypes.LONG),
        ('biYPelsPerMeter', wintypes.LONG),
        ('biClrUsed', wintypes.DWORD),
        ('biClrImportant', wintypes.DWORD),
        ('biCompression', wintypes.DWORD), 
    ]

class RGBQUAD(ctypes.Structure):
    _fields_ = [
        ('rgbBlue', wintypes.BYTE),
        ('rgbGreen', wintypes.BYTE),
        ('rgbRed', wintypes.BYTE),
        ('rgbReserved', wintypes.BYTE)
    ]
DIB_RGB_COLORS = 0
BI_RGB = 0
class mdTools_screenshot:
    def __init__(self):
        pass

    def md_screenshot(self, x: int, y: int, e_x: int, e_y: int, filename: str, path: Optional[str] = None) -> str:
        """
        截取指定区域的屏幕截图
        :param x: 起始X坐标（必传）
        :param y: 起始Y坐标（必传）
        :param e_x: 终止X坐标（必传）
        :param e_y: 终止Y坐标（必传）
        :param filename: 保存文件名（必传，支持.bmp或.png格式）
        :param path: 保存路径（默认当前目录）
        :return: 保存的文件完整路径
        """
        system = platform.system()
        try:
            if system == "Windows":
                return self._windows_screenshot(x, y, e_x, e_y, filename, path)
            elif system == "Darwin":
                return self._macos_screenshot(x, y, e_x, e_y, filename, path)
            elif system == "Linux":
                return self._linux_screenshot(x, y, e_x, e_y, filename, path)
            else:
                raise ToolsEorror("ToolsError: Unsupported operating system")
        except Exception as e:
            raise ToolsEorror(f"ToolsError: Screenshot failed: {str(e)}")

    def _windows_screenshot(self, x: int, y: int, e_x: int, e_y: int, filename: str, path: Optional[str] = None) -> str:
        if not all(isinstance(i, int) for i in [x, y, e_x, e_y]):
            raise ToolsEorror("ToolsError: Coordinates must be integers")
        if x >= e_x or y >= e_y:
            raise ToolsEorror("ToolsError: Invalid screenshot area")
        if not filename.lower().endswith(('.bmp', '.png')):
            raise ToolsEorror("ToolsError: Only supports BMP/PNG format")

        save_dir = os.path.abspath(path or os.getcwd())
        if not os.path.exists(save_dir):
            raise ToolsEorror(f"ToolsError: path does not exist: {save_dir}")
        full_path = os.path.join(save_dir, filename)

        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        
        hdc = user32.GetDC(None)
        memdc = gdi32.CreateCompatibleDC(hdc)

        width = e_x - x
        height = e_y - y
        bmp = gdi32.CreateCompatibleBitmap(hdc, width, height)
        gdi32.SelectObject(memdc, bmp)
        
        if not gdi32.BitBlt(memdc, 0, 0, width, height, hdc, x, y, 0x00CC0020):
            raise ToolsEorror("ToolsError: Screen capture failed")
        bmi = self._get_bitmap_info(width, height)
        buffer, buffer_size = self._capture_pixels(gdi32, memdc, bmp, height, bmi)

        if filename.lower().endswith('.png'):
            self._save_as_png(width, height, buffer, full_path)
        else:
            self._save_as_bmp(width, height, buffer, bmi, full_path)

        gdi32.DeleteObject(bmp)
        gdi32.DeleteDC(memdc)
        user32.ReleaseDC(None, hdc)

        return full_path

    def _get_bitmap_info(self, width: int, height: int):
        class BITMAPINFO(ctypes.Structure):
            _fields_ = [
                ("bmiHeader", BITMAPINFOHEADER), 
                ("bmiColors", RGBQUAD * 3)
            ]
        
        bmi = BITMAPINFO()
        header = bmi.bmiHeader
        header.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        header.biWidth = width
        header.biHeight = -height
        header.biPlanes = 1
        header.biBitCount = 24
        header.biCompression = BI_RGB 
        header.biSizeImage = 0
        return bmi
    def _capture_pixels(self, gdi32, memdc, bmp, height, bmi):
        buffer_size = 3 * bmi.bmiHeader.biWidth * abs(bmi.bmiHeader.biHeight)
        buffer = ctypes.create_string_buffer(buffer_size)
        
        if not gdi32.GetDIBits(memdc, bmp, 0, height, buffer, ctypes.byref(bmi), DIB_RGB_COLORS):
            raise ToolsEorror("ToolsError: Failed to obtain pixel data")
        return buffer, buffer_size

    def _save_as_png(self, width: int, height: int, buffer, path: str):
        try:
            pixels = bytearray()
            stride = (width * 3 + 3) & ~3 
            
            for y in range(height):
                offset = y * stride
                row = buffer[offset:offset + width*3]
                
                pixels.append(0)
                
                for i in range(0, len(row), 3):
                    pixels.append(row[i+2])
                    pixels.append(row[i+1])
                    pixels.append(row[i])

            compressor = zlib.compressobj(level=9)
            compressed = compressor.compress(bytes(pixels))
            compressed += compressor.flush()

            with open(path, 'wb') as f:
                f.write(b"\x89PNG\r\n\x1a\n")
                
                ihdr_data = struct.pack(">I", width)          # 宽度
                ihdr_data += struct.pack(">I", height)        # 高度
                ihdr_data += struct.pack(">B", 8)            # 位深
                ihdr_data += struct.pack(">B", 2)             # 颜色类型（真彩色）
                ihdr_data += struct.pack(">BBB", 0, 0, 0)     # 压缩/过滤/隔行
                
                ihdr_chunk = struct.pack(">I", 13)           # 数据长度
                ihdr_chunk += b"IHDR"
                ihdr_chunk += ihdr_data
                ihdr_chunk += struct.pack(">I", zlib.crc32(ihdr_chunk[4:]))
                f.write(ihdr_chunk)

                idat_chunk = struct.pack(">I", len(compressed))
                idat_chunk += b"IDAT"
                idat_chunk += compressed
                idat_chunk += struct.pack(">I", zlib.crc32(idat_chunk[4:]))
                f.write(idat_chunk)

                f.write(b"\x00\x00\x00\x00IEND\xae\x42\x60\x82")
                
        except Exception as e:
            raise ToolsEorror(f"ToolsError: PNG encoding failed: {str(e)}")

    def _save_as_bmp(self, width: int, height: int, buffer, bmi, path: str):
        try:
            with open(path, 'wb') as f:
                file_header = struct.pack("<HLHHL", 
                    0x4D42,
                    54 + len(buffer),
                    0, 0, 54 
                )
                f.write(file_header)
                
                info_header = struct.pack("<LllHHLLllLL", 
                    bmi.bmiHeader.biSize,
                    width,
                    height,
                    1,
                    24, 
                    0, 0, 0, 0, 0, 0
                )
                f.write(info_header)
                f.write(buffer)
        except struct.error as e:
            raise ToolsEorror(f"ToolsError: BMP encoding failed: {str(e)}")
    
    def _macos_screenshot(self, x, y, e_x, e_y, filename, path):
        save_path = os.path.join(path or os.getcwd(), filename)
        
        width = e_x - x
        height = e_y - y
        geometry = f"-R{x},{y},{width},{height}"
        
        cmd = f"screencapture {geometry} -x {save_path}"
        if os.system(cmd) != 0:
            raise ToolsEorror("ToolsError: MacOS screenshot command execution failed")
        return save_path

    def _linux_screenshot(self, x, y, e_x, e_y, filename, path):
        save_dir = path or os.getcwd()
        save_path = os.path.join(save_dir, filename)
        
        if os.system("which scrot >/dev/null") != 0:
            raise ToolsEorror("ToolsError: Please install Scrot first. The command is: sudo apt-get install scrot")
        
        geometry = f"{e_x - x}x{e_y - y}+{x}+{y}"
        cmd = f"scrot -a {geometry} -q 100 -e 'mv $f {save_path}'"
        if os.system(cmd) != 0:
            raise ToolsEorror("ToolsError: Linux screenshot failed")
        return save_path

    def md_full_screenshot(self, filename: str, path: Optional[str] = None, wait_time: float = 0) -> str:
        """
        截取全屏截图
        :param filename: 保存文件名（必传，支持.bmp或.png格式）
        :param path: 保存路径（默认当前目录）
        :param wait_time: 截图前等待时间（秒，默认0）
        :return: 保存的文件完整路径
        """
        """
        :param filename: 保存文件名（必须包含.png或.bmp扩展名）
        :param path: 保存路径（默认当前目录）
        :return: 完整文件路径
        """
        try:
            time.sleep(wait_time)
            # 参数验证
            if not filename:
                raise ToolsEorror("ToolsError: Filename cannot be empty")
            if not filename.lower().endswith(('.png', '.bmp')):
                raise ToolsEorror("ToolsError: Unsupported file format, use .png or .bmp")
            root = Tk()
            root.withdraw()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            
            if platform.system() == "Windows":
                try:
                    ctypes.windll.shcore.SetProcessDpiAwareness(2)
                    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
                    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
                except:
                    pass
            
            root.destroy()

            return self.md_screenshot(
                x=0,
                y=0,
                e_x=screen_width,
                e_y=screen_height,
                filename=filename,
                path=path
            )

        except PermissionError as e:
            raise ToolsEorror(f"ToolsError: Permission denied: {str(e)}")
        except FileNotFoundError as e:
            raise ToolsEorror(f"ToolsError: Path not found: {str(e)}")
        except Exception as e:
            raise ToolsEorror(f"ToolsError: Full screen capture failed: {str(e)}")
