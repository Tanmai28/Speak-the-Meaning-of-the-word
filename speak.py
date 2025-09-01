import pyttsx3
import requests
import json


class Speaking:

    def speak(self, audio):
        try:
            # Having the initial constructor of pyttsx3 
            # and having the sapi5 in it as a parameter
            engine = pyttsx3.init('sapi5')
            
            # Calling the getter and setter of pyttsx3
            voices = engine.getProperty('voices')
            
            # Method for the speaking of the assistant
            if voices:
                engine.setProperty('voice', voices[0].id)
            engine.say(audio)
            engine.runAndWait()
        except Exception as e:
            print(f"Text-to-speech error: {e}")
            print(f"[TTS would say: {audio}]")


class SpeakingMeaning:
    def get_meaning_reliable(self, word):
        """Reliable method using Free Dictionary API"""
        try:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            print(f"Fetching from: {url}")
            response = requests.get(url, timeout=10)
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    meanings = {}
                    for entry in data:
                        for meaning in entry.get('meanings', []):
                            part_of_speech = meaning.get('partOfSpeech', 'unknown')
                            definitions = [defn.get('definition', '') for defn in meaning.get('definitions', [])]
                            if definitions:  # Only add if we have definitions
                                meanings[part_of_speech] = definitions
                    return meanings
            else:
                print(f"API returned status code: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None
    
    def Dictionary(self):
        speak = Speaking()
        speak.speak("Welcome to the dictionary! Which word do you want to find the meaning of?")
        
        while True:
            # Taking the string input
            query = str(input("\nEnter the word (or 'quit' to exit): "))
            query = query.lower().strip()
            
            # Check for exit command
            if query in ['quit', 'exit', 'q']:
                speak.speak("Goodbye! Have a great day!")
                print("Goodbye!")
                break
            
            # Input validation
            if not query or not query.replace(' ', '').isalpha():
                speak.speak("Please enter a valid word with only letters")
                print("Please enter a valid word with only letters")
                continue
            
            print(f"Looking up word: '{query}'")
            
            # Use the reliable API directly
            word = self.get_meaning_reliable(query)
            
            if not word or len(word) == 0:
                speak.speak(f"Sorry, no meaning found for the word: {query}")
                print("No meaning found. This could be due to:")
                print("1. Network connectivity issues")
                print("2. The word doesn't exist in the dictionary")
                print("3. Dictionary services are temporarily unavailable")
                continue
            
            speak.speak(f"Found meaning for the word: {query}")
            for part_of_speech, meanings in word.items():
                print(f"\n{part_of_speech.upper()}:")
                for i, meaning in enumerate(meanings, 1):
                    print(f"  {i}. {meaning}")
                speak.speak(f"As a {part_of_speech}, {query} means {meanings[0]}")


if __name__ == '__main__':
    speakingWithMeaning = SpeakingMeaning()
    speakingWithMeaning.Dictionary()
