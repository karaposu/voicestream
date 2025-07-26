# VoxStream API Reference

Comprehensive documentation of all public methods and classes in VoxStream.

## Table of Contents

- [Core Classes](#core-classes)
  - [VoxStream](#voxstream-class)
  - [StreamProcessor](#streamprocessor-class)
- [Configuration Types](#configuration-types)
  - [StreamConfig](#streamconfig)
  - [VADConfig](#vadconfig)
  - [BufferConfig](#bufferconfig)
- [Voice Detection](#voice-detection)
  - [VADetector](#vadetector-class)
- [Exceptions](#exceptions)

---

## Core Classes

### VoxStream Class

The main streaming engine for real-time voice processing.

```python
from voxstream import VoxStream
```

#### Constructor

```python
VoxStream(
    mode: ProcessingMode = ProcessingMode.BALANCED,
    config: StreamConfig = None,
    buffer_config: BufferConfig = None,
    logger: Optional[logging.Logger] = None
)
```

**Parameters:**
- `mode`: Processing mode (REALTIME, QUALITY, or BALANCED)
- `config`: Stream configuration object
- `buffer_config`: Buffer pool configuration
- `logger`: Optional logger instance

**Example:**
```python
stream = VoxStream(mode=ProcessingMode.REALTIME)
```

#### Methods

##### process_audio

```python
process_audio(audio_bytes: bytes) -> bytes
```

Process audio data through the streaming pipeline.

**Parameters:**
- `audio_bytes`: Raw audio data (PCM16 format)

**Returns:**
- Processed audio bytes

**Example:**
```python
processed = stream.process_audio(raw_audio)
```

##### configure_vad

```python
configure_vad(vad_config: VADConfig) -> None
```

Configure Voice Activity Detection.

**Parameters:**
- `vad_config`: VAD configuration object

**Example:**
```python
vad_config = VADConfig(threshold=0.02)
stream.configure_vad(vad_config)
```

##### get_vad_state

```python
get_vad_state() -> Optional[str]
```

Get current VAD state.

**Returns:**
- One of: 'silence', 'speech_starting', 'speech', 'speech_ending', or None

##### get_metrics

```python
get_metrics() -> Dict[str, Any]
```

Get performance metrics.

**Returns:**
- Dictionary containing:
  - `total_chunks`: Total chunks processed
  - `total_bytes`: Total bytes processed
  - `avg_latency_ms`: Average processing latency
  - `min_latency_ms`: Minimum latency
  - `max_latency_ms`: Maximum latency
  - `error_count`: Number of errors
  - `buffer_pool_hit_rate`: Buffer pool efficiency

##### add_pre_processor

```python
add_pre_processor(processor: Callable[[bytes], bytes]) -> None
```

Add a pre-processing function to the pipeline.

**Parameters:**
- `processor`: Function that takes and returns audio bytes

**Example:**
```python
def denoise(audio: bytes) -> bytes:
    # Denoising logic
    return audio

stream.add_pre_processor(denoise)
```

##### add_post_processor

```python
add_post_processor(processor: Callable[[bytes], bytes]) -> None
```

Add a post-processing function to the pipeline.

##### enable_feature

```python
enable_feature(feature: str, enabled: bool = True) -> None
```

Enable or disable specific features.

**Parameters:**
- `feature`: Feature name ('vad', 'enhancement', 'noise_reduction')
- `enabled`: Whether to enable the feature

##### cleanup

```python
cleanup() -> None
```

Clean up resources and reset state.

---

### StreamProcessor Class

Low-level audio processing with optimized paths.

```python
from voxstream.core.processor import StreamProcessor
```

#### Constructor

```python
StreamProcessor(
    config: StreamConfig = None,
    mode: ProcessingMode = ProcessingMode.BALANCED,
    logger: Optional[logging.Logger] = None
)
```

#### Methods

##### process_realtime

```python
process_realtime(audio_bytes: bytes) -> bytes
```

Fast processing path for minimal latency.

**Returns:**
- Processed audio with minimal transformations

##### process_quality

```python
process_quality(
    audio_bytes: bytes,
    metadata: Optional[AudioMetadata] = None
) -> Tuple[bytes, Dict[str, Any]]
```

Quality processing path with full pipeline.

**Returns:**
- Tuple of (processed_audio, processing_metadata)

##### validate_audio

```python
validate_audio(
    audio_bytes: bytes,
    min_duration_ms: float = 10.0
) -> Tuple[bool, Optional[str]]
```

Validate audio data.

**Returns:**
- Tuple of (is_valid, error_message)

---

## Configuration Types

### StreamConfig

Main configuration for audio streaming.

```python
@dataclass
class StreamConfig:
    sample_rate: int = 24000      # Sample rate in Hz
    channels: int = 1             # Number of channels
    bit_depth: int = 16          # Bits per sample
    format: AudioFormat = AudioFormat.PCM16
    chunk_duration_ms: int = 100  # Chunk size in milliseconds
    min_chunk_ms: int = 10       # Minimum chunk size
    max_chunk_ms: int = 1000     # Maximum chunk size
    use_numpy: bool = True       # Use NumPy optimizations
    pre_allocate_buffers: bool = True
```

**Properties:**
- `frame_size`: Bytes per audio frame
- `bytes_per_second`: Audio data rate
- `chunk_size_bytes(duration_ms)`: Calculate chunk size in bytes

### VADConfig

Voice Activity Detection configuration.

```python
@dataclass
class VADConfig:
    type: VADType = VADType.ENERGY
    threshold: float = 0.02
    speech_start_ms: int = 100   # Time to confirm speech started
    speech_end_ms: int = 300     # Time to confirm speech ended
    prefix_padding_ms: int = 300 # Audio to include before speech
    min_speech_ms: int = 50      # Minimum speech duration
    sample_rate: int = 24000
    create_response: bool = True
```

### BufferConfig

Buffer management configuration.

```python
@dataclass
class BufferConfig:
    max_size_bytes: int = 1024 * 1024  # 1MB
    max_duration_ms: int = 5000        # 5 seconds
    chunk_queue_size: int = 100
    overflow_strategy: Literal["drop_oldest", "drop_newest", "error"] = "drop_oldest"
    pre_allocate: bool = True
    use_circular: bool = True
```

---

## Voice Detection

### VADetector Class

Fast voice activity detection optimized for real-time.

```python
from voxstream.voice.vad import VADetector
```

#### Constructor

```python
VADetector(
    config: VADConfig = None,
    audio_config: StreamConfig = None,
    logger: Optional[logging.Logger] = None
)
```

#### Methods

##### process_chunk

```python
process_chunk(audio_chunk: bytes) -> VoiceState
```

Process audio chunk and detect voice activity.

**Returns:**
- VoiceState enum value

##### get_state

```python
get_state() -> VoiceState
```

Get current VAD state.

##### get_prebuffer

```python
get_prebuffer() -> bytes
```

Get buffered audio from before speech started.

##### reset

```python
reset() -> None
```

Reset VAD state and clear buffers.

---

## Exceptions

### VoxStreamError

Base exception for all VoxStream errors.

```python
class VoxStreamError(Exception):
    """Base exception for VoxStream errors"""
```

### AudioError

Audio processing specific errors.

```python
class AudioError(VoxStreamError):
    """Raised when audio processing fails"""
```

### ConfigurationError

Configuration related errors.

```python
class ConfigurationError(VoxStreamError):
    """Raised when configuration is invalid"""
```

---

## Enums

### ProcessingMode

```python
class ProcessingMode(Enum):
    REALTIME = "realtime"  # Minimum latency
    QUALITY = "quality"    # Maximum quality
    BALANCED = "balanced"  # Adaptive mode
```

### VoiceState

```python
class VoiceState(Enum):
    SILENCE = "silence"
    SPEECH_STARTING = "speech_starting"
    SPEECH = "speech"
    SPEECH_ENDING = "speech_ending"
```

### AudioFormat

```python
class AudioFormat(Enum):
    PCM16 = "pcm16"
    G711_ULAW = "g711_ulaw"
    G711_ALAW = "g711_alaw"
```

---

## Utility Functions

### create_fast_lane_engine

```python
create_fast_lane_engine(
    sample_rate: int = 24000,
    chunk_duration_ms: int = 20,
    vad_config: Optional[VADConfig] = None
) -> VoxStream
```

Create an engine optimized for minimum latency.

### create_adaptive_engine

```python
create_adaptive_engine(
    sample_rate: int = 24000,
    latency_target_ms: float = 50.0
) -> VoxStream
```

Create an engine that adapts to system performance.

---

## Complete Example

```python
from voxstream import VoxStream, StreamConfig, VADConfig, ProcessingMode

# Configure stream
config = StreamConfig(
    sample_rate=16000,
    chunk_duration_ms=20
)

# Configure VAD
vad_config = VADConfig(
    threshold=0.03,
    speech_start_ms=150
)

# Create stream processor
stream = VoxStream(
    mode=ProcessingMode.REALTIME,
    config=config
)
stream.configure_vad(vad_config)

# Process audio
def process_audio_stream(audio_source):
    for chunk in audio_source:
        # Process chunk
        processed = stream.process_audio(chunk)
        
        # Check VAD state
        vad_state = stream.get_vad_state()
        if vad_state == 'speech_starting':
            print("Speech detected!")
        
        # Yield processed audio
        yield processed

# Get metrics
metrics = stream.get_metrics()
print(f"Processed {metrics['total_chunks']} chunks")
print(f"Average latency: {metrics['avg_latency_ms']}ms")

# Cleanup
stream.cleanup()
```