import pyttsx3
import asyncio
import io
import tempfile
import os
from typing import Optional

class TextToSpeech:
    def __init__(self, use_google_cloud: bool = False):
        """
        Initialize TTS engine
        Args:
            use_google_cloud: If True, use Google Cloud TTS (requires credentials),
                            otherwise use pyttsx3
        """
        self.use_google_cloud = use_google_cloud
        if not use_google_cloud:
            self.engine = pyttsx3.init()
            # Configure voice properties
            self.engine.setProperty('rate', 150)    # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
            
            # Get available voices and set a default one
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)  # Index 0 is usually default voice
        else:
            try:
                from google.cloud import texttospeech
                self.client = texttospeech.TextToSpeechClient()
            except ImportError:
                print("Google Cloud TTS not available. Falling back to pyttsx3.")
                self.use_google_cloud = False
                self.engine = pyttsx3.init()

    async def generate_speech(self, text: str) -> Optional[bytes]:
        """
        Generate speech from text
        Args:
            text: Text to convert to speech
        Returns:
            bytes: Audio data in WAV format
        """
        if not text:
            return None

        if self.use_google_cloud:
            return await self._generate_speech_google(text)
        else:
            return await self._generate_speech_pyttsx3(text)

    async def _generate_speech_pyttsx3(self, text: str) -> bytes:
        """Generate speech using pyttsx3"""
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_path = temp_file.name

        def _save_to_file():
            self.engine.save_to_file(text, temp_path)
            self.engine.runAndWait()

        # Run in thread pool since pyttsx3 is blocking
        await asyncio.get_event_loop().run_in_executor(None, _save_to_file)

        # Read the temporary file
        with open(temp_path, 'rb') as f:
            audio_data = f.read()

        # Clean up temporary file
        os.unlink(temp_path)

        return audio_data

    async def _generate_speech_google(self, text: str) -> bytes:
        """Generate speech using Google Cloud TTS"""
        from google.cloud import texttospeech

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        # Select the type of audio file
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        # Perform the text-to-speech request
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
        )

        return response.audio_content

    def set_voice(self, voice_id: str) -> bool:
        """
        Set the voice to use for speech synthesis
        Args:
            voice_id: ID of the voice to use
        Returns:
            bool: True if voice was set successfully
        """
        if not self.use_google_cloud:
            try:
                self.engine.setProperty('voice', voice_id)
                return True
            except:
                return False
        return False

    def set_rate(self, rate: int) -> bool:
        """
        Set the speech rate
        Args:
            rate: Speech rate (words per minute)
        Returns:
            bool: True if rate was set successfully
        """
        if not self.use_google_cloud:
            try:
                self.engine.setProperty('rate', rate)
                return True
            except:
                return False
        return False

    def set_volume(self, volume: float) -> bool:
        """
        Set the speech volume
        Args:
            volume: Volume level (0.0 to 1.0)
        Returns:
            bool: True if volume was set successfully
        """
        if not self.use_google_cloud:
            try:
                self.engine.setProperty('volume', volume)
                return True
            except:
                return False
        return False

    def get_available_voices(self) -> list:
        """
        Get list of available voices
        Returns:
            list: List of available voice IDs
        """
        if not self.use_google_cloud:
            return [voice.id for voice in self.engine.getProperty('voices')]
        return []

async def main():
    """Test the TTS functionality"""
    tts = TextToSpeech()
    
    # Test basic TTS
    print("Testing TTS...")
    audio_data = await tts.generate_speech("Hello, this is a test of the text to speech system.")
    
    if audio_data:
        # Save test audio to file
        with open("test_speech.wav", "wb") as f:
            f.write(audio_data)
        print("Test audio saved to 'test_speech.wav'")
    
    # Print available voices
    print("\nAvailable voices:")
    voices = tts.get_available_voices()
    for voice in voices:
        print(f"- {voice}")

if __name__ == "__main__":
    asyncio.run(main())
