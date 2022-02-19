import speech_recognition as sr
r = sr.Recognizer()
#pericoloso = sr.AudioFile('7601-291468-0006.wav')
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Sono in ascolto, parla pure!")
    audio = r.listen(source)
    print("Ok, sto elaborando il messaggio...")

try:
    testo = r.recognize_google(audio, language="it-IT")
    print(testo)
except Exception as e:
    print(e)