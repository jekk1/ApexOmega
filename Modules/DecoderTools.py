import base64
import urllib.parse
import html
import binascii
import re
import json
from typing import Optional, List, Dict, Tuple
from collections import OrderedDict


class DecoderTools:
    """Universal decoder dengan automatic detection dan manual mode."""
    
    def __init__(self):
        self.encoding_history = []
        
    # ========== AUTO DETECTION ENGINE ==========
    
    def auto_decode(self, encoded_text: str) -> Dict[str, any]:
        """
        Automatic decoder yang mencoba semua tipe encoding dan return hasil terbaik.
        
        Returns:
            Dict dengan keys: 'success', 'decoded_text', 'encoding_type', 'confidence', 'all_results'
        """
        if not encoded_text or not encoded_text.strip():
            return {
                'success': False,
                'decoded_text': '',
                'encoding_type': 'None',
                'confidence': 0,
                'all_results': [],
                'error': 'Empty input'
            }
        
        encoded_text = encoded_text.strip()
        all_results = []
        best_result = None
        best_confidence = 0
        
        # Daftar semua decoder yang tersedia
        decoders = [
            ('Base64', self._decode_base64),
            ('Base64 URL-Safe', self._decode_base64_url),
            ('URL Encode', self._decode_url),
            ('HTML Entities', self._decode_html),
            ('Hex', self._decode_hex),
            ('Binary', self._decode_binary),
            ('Rot13', self._decode_rot13),
            ('Reverse', self._decode_reverse),
            ('Base32', self._decode_base32),
            ('Base85', self._decode_base85),
            ('ASCII85', self._decode_ascii85),
            ('URL Double', self._decode_url_double),
            ('Base64 Double', self._decode_base64_double),
        ]
        
        # Coba semua decoder
        for encoding_name, decoder_func in decoders:
            try:
                decoded, confidence, is_readable = decoder_func(encoded_text)
                
                if decoded and confidence > 0:
                    result = {
                        'encoding': encoding_name,
                        'decoded': decoded,
                        'confidence': confidence,
                        'readable': is_readable
                    }
                    all_results.append(result)
                    
                    # Update best result (prioritaskan yang readable dan confidence tinggi)
                    if is_readable and confidence > best_confidence:
                        best_confidence = confidence
                        best_result = result
                    elif not best_result and confidence > best_confidence:
                        best_confidence = confidence
                        best_result = result
                        
            except Exception:
                continue
        
        # Sort results by confidence
        all_results.sort(key=lambda x: (x['readable'], x['confidence']), reverse=True)
        
        if best_result:
            return {
                'success': True,
                'decoded_text': best_result['decoded'],
                'encoding_type': best_result['encoding'],
                'confidence': best_result['confidence'],
                'readable': best_result['readable'],
                'all_results': all_results,
                'error': None
            }
        else:
            return {
                'success': False,
                'decoded_text': '',
                'encoding_type': 'Unknown',
                'confidence': 0,
                'all_results': all_results,
                'error': 'No successful decoding found'
            }
    
    # ========== INDIVIDUAL DECODERS ==========
    
    def _decode_base64(self, text: str) -> Tuple[str, float, bool]:
        """Decode Base64 standard."""
        try:
            # Padding fix
            padding_needed = len(text) % 4
            if padding_needed:
                text += '=' * (4 - padding_needed)
            
            decoded_bytes = base64.b64decode(text, validate=False)
            decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
            
            confidence = self._calculate_confidence(decoded_str)
            is_readable = self._is_readable_text(decoded_str)
            
            return decoded_str, confidence, is_readable
        except Exception:
            return '', 0, False
    
    def _decode_base64_url(self, text: str) -> Tuple[str, float, bool]:
        """Decode Base64 URL-safe."""
        try:
            # Convert URL-safe chars to standard
            text = text.replace('-', '+').replace('_', '/')
            padding_needed = len(text) % 4
            if padding_needed:
                text += '=' * (4 - padding_needed)
            
            decoded_bytes = base64.b64decode(text, validate=False)
            decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
            
            confidence = self._calculate_confidence(decoded_str)
            is_readable = self._is_readable_text(decoded_str)
            
            return decoded_str, confidence, is_readable
        except Exception:
            return '', 0, False
    
    def _decode_base64_double(self, text: str) -> Tuple[str, float, bool]:
        """Decode Base64 dua kali (nested encoding)."""
        try:
            first_decode, _, _ = self._decode_base64(text)
            if first_decode:
                second_decode, conf, readable = self._decode_base64(first_decode)
                if second_decode and conf > 0.5:
                    return second_decode, conf * 0.9, readable
        except Exception:
            pass
        return '', 0, False
    
    def _decode_base32(self, text: str) -> Tuple[str, float, bool]:
        """Decode Base32."""
        try:
            text = text.upper().replace('=', '')
            padding_needed = len(text) % 8
            if padding_needed:
                text += '=' * (8 - padding_needed)
            
            decoded_bytes = base64.b32decode(text)
            decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
            
            confidence = self._calculate_confidence(decoded_str)
            is_readable = self._is_readable_text(decoded_str)
            
            return decoded_str, confidence, is_readable
        except Exception:
            return '', 0, False
    
    def _decode_base85(self, text: str) -> Tuple[str, float, bool]:
        """Decode Base85 (Ascii85 variant)."""
        try:
            decoded_bytes = base64.b85decode(text)
            decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
            
            confidence = self._calculate_confidence(decoded_str)
            is_readable = self._is_readable_text(decoded_str)
            
            return decoded_str, confidence, is_readable
        except Exception:
            return '', 0, False
    
    def _decode_ascii85(self, text: str) -> Tuple[str, float, bool]:
        """Decode ASCII85 (Adobe variant)."""
        try:
            decoded_bytes = base64.a85decode(text)
            decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
            
            confidence = self._calculate_confidence(decoded_str)
            is_readable = self._is_readable_text(decoded_str)
            
            return decoded_str, confidence, is_readable
        except Exception:
            return '', 0, False
    
    def _decode_url(self, text: str) -> Tuple[str, float, bool]:
        """Decode URL encoding (%XX)."""
        try:
            decoded_str = urllib.parse.unquote(text)
            
            # Check if actually decoded
            if decoded_str != text:
                confidence = self._calculate_confidence(decoded_str)
                is_readable = self._is_readable_text(decoded_str)
                return decoded_str, confidence, is_readable
            
            return '', 0, False
        except Exception:
            return '', 0, False
    
    def _decode_url_double(self, text: str) -> Tuple[str, float, bool]:
        """Decode URL encoding dua kali (nested)."""
        try:
            first_decode = urllib.parse.unquote(text)
            second_decode = urllib.parse.unquote(first_decode)
            
            if second_decode != text and second_decode != first_decode:
                confidence = self._calculate_confidence(second_decode)
                is_readable = self._is_readable_text(second_decode)
                return second_decode, confidence * 0.9, is_readable
        except Exception:
            pass
        return '', 0, False
    
    def _decode_html(self, text: str) -> Tuple[str, float, bool]:
        """Decode HTML entities (&#xXX;, &amp;, dll)."""
        try:
            decoded_str = html.unescape(text)
            
            if decoded_str != text:
                confidence = self._calculate_confidence(decoded_str)
                is_readable = self._is_readable_text(decoded_str)
                return decoded_str, confidence, is_readable
            
            return '', 0, False
        except Exception:
            return '', 0, False
    
    def _decode_hex(self, text: str) -> Tuple[str, float, bool]:
        """Decode Hexadecimal (0x, \\x, atau plain hex)."""
        try:
            # Clean text dari prefix
            clean_text = text.replace('0x', '').replace('\\x', '').replace(' ', '')
            
            # Validate hex characters
            if not all(c in '0123456789abcdefABCDEF' for c in clean_text):
                return '', 0, False
            
            # Ensure even length
            if len(clean_text) % 2 != 0:
                clean_text = '0' + clean_text
            
            decoded_bytes = bytes.fromhex(clean_text)
            decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
            
            confidence = self._calculate_confidence(decoded_str)
            is_readable = self._is_readable_text(decoded_str)
            
            return decoded_str, confidence, is_readable
        except Exception:
            return '', 0, False
    
    def _decode_binary(self, text: str) -> Tuple[str, float, bool]:
        """Decode Binary (8-bit per character)."""
        try:
            # Extract binary patterns
            binary_strings = re.findall(r'[01]{8}', text)
            
            if not binary_strings:
                return '', 0, False
            
            decoded_chars = []
            for binary in binary_strings:
                char_code = int(binary, 2)
                if 32 <= char_code <= 126 or char_code in (9, 10, 13):  # Printable ASCII
                    decoded_chars.append(chr(char_code))
            
            decoded_str = ''.join(decoded_chars)
            
            if decoded_str:
                confidence = self._calculate_confidence(decoded_str)
                is_readable = self._is_readable_text(decoded_str)
                return decoded_str, confidence, is_readable
            
            return '', 0, False
        except Exception:
            return '', 0, False
    
    def _decode_rot13(self, text: str) -> Tuple[str, float, bool]:
        """Decode ROT13 cipher."""
        try:
            decoded_str = ''
            for char in text:
                if 'a' <= char <= 'z':
                    decoded_str += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
                elif 'A' <= char <= 'Z':
                    decoded_str += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
                else:
                    decoded_str += char
            
            # ROT13 confidence rendah kecuali ada pattern khusus
            confidence = 0.3
            is_readable = self._is_readable_text(decoded_str)
            
            # Increase confidence jika hasil lebih readable dari input
            if is_readable and not self._is_readable_text(text):
                confidence = 0.8
            
            return decoded_str, confidence, is_readable
        except Exception:
            return '', 0, False
    
    def _decode_reverse(self, text: str) -> Tuple[str, float, bool]:
        """Decode reverse string."""
        try:
            decoded_str = text[::-1]
            confidence = 0.2  # Low confidence by default
            is_readable = self._is_readable_text(decoded_str)
            
            # Increase confidence jika reverse lebih readable
            if is_readable and not self._is_readable_text(text):
                confidence = 0.7
            
            return decoded_str, confidence, is_readable
        except Exception:
            return '', 0, False
    
    # ========== HELPER METHODS ==========
    
    def _calculate_confidence(self, text: str) -> float:
        """
        Hitung confidence score berdasarkan karakteristik teks.
        Score 0.0 - 1.0
        """
        if not text:
            return 0.0
        
        # Printable character ratio
        printable_count = sum(1 for c in text if c.isprintable() or c in '\n\r\t')
        printable_ratio = printable_count / len(text)
        
        # Letter ratio (alphabetic characters)
        letter_count = sum(1 for c in text if c.isalpha())
        letter_ratio = letter_count / len(text) if len(text) > 0 else 0
        
        # Space ratio (normal text has spaces)
        space_count = text.count(' ')
        space_ratio = space_count / len(text) if len(text) > 0 else 0
        
        # Common word patterns
        common_patterns = ['the', 'and', 'is', 'are', 'was', 'were', 'be', 'to', 'of', 
                          'in', 'for', 'on', 'with', 'that', 'this', 'http', 'www',
                          'admin', 'password', 'user', 'login', 'success', 'error']
        text_lower = text.lower()
        pattern_matches = sum(1 for pattern in common_patterns if pattern in text_lower)
        pattern_score = min(pattern_matches * 0.1, 0.3)
        
        # Calculate final confidence
        confidence = (
            printable_ratio * 0.3 +
            letter_ratio * 0.2 +
            (1.0 if 0.05 < space_ratio < 0.2 else 0.5) * 0.2 +
            pattern_score
        )
        
        return min(confidence, 1.0)
    
    def _is_readable_text(self, text: str) -> bool:
        """
        Cek apakah teks bisa dibaca manusia (human-readable).
        """
        if not text:
            return False
        
        # Check printable ratio
        printable_count = sum(1 for c in text if c.isprintable() or c in '\n\r\t')
        printable_ratio = printable_count / len(text)
        
        if printable_ratio < 0.8:
            return False
        
        # Check if contains meaningful content
        has_letters = any(c.isalpha() for c in text)
        has_spaces = ' ' in text
        has_common_words = any(word in text.lower() for word in ['the', 'and', 'is', 'are', 'was'])
        
        return has_letters and (has_spaces or has_common_words)
    
    # ========== MANUAL DECODER (Specific) ==========
    
    def manual_decode(self, text: str, encoding_type: str) -> Dict[str, any]:
        """
        Manual decoder untuk encoding spesifik.
        
        Args:
            text: Input encoded text
            encoding_type: Tipe encoding ('base64', 'url', 'hex', 'html', 'binary', 'rot13', dll)
        
        Returns:
            Dict dengan hasil decode
        """
        encoding_type = encoding_type.lower().strip()
        
        decoder_map = {
            'base64': self._decode_base64,
            'base64url': self._decode_base64_url,
            'base64double': self._decode_base64_double,
            'base32': self._decode_base32,
            'base85': self._decode_base85,
            'ascii85': self._decode_ascii85,
            'url': self._decode_url,
            'urldouble': self._decode_url_double,
            'html': self._decode_html,
            'hex': self._decode_hex,
            'binary': self._decode_binary,
            'rot13': self._decode_rot13,
            'reverse': self._decode_reverse,
        }
        
        decoder_func = decoder_map.get(encoding_type)
        
        if not decoder_func:
            return {
                'success': False,
                'decoded_text': '',
                'encoding_type': encoding_type,
                'error': f'Unknown encoding type: {encoding_type}'
            }
        
        try:
            decoded, confidence, readable = decoder_func(text)
            
            if decoded:
                return {
                    'success': True,
                    'decoded_text': decoded,
                    'encoding_type': encoding_type,
                    'confidence': confidence,
                    'readable': readable,
                    'error': None
                }
            else:
                return {
                    'success': False,
                    'decoded_text': '',
                    'encoding_type': encoding_type,
                    'error': 'Decoding failed - invalid input format'
                }
        except Exception as e:
            return {
                'success': False,
                'decoded_text': '',
                'encoding_type': encoding_type,
                'error': str(e)
            }
    
    # ========== ENCODER (Reverse Operations) ==========
    
    def encode(self, text: str, encoding_type: str) -> Dict[str, any]:
        """
        Encode text ke berbagai format.
        """
        encoding_type = encoding_type.lower().strip()
        
        try:
            if encoding_type == 'base64':
                encoded = base64.b64encode(text.encode()).decode()
            elif encoding_type == 'base64url':
                encoded = base64.urlsafe_b64encode(text.encode()).decode()
            elif encoding_type == 'base32':
                encoded = base64.b32encode(text.encode()).decode()
            elif encoding_type == 'base85':
                encoded = base64.b85encode(text.encode()).decode()
            elif encoding_type == 'ascii85':
                encoded = base64.a85encode(text.encode()).decode()
            elif encoding_type == 'url':
                encoded = urllib.parse.quote(text, safe='')
            elif encoding_type == 'html':
                encoded = html.escape(text)
            elif encoding_type == 'hex':
                encoded = text.encode().hex()
            elif encoding_type == 'binary':
                encoded = ' '.join(format(ord(c), '08b') for c in text)
            elif encoding_type == 'rot13':
                encoded = ''
                for char in text:
                    if 'a' <= char <= 'z':
                        encoded += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
                    elif 'A' <= char <= 'Z':
                        encoded += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
                    else:
                        encoded += char
            elif encoding_type == 'reverse':
                encoded = text[::-1]
            else:
                return {
                    'success': False,
                    'encoded_text': '',
                    'error': f'Unknown encoding type: {encoding_type}'
                }
            
            return {
                'success': True,
                'encoded_text': encoded,
                'encoding_type': encoding_type,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'encoded_text': '',
                'error': str(e)
            }
    
    # ========== BATCH DECODER ==========
    
    def batch_decode(self, text_list: List[str], auto: bool = True) -> List[Dict]:
        """
        Decode multiple inputs sekaligus.
        """
        results = []
        
        for text in text_list:
            if auto:
                result = self.auto_decode(text)
            else:
                result = {'input': text, 'note': 'Manual mode requires encoding_type'}
            
            results.append(result)
        
        return results
    
    # ========== CHAIN DECODER (Multi-layer) ==========
    
    def chain_decode(self, text: str, max_iterations: int = 5) -> Dict[str, any]:
        """
        Decode berlapis otomatis (nested encoding).
        Contoh: Base64(URL(Hex(text)))
        """
        iterations = []
        current_text = text
        
        for i in range(max_iterations):
            result = self.auto_decode(current_text)
            
            if not result['success']:
                break
            
            iterations.append({
                'iteration': i + 1,
                'encoding': result['encoding_type'],
                'decoded': result['decoded_text'],
                'confidence': result['confidence']
            })
            
            # Stop jika sudah tidak bisa decode lagi atau sudah readable
            if result['confidence'] < 0.5 or result['readable']:
                break
            
            current_text = result['decoded_text']
        
        return {
            'success': len(iterations) > 0,
            'original': text,
            'final': current_text,
            'iterations': iterations,
            'total_layers': len(iterations)
        }
