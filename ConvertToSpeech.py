import langdetect
import pygame
from gtts import gTTS
from langdetect import detect
from pygame.locals import *
from pygame import mixer

languages = set()

def fileToString(TextFile):
    with open(TextFile, 'r', encoding='utf-8') as file1:
        lines = file1.readlines()
    return lines


def convertToAudio(txt, language, AudioFile):
    #convert the text into a gTTS object then Append it to the audio file
    tts = gTTS(text=txt, lang=language)
    with open(AudioFile, 'ab') as f:
        tts.write_to_fp(f)


def clearAudio(AudioFile):
    # to clear the content of the audio file if it previosly existed
    with open(AudioFile, 'wb') as f:
            f.truncate(0)


def detectLanguage(lines):
    # Identify the languages present in the text file
    for line in lines:
        print('line: '+ line)
        detected_lang = detect(line)
        print('lang: '+ detected_lang)
        languages.add(detected_lang)


def ConvertByLanguage(lines, AudioFile):
    # Convert text for each language to audio
    for language in languages:
        audio_text = ""
        for line in lines:
            if detect(line) == language:
                audio_text += line+' '

        convertToAudio(audio_text, language, AudioFile)


def play(soundfile):
    mixer.init()

    try:
        mixer.music.load(soundfile)
        mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
    except pygame.error:
        main('Error.txt')

    mixer.music.stop()
    mixer.quit()


def main(TextFile):
    AudioFile='text.mp3'
    clearAudio(AudioFile)
    s = fileToString(TextFile)
    detectLanguage(s)
    ConvertByLanguage(s,AudioFile)
    play(AudioFile)

#main('noDup.txt')


#mesk alhamaideh





























# made by MeskAlhamaideh