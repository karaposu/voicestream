# VoxStream

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/latency-<5ms-orange.svg" alt="Ultra Low Latency">
  <img src="https://img.shields.io/badge/status-production_ready-brightgreen.svg" alt="Production Ready">
</p>

<p align="center">
  <strong>Real-time voice streaming engine for AI-powered conversations</strong>
</p>

---

## 🎯 What is VoxStream?

VoxStream is a high-performance, real-time voice streaming engine designed specifically for AI voice applications. It handles the complex audio pipeline between users and AI services, providing ultra-low latency processing, voice activity detection, and seamless streaming capabilities.

### ✨ Key Features

- 🚀 **Ultra-low latency** (<5ms processing overhead)
- 🎙️ **Voice Activity Detection** (VAD) with speech boundary detection  
- 🌊 **Streaming-first design** for WebSocket/real-time applications
- 📦 **Smart buffering** for network jitter compensation
- 🔊 **Voice enhancement** - noise reduction, echo cancellation
- 🎯 **Provider agnostic** - works with any AI service
- 📊 **Real-time metrics** for monitoring quality
- 🧪 **Development tools** for local testing

### 🚫 What VoxStream is NOT

- ❌ NOT a Speech-to-Text (STT) engine
- ❌ NOT a Text-to-Speech (TTS) engine  
- ❌ NOT tied to any specific AI provider
- ❌ NOT a WebSocket server (but integrates perfectly)

## 🚀 Quick Start

### Installation

```bash
pip install voxstream
```

### Basic Usage

```python
from voxstream import VoxStream

# Initialize the stream
vox = VoxStream()

# Process audio from any source
audio_bytes = get_audio_from_user()  # Your audio source

# Stream processing
if vox.detect_voice(audio_bytes):
    processed = vox.process(audio_bytes)
    
    # Send to your AI service
    await ai_service.send(processed)
```

### Real-time Streaming

```python
from voxstream import VoxStream, StreamConfig

# Configure for ultra-low latency
vox = VoxStream(
    config=StreamConfig(
        sample_rate=24000,      # Standard for AI services
        chunk_duration_ms=20,   # 20ms chunks
        optimize_for="latency"  # Latency-first mode
    )
)

# Stream audio chunks
async for chunk in vox.stream(audio_source):
    # Each chunk is validated and optimized
    await websocket.send(chunk)
```

## 🏗️ Architecture

VoxStream is designed specifically for real-time voice streaming pipelines:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  User Voice │────▶│  VoxStream  │────▶│ AI Service  │
│   (Input)   │     │  (Process)  │     │  (STT/LLM)  │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │  Features   │
                    ├─────────────┤
                    │ • VAD       │
                    │ • Enhance   │
                    │ • Buffer    │
                    │ • Metrics   │
                    └─────────────┘
```

## 💡 Core Concepts

### Voice Activity Detection (VAD)

VoxStream includes sophisticated VAD optimized for conversation:

```python
from voxstream import VoxStream, VADConfig

vox = VoxStream()

# Configure VAD for conversation
vox.configure_vad(VADConfig(
    sensitivity=0.7,            # 0-1, higher = more sensitive
    speech_start_ms=100,        # Debounce speech start
    speech_end_ms=700,          # Natural pause detection
    pre_speech_buffer_ms=300    # Capture word beginnings
))

# Real-time voice detection
state = vox.detect_voice(audio_chunk)
# Returns: "silence", "speech_starting", "speech", "speech_ending"

# Get pre-speech buffer (never miss word beginnings)
if state == "speech_starting":
    pre_buffer = vox.get_pre_speech_buffer()
```

### Streaming Pipeline

Designed for WebSocket and real-time streaming:

```python
# Create streaming pipeline
vox = VoxStream()

# Process large audio into stream-ready chunks
async for chunk in vox.create_stream(large_audio_buffer):
    # Each chunk is perfectly sized for streaming
    await send_to_ai(chunk)

# Or use continuous streaming
stream = vox.continuous_stream()
await stream.connect(audio_source)
await stream.flow_to(ai_destination)
```

### Voice Enhancement

Optimize voice for AI processing:

```python
# Enable voice enhancements
vox = VoxStream()
vox.enhance_voice(
    noise_reduction=True,      # Remove background noise
    echo_cancellation=True,    # Remove acoustic echo
    gain_control=True,         # Normalize volume
    clarity_boost=True         # Enhance speech frequencies
)

# Process with all enhancements
clean_voice = vox.process(noisy_audio)
```

## 🔧 Advanced Usage

### WebSocket Integration

Perfect for real-time voice chat applications:

```python
from voxstream import VoxStream

class VoiceRelay:
    def __init__(self):
        self.vox = VoxStream(optimize_for="latency")
        
    async def handle_client_audio(self, websocket):
        async for audio_data in websocket:
            # Process through VoxStream
            processed = self.vox.process(audio_data)
            
            # Only forward speech
            if self.vox.is_speaking:
                await self.ai_websocket.send(processed)
            
            # Monitor quality
            if self.vox.metrics.latency_ms > 50:
                await self.optimize_connection()
```

### Multi-Provider Support

```python
# VoxStream works with any AI provider
class MultiProviderVoice:
    def __init__(self):
        self.vox = VoxStream()
    
    async def send_to_openai(self, audio):
        processed = self.vox.prepare_for_ai(audio, provider="openai")
        return await openai_client.audio.transcribe(processed)
    
    async def send_to_google(self, audio):
        processed = self.vox.prepare_for_ai(audio, provider="google")
        return await google_speech.recognize(processed)
    
    async def send_to_azure(self, audio):
        processed = self.vox.prepare_for_ai(audio, provider="azure")
        return await azure_speech.recognize(processed)
