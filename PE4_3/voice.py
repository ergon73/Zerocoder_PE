# voice.py — поддерживает выбор голоса и генерацию аудио
# voice.py — supports voice selection and audio generation

from elevenlabs import save, Voice, VoiceSettings
from elevenlabs.client import ElevenLabs
import config

# Создание клиента ElevenLabs / Create ElevenLabs client
client = ElevenLabs(api_key=config.elevenlabs_api_key)

# Получение всех голосов / Get list of all voices
def get_all_voices():
    voices = client.voices.get_all()
    # Преобразуем в список словарей / Convert to list of dicts
    return [{'name': voice.name, 'id': voice.voice_id} for voice in voices.voices]

# Генерация аудио и возврат пути к MP3 / Generate audio and return path
def generate_audio(text: str, voice_id: str) -> str:
    audio = client.generate(
        text=text,
        voice=Voice(
            voice_id=voice_id,
            settings=VoiceSettings(
                stability=0.75,
                similarity_boost=0.5,
                style=0.0,
                use_speaker_boost=True
            )
        ),
        model="eleven_multilingual_v2"
    )
    filename = "audio.mp3"
    save(audio, filename)
    return filename
