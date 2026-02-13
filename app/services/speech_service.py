import os
from pathlib import Path
import io

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    import sounddevice as sd
    import soundfile as sf
    AUDIO_RECORDING_AVAILABLE = True
except ImportError:
    AUDIO_RECORDING_AVAILABLE = False


def record_audio(duration: int = 5, sample_rate: int = 16000) -> bytes:
    """
    Record audio from microphone for speech recognition.
    
    Args:
        duration: Duration of recording in seconds
        sample_rate: Sample rate in Hz
        
    Returns:
        Audio data in bytes
    """
    if not AUDIO_RECORDING_AVAILABLE:
        raise ImportError(
            "Audio recording requires 'sounddevice' and 'soundfile'. "
            "Install with: pip install sounddevice soundfile"
        )
    
    try:
        print(f"Recording for {duration} seconds...")
        audio_data = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='float32'
        )
        sd.wait()
        
        # Convert to bytes
        audio_buffer = io.BytesIO()
        sf.write(audio_buffer, audio_data, sample_rate, format='WAV')
        audio_buffer.seek(0)
        return audio_buffer.getvalue()
    except Exception as e:
        raise RuntimeError(f"Audio recording failed: {str(e)}")


def transcribe_audio(audio_path: str = None, audio_bytes: bytes = None, language: str = None) -> dict:
    """
    Transcribe audio to text using Whisper.
    
    Args:
        audio_path: Path to audio file
        audio_bytes: Audio data as bytes
        language: Language code (e.g., 'en' for English)
        
    Returns:
        Dictionary with transcription results
    """
    if not WHISPER_AVAILABLE:
        return {
            "success": False,
            "error": "Whisper is not installed. Install with: pip install openai-whisper"
        }
    
    try:
        # Load model
        model = whisper.load_model("base")
        
        # Handle audio input
        if audio_path and Path(audio_path).exists():
            result = model.transcribe(audio_path, language=language)
        elif audio_bytes:
            # Save bytes to temporary file
            temp_path = "/tmp/audio_temp.wav"
            with open(temp_path, "wb") as f:
                f.write(audio_bytes)
            result = model.transcribe(temp_path, language=language)
            os.remove(temp_path)
        else:
            return {
                "success": False,
                "error": "No audio input provided"
            }
        
        return {
            "success": True,
            "text": result.get("text", ""),
            "language": result.get("language", "unknown"),
            "duration": result.get("duration", 0)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def speech_to_text(duration: int = 5, language: str = None) -> dict:
    """
    Record audio and transcribe it to text in one call.
    
    Args:
        duration: Duration of recording in seconds
        language: Language code (e.g., 'en' for English)
        
    Returns:
        Dictionary with transcription results
    """
    try:
        audio_bytes = record_audio(duration)
        return transcribe_audio(audio_bytes=audio_bytes, language=language)
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