```

### Conversation Flow Control

```python
from voxstream import VoxStream, ConversationMode

vox = VoxStream()

# Configure for natural conversation
vox.set_mode(ConversationMode.NATURAL)

# Handle interruptions
vox.on('user_interruption', lambda: handle_interruption())

# Detect conversation cues
vox.on('long_pause', lambda: prompt_user())
vox.on('speech_overlap', lambda: handle_overlap())

# Conversation-aware streaming
async for event in vox.conversation_stream():
    if event.type == 'user_speaking':
        await pause_ai_response()
    elif event.type == 'user_finished':
        await resume_ai_response()
```

### Real-time Metrics

```python
# Monitor stream health
metrics = vox.get_metrics()

print(f"Latency: {metrics.latency_ms}ms")
print(f"Voice Quality: {metrics.voice_quality_score}")
print(f"Packet Loss: {metrics.packet_loss_percent}%")
print(f"Speaking Time: {metrics.speaking_duration_ms}ms")

# Set up alerts
vox.on_metric('latency_ms', lambda v: v > 100, alert_high_latency)
vox.on_metric('voice_quality', lambda v: v < 0.5, alert_poor_quality)
```

## 🧪 Development & Testing

### Local Testing Mode

```python
# Enable local microphone for testing
from voxstream import VoxStream, TestMode

vox = VoxStream(mode=TestMode.LOCAL_MIC)

# Capture from local microphone
async for audio in vox.capture_local():
    processed = vox.process(audio)
    print(f"VAD State: {vox.detect_voice(processed)}")
    print(f"Audio level: {vox.get_level(processed)}")
```

### Voice Simulation

```python
# Generate test audio
test_audio = vox.generate_test_audio(
    duration_ms=1000,
    pattern="speech"  # or "silence", "mixed"
)

# Test your pipeline
result = vox.process(test_audio)
assert vox.detect_voice(result) == "speech"
```

## 📊 Performance

### Benchmarks

| Operation | Latency | Throughput |
|-----------|---------|------------|
| Process 20ms chunk | <1ms | >1000 chunks/sec |
| VAD detection | <0.5ms | >2000 chunks/sec |
| Stream creation | <2ms | >500 streams/sec |
| Enhancement | <3ms | >300 chunks/sec |

### Optimization Modes

```python
# Ultra-low latency mode
vox = VoxStream(optimize_for="latency")  # <5ms total

# Balanced mode  
vox = VoxStream(optimize_for="balanced")  # <20ms with enhancement

# Quality mode
vox = VoxStream(optimize_for="quality")  # <50ms full processing
```

## 🔌 Integration Examples

### With OpenAI Realtime API

```python
vox = VoxStream()

# Prepare for OpenAI's expectations
processed = vox.prepare_for_ai(audio, provider="openai")
await openai_ws.send(processed)
```

### With Custom AI Services

```python
# Add custom preparation
vox.add_provider("myai", {
    "sample_rate": 16000,
    "format": "pcm16",
    "chunk_ms": 100
})

processed = vox.prepare_for_ai(audio, provider="myai")
```

### With React/Next.js Frontend

```javascript
// Frontend (React)
const recorder = new MediaRecorder(stream);
recorder.ondataavailable = (e) => {
    websocket.send(e.data);  // Send to backend
};

// Backend (Python)
vox = VoxStream()
async for audio in websocket:
    processed = vox.process(audio)
    await ai_service.send(processed)
```

## 📚 API Reference

### Core Classes

#### `VoxStream`
```python
vox = VoxStream(
    config: StreamConfig = None,
    optimize_for: str = "balanced"  # "latency", "balanced", "quality"
)

# Main methods
vox.process(audio: bytes) -> bytes
vox.detect_voice(audio: bytes) -> str
vox.stream(audio: bytes) -> AsyncIterator[bytes]
vox.enhance_voice(audio: bytes) -> bytes
vox.get_metrics() -> StreamMetrics
```

#### `StreamConfig`
```python
config = StreamConfig(
    sample_rate=24000,        # Hz
    channels=1,               # Mono
    chunk_duration_ms=20,     # Streaming chunk size
    format="pcm16"           # Audio format
)
```

#### `VADConfig`
```python
vad = VADConfig(
    sensitivity=0.7,          # 0-1
    speech_start_ms=100,
    speech_end_ms=700,
    pre_speech_buffer_ms=300
)
```

## 🛠️ Installation Options

```bash
# Basic installation
pip install voxstream

# With optimization extras
pip install voxstream[performance]

# Development version
pip install voxstream[dev]

# All features
pip install voxstream[all]
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Clone repository
git clone https://github.com/voxstream/voxstream
cd voxstream

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run benchmarks
python -m voxstream.benchmarks
```

## 📈 Roadmap

- [ ] Advanced echo cancellation algorithms
- [ ] Multi-language VAD optimization
- [ ] WebAssembly version for browser
- [ ] GPU acceleration for enhancement
- [ ] Spatial audio support

## 📄 License

VoxStream is MIT licensed. See [LICENSE](LICENSE) for details.

## 💬 Community

- 📧 Email: hello@voxstream.io
- 💬 Discord: [Join our server](https://discord.gg/voxstream)
- 🐦 Twitter: [@voxstream](https://twitter.com/voxstream)
- 📖 Docs: [voxstream.readthedocs.io](https://voxstream.readthedocs.io)

---

<p align="center">
  Built with 🎙️ for the future of voice AI
</p>