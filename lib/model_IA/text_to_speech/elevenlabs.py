from elevenlabs import ElevenLabs, VoiceSettings

def text_to_speech():
    """
    text_to_speech with ElevenLabs with charlotte voice
    """
    client = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))

    client.voices.edit_settings(
    voice_id="XB0fDUnXU5powFXDhCwa",
    request=VoiceSettings(
        stability=0.3,
        similarity_boost=0.75,
        style=0,
    ),
)
    
    audio_generator = client.text_to_speech.convert(
    voice_id="XB0fDUnXU5powFXDhCwa",
    model_id="eleven_multilingual_v2",
    text="""
    Bonjour Google Pitch Day ! 
    Vous rêvez d'exercer la profession d'avocat ailleurs : pouvoir surfez même en semaine à Biarritz ; profitez du soleil de la Côte d'Azur ou alors du calme de la campagne ? 
    Vous souhaitez diversifiez vos pratiques mais ne savez pas celles qui seront porteuses ?
    Toutes ces questions auront une réponse, grâce à notre nouvel outil: Phoebe.
    """,
    )
    return audio_generator