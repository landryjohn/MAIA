import speech_recognition as sr
r = sr.Recognizer()
def listen():
	with sr.Microphone(device_index = 2) as source:
		r.adjust_for_ambient_noise(source)
		r.pause_threshold = 2
		print("Say Something");
		audio = r.listen(source)
		print("got it");
	text = r.recognize_google(audio, language = "fr-FR")
	print("You said : ", text)

def l2():
	with sr.AudioFile('out.wav') as source :
		r.adjust_for_ambiant_noise(source)
		audio = r.record(source)
		text = r.recognize_google(audio, language='fr-FR')
		print(text)
