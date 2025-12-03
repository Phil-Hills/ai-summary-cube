import json
import gzip
import base64
import math
import hashlib

class CubeProtocol:
    """
    Core CUBE Protocol compressor.

    Implements:
      - Data-specific preprocessing
      - gzip compression
      - base64 encoding
      - cube slicing (3D)
      - Trinity descriptor assembly
      - SHA256 integrity hashing

    Output matches the documented CUBE Protocol structure.
    """

    @staticmethod
    def _preprocess(data: str) -> bytes:
        """
        Data-specific optimization/minification.
        Future versions can apply HTML minifiers, JSON compaction, etc.
        """
        return data.encode("utf-8")

    @staticmethod
    def _compress(raw: bytes) -> bytes:
        """gzip deflation."""
        return gzip.compress(raw, compresslevel=9)

    @staticmethod
    def _encode(b: bytes) -> str:
        """Base64 encode to produce safe string."""
        return base64.b64encode(b).decode("ascii")

    @staticmethod
    def _cube_dimensions(n: int):
        """
        Compute 3D cube dimensions. Uses cubic root for balanced shape.
        Ensures minimum side of 1.
        """
        side = max(1, int(round(n ** (1/3))))
        return (side, side, side)

    @staticmethod
    def _slice_to_cube(encoded: str, dims):
        """
        Slice the base64 string into a 3D cube array represented as a single
        flattened string. Pads with '=' for exact fitting.
        """
        x, y, z = dims
        total = x * y * z
        padded = encoded.ljust(total, "=")
        return padded[:total]

    @classmethod
    def compress(cls, data: str, domain: str, sequence: str, outcome: str):
        """
        Main entry. Compress a string using the CUBE Protocol.

        Returns a CubeObject containing:
          - descriptor
          - cube dimensions
          - base64 cube data
          - generated SHA256 hash
        """
        raw = cls._preprocess(data)
        compressed = cls._compress(raw)
        encoded = cls._encode(compressed)

        dims = cls._cube_dimensions(len(encoded))
        sliced = cls._slice_to_cube(encoded, dims)

        descriptor = f"{domain}|{sequence}|{outcome}"

        return CubeObject(descriptor, dims, sliced)


class CubeObject:
    """Encapsulates the final cube + metadata."""
    
    def __init__(self, descriptor, dimensions, data):
        self.descriptor = descriptor
        self.dimensions = dimensions
        self.data = data

    def sha256(self):
        raw = base64.b64decode(self.data)
        return hashlib.sha256(raw).hexdigest()

    def as_dict(self):
        return {
            "protocol_version": "cube-1.0",
            "descriptor": self.descriptor,
            "cube": {
                "dimensions": list(self.dimensions),
                "encoding": "base64",
                "data": self.data
            },
            "hash": {
                "algorithm": "SHA256",
                "value": self.sha256()
            }
        }
