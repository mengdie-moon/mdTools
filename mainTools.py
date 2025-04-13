"""
@Author   : 梦蝶
@Contact  : 3257053519@qq.com
@CallMe   : 3257053519
@Copyright: (c) 2025 by 梦蝶, Inc. All Rights Reserved.
"""

import random
import re
import os
import base64
import hashlib
import binascii
from mdToolsError import ToolsEorror

class mdTools_main:
    # Base64 标准字符集
    _STANDARD_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    _URL_SAFE_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    def __init__(self):
        self._encode_map = {}
        self._decode_map = {}

    def randomPassword(self, length: int = 10, isNumber: bool = True, isStr: bool = True, isNotation: bool = False) -> str:
        """
        生成随机密码
        :param length: 密码长度（默认10）
        :param isNumber: 是否包含数字（默认True）
        :param isStr: 是否包含字母（默认True）
        :param isNotation: 是否包含特殊字符（默认False）
        :return: 生成的随机密码字符串
        """
        numbers = '0123456789'
        letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        notations = '!@#$%&-+=/*,;:[]{}|'
        if not any([isNumber, isStr, isNotation]):
            raise ToolsEorror("ToolsError: At least one character type must be enabled")
        charset = []
        if isNumber:
            charset.append(numbers)
        if isStr:
            charset.append(letters)
        if isNotation:
            charset.append(notations)
        combined = ''.join(charset)
        return ''.join(random.SystemRandom().choice(combined) for _ in range(length))
    def base64_encode(self, data: str | bytes, url_safe: bool = False, encoding: str = 'utf-8') -> str:
        """
        Base64编码
        :param data: 要编码的数据（字符串或字节）
        :param url_safe: 是否使用URL安全的字符集（默认False）
        :param encoding: 字符编码（默认utf-8）
        :return: Base64编码后的字符串
        """
        if not isinstance(data, (str, bytes)):
            raise ToolsEorror(f"ToolsError: Invalid input type: {type(data).__name__}")
        if not data:
            raise ToolsEorror("ToolsError: Empty input data")
        try:
            byte_data = data.encode(encoding) if isinstance(data, str) else data
        except (UnicodeEncodeError, LookupError) as e:
            raise ToolsEorror(f"Encoding error: {e}")
        try:
            if url_safe:
                encoded_bytes = base64.urlsafe_b64encode(byte_data)
            else:
                encoded_bytes = base64.b64encode(byte_data)
        except Exception as e:
            raise ToolsEorror(f"Encoding error: {e}")
        return encoded_bytes.decode('ascii')

    def base64_decode(self, encoded_data: str | bytes, url_safe: bool = False, encoding: str = 'utf-8') -> str | bytes:
        """
        Base64解码
        :param encoded_data: 要解码的Base64数据（字符串或字节）
        :param url_safe: 是否使用URL安全的字符集（默认False）
        :param encoding: 字符编码（默认utf-8）
        :return: 解码后的字符串或字节
        """
        if not isinstance(encoded_data, (str, bytes)):
            raise ToolsEorror(f"ToolsError: Invalid input type: {type(encoded_data).__name__}")
        if not encoded_data:
            raise ToolsEorror("ToolsError: Empty input data")
        if isinstance(encoded_data, bytes):
            try:
                encoded_str = encoded_data.decode('ascii')
            except UnicodeDecodeError as e:
                raise ToolsEorror(f"ToolsError: Invalid ASCII data: {e}")
        else:
            encoded_str = encoded_data
        if len(encoded_str) % 4 != 0:
            raise ToolsEorror("ToolsError: Invalid length (must be multiple of 4)")
        if not re.match(r'^[A-Za-z0-9+/=_-]*$', encoded_str):
            raise ToolsEorror("ToolsError: Invalid character detected")
        if url_safe:
            encoded_str = encoded_str.replace('-', '+').replace('_', '/')
        pad_count = encoded_str.count('=', 0, len(encoded_str) - 2)
        if pad_count > 2:
            raise ToolsEorror("ToolsError: Excessive padding characters")
        try:
            decoded_bytes = base64.b64decode(encoded_str)
        except binascii.Error as e:
            raise ToolsEorror(f"ToolsError: Decoding error: {e}")
        try:
            return decoded_bytes.decode(encoding)
        except (UnicodeDecodeError, LookupError) as e:
            raise ToolsEorror(f"Decoding error: {e}")

    def base64_encode_file(self, file_path: str, url_safe: bool = False, encoding: str = 'utf-8', output_file: str = None) -> str | None:
        """
        对文件进行Base64编码
        :param file_path: 要编码的文件路径
        :param url_safe: 是否使用URL安全的字符集（默认False）
        :param encoding: 字符编码（默认utf-8）
        :param output_file: 输出文件路径（默认None，直接返回编码结果）
        :return: 如果指定输出文件则返回None，否则返回编码后的字符串
        """
        if not os.path.exists(file_path):
            raise ToolsEorror(f"ToolsError: Input file not found: {file_path}")
        
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
        except IOError as e:
            raise ToolsEorror(f"ToolsError: File read error: {e}")
        
        encoded = self.base64_encode(file_data, url_safe=url_safe, encoding=encoding)
        
        if isinstance(encoded, str) and "ToolsError" in encoded:
            return encoded
        if output_file:
            try:
                with open(output_file, 'w', encoding=encoding) as f:
                    f.write(encoded)
            except IOError as e:
                raise ToolsEorror(f"ToolsError: Output file write error: {e}")
            return None
        else:
            return encoded

    def base64_decode_file(self, file_path: str, url_safe: bool = False, encoding: str = 'utf-8', output_file: str = None) -> str | bytes | None:
        """
        对Base64编码的文件进行解码
        :param file_path: 要解码的文件路径
        :param url_safe: 是否使用URL安全的字符集（默认False）
        :param encoding: 字符编码（默认utf-8）
        :param output_file: 输出文件路径（默认None，直接返回解码结果）
        :return: 如果指定输出文件则返回None，否则返回解码后的字符串或字节
        """
        if not os.path.exists(file_path):
            raise ToolsEorror(f"ToolsError: Input file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='ascii') as f:
                base64_str = f.read()
        except (IOError, UnicodeDecodeError) as e:
            raise ToolsEorror(f"ToolsError: File read error: {e}")
        
        decoded = self.base64_decode(base64_str, url_safe=url_safe, encoding=encoding)
        
        if isinstance(decoded, str) and "ToolsError" in decoded:
            return decoded
        
        if output_file:
            try:
                with open(output_file, 'wb') as f:
                    f.write(decoded if isinstance(decoded, bytes) else decoded.encode(encoding))
            except IOError as e:
                raise ToolsEorror(f"ToolsError: Output file write error: {e}")
            return None
        else:
            return decoded    
    def md5_hash(self, data: str | bytes, encoding: str = 'utf-8') -> str:
        """
        计算MD5哈希值
        :param data: 要计算哈希的数据（字符串或字节）
        :param encoding: 字符编码（默认utf-8）
        :return: 32位MD5哈希值字符串
        """
        if not isinstance(data, (str, bytes)):
            raise ToolsEorror(f"ToolsError: Invalid input type: {type(data).__name__}")
        
        try:
            byte_data = data.encode(encoding) if isinstance(data, str) else data
            hash_obj = hashlib.md5(byte_data)
            return hash_obj.hexdigest()
        except (UnicodeEncodeError, LookupError) as e:
            raise ToolsEorror(f"ToolsError: code error: {e}")

    def md5_hash_file(self, input_file: str,  output_file: str = None, chunk_size: int = 8192) -> str | None:
        """
        计算文件的MD5哈希值
        :param input_file: 输入文件路径
        :param output_file: 输出文件路径（默认None，直接返回哈希值）
        :param chunk_size: 读取文件的块大小（默认8192字节）
        :return: 如果指定输出文件则返回None，否则返回32位MD5哈希值字符串
        """
        try:
            hash_obj = hashlib.md5()
            try:
                with open(input_file, 'rb') as f:
                    while chunk := f.read(chunk_size):
                        hash_obj.update(chunk)
            except FileNotFoundError:
                raise ToolsEorror(f"ToolsError: file not found: {input_file}")
            except IOError as e:
                raise ToolsEorror(f"ToolsError: file read error: {e}")
            hex_digest = hash_obj.hexdigest()
        except Exception as e:
            raise ToolsEorror(f"ToolsError: unknown error: {e}")
        
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(hex_digest)
            except IOError as e:
                raise ToolsEorror(f"ToolsError: hash write failed: {e}")
            return None
        else:
            return hex_digest
            
    def random_user_agent(self, num: int = 1, devices: list = ["pc", "mobile", "tablet"], browsers: list = ["chrome", "firefox", "safari", "edge"], device_weights: list = None) -> str | list:
        """
        生成随机User-Agent
        :param num: 生成数量（默认1）
        :param devices: 设备类型列表（默认["pc", "mobile", "tablet"]）
        :param browsers: 浏览器类型列表（默认["chrome", "firefox", "safari", "edge"]）
        :param device_weights: 设备类型权重列表（默认None，使用内置权重）
        :return: 当num=1时返回字符串，否则返回User-Agent列表
        """
        if num < 1:
            raise ToolsEorror("ToolsError: The generated quantity must be ≥ 1")
                
        valid_devices = ["pc", "mobile", "tablet"]
        if invalid := [d for d in devices if d not in valid_devices]:
            raise ToolsEorror(f"ToolsError: Invalid device type: {invalid}, optional:{valid_devices}")

        valid_browsers = ["chrome", "firefox", "safari", "edge"]
        if invalid := [b for b in browsers if b not in valid_browsers]:
            raise ToolsEorror(f"ToolsError: Invalid browser type: {invalid}, optional:{valid_browsers}")

        DEFAULT_WEIGHTS = {"pc": 35, "mobile": 50, "tablet": 15}
        if device_weights:
            if len(device_weights) != len(devices):
                raise ToolsEorror(f"ToolsError: Number of weights ({len(device_weights)}) number of devices ({len(devices)}) mismatched")
            if not all(isinstance(w, (int, float)) for w in device_weights):
                raise ToolsEorror("ToolsError: Weight must be of numeric type")
            if sum(device_weights) <= 0:
                raise ToolsEorror("ToolsError: The total weight must be greater than 0")
            valid_weights = device_weights
        else:
            valid_weights = [DEFAULT_WEIGHTS[d] for d in devices]

        VERSION_POOL = {
            "chrome": {
                "pc": [("121", "6167"), ("120", "6099")],
                "mobile": [("121", "6167"), ("120", "6099")],
                "tablet": [("121", "6167"), ("120", "6099")]
            },
            "firefox": {
                "pc": [("115", "0"), ("110", "0")],
                "mobile": [("115", "0"), ("110", "0")]
            },
            "safari": {
                "pc": [("16", "6"), ("17", "3")],
                "mobile": [("17", "3"), ("16", "6")],
                "tablet": [("17", "3"), ("16", "6")]
            },
            "edge": {
                "pc": [("121", "0"), ("120", "0")],
                "tablet": [("121", "0")]
            }
        }

        OS_TEMPLATES = {
            "pc": [
                ("Windows NT 10.0; Win64; x64", 0.4),
                ("Windows NT 11.0; Win64; x64", 0.3),
                ("Macintosh; Intel Mac OS X 10_15_7", 0.2),
                ("X11; Linux x86_64", 0.1)
            ],
            "mobile": [
                ("Linux; Android 14; SM-S901B", 0.5),
                ("iPhone; CPU iPhone OS 17_3_1 like Mac OS X", 0.5)
            ],
            "tablet": [
                ("iPad; CPU OS 17_3_1 like Mac OS X", 0.6),
                ("Linux; Android 13; SM-X700", 0.4)
            ]
        }
        WEIGHTS_MAP = {"pc": 35, "mobile": 50, "tablet": 15}
        valid_weights = [WEIGHTS_MAP[d] for d in devices]
        ua_list = []
        for _ in range(num):
            device = random.choices(devices, weights=valid_weights, k=1)[0]
            browser = random.choice(browsers)
                
            if device == "tablet":
                if browser == "safari": browser = "chrome"
                if browser == "edge" and device not in VERSION_POOL["edge"]: browser = "chrome"
            elif device == "mobile":
                if browser == "edge": browser = "chrome"

            os_options, weights = zip(*OS_TEMPLATES[device])
            os_template = random.choices(os_options, weights=weights, k=1)[0]

            try:
                version, build = random.choice(VERSION_POOL[browser][device])
            except KeyError:
                version, build = "121", "6167"  
                browser = "chrome"

            device_id = ""
            if "Android" in os_template:
                device_id = f"; {random.choice(['SM-G998B', 'M2012K11AG', 'SM-S9010'])}"
            elif "iPhone" in os_template:
                device_id = f"; {random.choice(['iPhone15,3', 'iPhone14,2', 'iPhone13,2'])}"

            platform = ""
            if device == "mobile" and "iPhone" not in os_template:
                platform = "Mobile "
            elif device == "tablet":
                platform = "Tablet " if "iPad" not in os_template else ""

            ua = f"Mozilla/5.0 ({os_template}{device_id}) AppleWebKit/537.36 (KHTML, like Gecko) "
                
            if browser == "chrome":
                ua += f"Chrome/{version}.0.{build}.{random.randint(100,999)} {platform}Safari/537.36"
            elif browser == "firefox":
                ua += f"Firefox/{version}.{build}"
            elif browser == "safari":
                ua += f"Version/{version}.{build} Safari/605.1.15"
            elif browser == "edge":
                ua += f"Edg/{version}.0.{build}.{random.randint(100,999)}"

            ua_list.append(ua)

        return ua_list[0] if num == 1 else ua_list

    def random_ip(self, num: int = 1) -> str | list:
        """
        生成随机有效的公网IPv4地址
        """
        if not isinstance(num, int) or num < 1:
            raise ToolsEorror("ToolsError: 生成数量必须为≥1的整数")

        def _is_private(octets: list) -> bool:
            """检查是否为保留地址"""
            if octets[0] == 0: return True
            if octets[0] == 10: return True
            if octets[0] == 127: return True
            if octets[0] == 169 and octets[1] == 254: return True
            if octets[0] == 172 and 16 <= octets[1] <=31: return True
            if octets[0] == 192 and octets[1] == 168: return True
            if octets[0] >= 224: return True    
            return False

        ips = []
        for _ in range(num):
            while True:
                first_octet = random.randint(1, 223)
                if first_octet in (10, 127) or first_octet >= 224:
                    continue
                if first_octet == 172:
                    second_octet = random.randint(16, 31)
                else:
                    second_octet = random.randint(0, 255)
                
                third_octet = random.randint(0, 255)
                fourth_octet = random.randint(1, 254)
                
                octets = [first_octet, second_octet, third_octet, fourth_octet]
                if not _is_private(octets):
                    ips.append(".".join(map(str, octets)))
                    break

        return ips[0] if num == 1 else ips
    