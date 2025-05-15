from gtts import gTTS
import pygame
import io

def text_to_speech(text, language_code):
    """
    Convert text to speech and play it directly without creating audio files.
    
    Args:
        text (str): The text to be converted to speech
        language_code (str): Language code (e.g., 'ur' for Urdu, 'ar' for Arabic)
    """
    try:
        # Convert text to speech in memory
        tts = gTTS(text=text, lang=language_code)
        
        # Create an in-memory file-like object
        audio_data = io.BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)  # Rewind to start of stream
        
        # Initialize pygame mixer and play the audio
        pygame.mixer.init()
        pygame.mixer.music.load(audio_data)
        pygame.mixer.music.play()

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # Clean up
        pygame.mixer.quit()

    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Urdu example
    text_to_speech("یہ فلم ایک بہادر ہیرو کی کہانی بیان کرتی ہے۔", 'ur')
    
    # Arabic example
    text_to_speech("هذا فيلم عن بطل شجاع", 'ar')

    text_to_speech("After more than 30 years of service as one of the Navy's top aviators, Pete 'Maverick' Mitchell is where he belongs, pushing the envelope as a courageous test pilot and dodging the advancement in rank that would ground him. Training a detachment of graduates for a special assignment, Maverick must confront the ghosts of his past and his deepest fears, culminating in a mission that demands the ultimate sacrifice from those who choose to fly it.", 'en') 
