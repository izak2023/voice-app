import speech_recognition as sr

def get_recognizer(api_name):
    """
    Returns a recognizer object based on the selected API.
    """
    recognizer = sr.Recognizer()
    if api_name == 'google':
        return recognizer
    elif api_name == 'sphinx':
        return recognizer
    else:
        raise ValueError(f"Unsupported API: {api_name}")

def transcribe_speech(api_name, audio_file_path, language):
    recognizer = get_recognizer(api_name)
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
        if api_name == 'google':
            text = recognizer.recognize_google(audio_data, language=language)
        elif api_name == 'sphinx':
            text = recognizer.recognize_sphinx(audio_data)
        else:
            raise ValueError(f"Unsupported API: {api_name}")
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from the API; {e}"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def save_transcription(text, file_path):
    """
    Saves the transcribed text to a specified file.
    """
    with open(file_path, 'w') as file:
        file.write(text)

def main():
    api_choice = input("Choose API (google/sphinx): ").strip().lower()
    audio_file = "path/to/audio/file.wav"
    language = input("Enter the language code (e.g., 'en-US' for English): ").strip()
    output_file = input("Enter the file path to save the transcription: ").strip()

    result = transcribe_speech(api_choice, audio_file, language)
    print(result)
    save_transcription(result, output_file)
    print(f"Transcription saved to {output_file}")

# Simulate Pause and Resume:
def process_audio_in_chunks(api_name, audio_file_path, language, chunk_duration=30):
    recognizer = get_recognizer(api_name)
    audio_chunks = []

    try:
        with sr.AudioFile(audio_file_path) as source:
            for i, chunk in enumerate(source.stream(chunk_duration)):
                audio_data = recognizer.record(chunk)
                audio_chunks.append(audio_data)

        full_text = ""
        for chunk in audio_chunks:
            if api_name == 'google':
                full_text += recognizer.recognize_google(chunk, language=language) + " "
            elif api_name == 'sphinx':
                full_text += recognizer.recognize_sphinx(chunk) + " "
            else:
                raise ValueError(f"Unsupported API: {api_name}")

        return full_text.strip()

    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from the API; {e}"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Example usage:
if __name__ == "__main__":
    main()
    # For chunk processing:
    # api_choice = 'google'
    # audio_file = "path/to/audio/file.wav"
    # language = 'en-US'
    # print(process_audio_in_chunks(api_choice, audio_file, language))
