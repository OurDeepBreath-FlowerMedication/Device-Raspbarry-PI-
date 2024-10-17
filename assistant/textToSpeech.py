import gtts
from pydub import AudioSegment
from pydub.playback import play

def tts(script) :
    tts = gtts.gTTS(text=script, lang='ko')
    tts.save("/home/Dahee_youn/iot_project/data/speech.mp3")
    sound = AudioSegment.from_mp3("/home/Dahee_youn/iot_project/data/speech.mp3")
    play(sound)
    print(script)