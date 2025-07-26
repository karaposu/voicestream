# VoxStream

A lightweight, high-performance voice streaming engine for real-time AI applications.

## Features

- 🚀 **Ultra-low latency** - Optimized for real-time voice streaming (<10ms processing latency)
- 🎯 **Voice Activity Detection** - Built-in VAD with customizable thresholds
- 🔄 **Adaptive Processing** - Automatic quality adjustment based on system load
- 🎵 **Flexible Audio Support** - Multiple formats and sample rates
- 🧩 **Modular Design** - Easy to integrate and extend
- 📊 **Performance Monitoring** - Built-in metrics and benchmarking

## Installation

```bash
pip install voxstream
```

Or install from source:

```bash
git clone https://github.com/yourusername/voxstream.git
cd voxstream
pip install -e .
```

## Quick Start

```python
from voxstream import VoxStream, StreamConfig

# Create a voice stream processor
stream = VoxStream()

# Process audio in real-time
audio_chunk = b"..."  # Your audio data
processed = stream.process_audio(audio_chunk)

# With custom configuration
config = StreamConfig(
    sample_rate=16000,
    chunk_duration_ms=20
)
stream = VoxStream(config=config)
```

## Voice Activity Detection

```python
from voxstream import VoxStream, VADConfig

# Configure VAD
vad_config = VADConfig(
    threshold=0.02,
    speech_start_ms=100,
    speech_end_ms=300
)

# Create stream with VAD
stream = VoxStream()
stream.configure_vad(vad_config)

# Process with VAD
audio_chunk = b"..."
processed = stream.process_audio(audio_chunk)
vad_state = stream.get_vad_state()  # Returns: 'speech', 'silence', etc.
```

## Processing Modes

VoxStream offers three processing modes optimized for different use cases:

```python
from voxstream import VoxStream, ProcessingMode

# Real-time mode - Minimum latency
stream = VoxStream(mode=ProcessingMode.REALTIME)

# Quality mode - Maximum quality
stream = VoxStream(mode=ProcessingMode.QUALITY)

# Balanced mode - Adaptive performance
stream = VoxStream(mode=ProcessingMode.BALANCED)
```

## Advanced Usage

### Stream Processing

```python
from voxstream import VoxStream
import asyncio

stream = VoxStream()

# Async streaming
async def process_stream(audio_source):
    async for chunk in audio_source:
        processed = stream.process_audio(chunk)
        yield processed
```

### Performance Monitoring

```python
# Get performance metrics
metrics = stream.get_metrics()
print(f"Average latency: {metrics['avg_latency_ms']}ms")
print(f"Chunks processed: {metrics['total_chunks']}")
```

### Custom Processing Pipeline

```python
# Add pre/post processors
def noise_reduction(audio: bytes) -> bytes:
    # Your noise reduction logic
    return audio

stream.add_pre_processor(noise_reduction)
stream.add_post_processor(lambda x: x)  # Your post-processor
```

## Architecture

VoxStream is built with a modular architecture:

```
voxstream/
├── core/           # Core streaming engine
├── voice/          # Voice-specific features (VAD)
├── config/         # Configuration and types
├── io/             # Audio I/O utilities
└── interfaces/     # Abstract interfaces
```

## Requirements

- Python 3.7+
- NumPy >= 1.21.0
- SoundDevice >= 0.4.0 (for audio I/O)

## Documentation

- [API Reference](endpoints.md) - Detailed method documentation
- [Examples](examples/) - Usage examples
- [Benchmarks](benchmarks/) - Performance benchmarks

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

VoxStream was created to provide a simple, efficient solution for real-time voice streaming in AI applications.