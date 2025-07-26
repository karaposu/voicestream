"""
VoxStream Buffer Management

High-performance buffer management for real-time streaming.
Zero-copy buffer pools and streaming buffers for minimal latency.
"""

import threading
import time
from typing import Optional, List, Deque, Dict, Any
from collections import deque
from dataclasses import dataclass

from voxstream.config.types import (
    BufferConfig, StreamConfig, AudioConstants,
    AudioBytes, ProcessingMode
)
from voxstream.exceptions import AudioError


class BufferPool:
    """Pre-allocated buffer pool for zero-copy operations"""
    
    def __init__(self, pool_size: int = 10, buffer_size: int = 48000):
        self.pool_size = pool_size
        self.buffer_size = buffer_size
        self.buffers = [bytearray(buffer_size) for _ in range(pool_size)]
        self.available = list(range(pool_size))
        self.in_use = set()
        self.lock = threading.Lock()
        
    def acquire(self) -> Optional[bytearray]:
        """Get a buffer from pool"""
        with self.lock:
            if not self.available:
                return None
            idx = self.available.pop()
            self.in_use.add(idx)
            return self.buffers[idx]
    
    def release(self, buffer: bytearray) -> None:
        """Return buffer to pool"""
        with self.lock:
            for idx, buf in enumerate(self.buffers):
                if buf is buffer:
                    if idx in self.in_use:
                        self.in_use.remove(idx)
                        self.available.append(idx)
                    break


class StreamBuffer:
    """
    Stream buffer for continuous audio processing.
    
    Manages large audio buffers for quality processing with
    automatic chunk management and overflow handling.
    """
    
    def __init__(
        self,
        config: BufferConfig = None,
        audio_config: StreamConfig = None,
        logger=None
    ):
        self.config = config or BufferConfig()
        self.audio_config = audio_config or StreamConfig()
        self.logger = logger
        
        # Main buffer
        self.buffer = bytearray(self.config.max_size_bytes)
        self.position = 0
        self.total_bytes = 0
        
        # Chunk queue for processing
        self.chunk_queue: Deque[AudioBytes] = deque(maxlen=self.config.chunk_queue_size)
        
        # Stats
        self.overflow_count = 0
        self.chunks_processed = 0
        self.bytes_consumed = 0
        
        # Thread safety
        self.lock = threading.Lock()
    
    def add_audio(self, audio: AudioBytes) -> bool:
        """Add audio to buffer. Returns True on success."""
        with self.lock:
            audio_len = len(audio)
            
            # Check for overflow
            if self.position + audio_len > self.config.max_size_bytes:
                if self.config.overflow_strategy == "circular":
                    # Wrap around
                    self.position = 0
                    self.overflow_count += 1
                elif self.config.overflow_strategy == "drop_oldest":
                    # Move data to make room
                    shift = audio_len
                    self.buffer[:-shift] = self.buffer[shift:]
                    self.position = max(0, self.position - shift)
                else:  # truncate
                    audio_len = self.config.max_size_bytes - self.position
                    audio = audio[:audio_len]
            
            # Copy audio to buffer
            self.buffer[self.position:self.position + audio_len] = audio
            self.position += audio_len
            self.total_bytes += audio_len
            return True
    
    def get_chunk(self, size: Optional[int] = None) -> Optional[AudioBytes]:
        """Get a chunk from buffer"""
        with self.lock:
            if self.position == 0:
                return None
            
            chunk_size = size or self.audio_config.chunk_size_bytes()
            chunk_size = min(chunk_size, self.position)
            
            # Extract chunk
            chunk = bytes(self.buffer[:chunk_size])
            
            # Shift remaining data
            self.buffer[:-chunk_size] = self.buffer[chunk_size:self.position]
            self.position -= chunk_size
            self.chunks_processed += 1
            self.bytes_consumed += chunk_size
            
            return chunk
    
    def clear(self) -> None:
        """Clear buffer"""
        with self.lock:
            self.position = 0
            self.overflow_count = 0
            self.chunks_processed = 0
    
    def get_available_bytes(self) -> int:
        """Get number of bytes available in buffer"""
        with self.lock:
            return self.position
    
    @property
    def total_bytes_added(self) -> int:
        """Total bytes added to buffer"""
        return self.total_bytes
    
    @property
    def total_bytes_consumed(self) -> int:
        """Total bytes consumed from buffer"""
        return self.bytes_consumed
    
    def get_stats(self) -> Dict[str, Any]:
        """Get buffer statistics"""
        with self.lock:
            return {
                "current_size": self.position,
                "total_bytes": self.total_bytes,
                "overflow_count": self.overflow_count,
                "chunks_processed": self.chunks_processed,
                "utilization": self.position / self.config.max_size_bytes
            }