import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone(device_index=2) as source :
	r.adjust_for_ambient_noise(source)
	print("Listenning ...")
	audio = r.listen(source)

	with open('outs.wav', 'wb') as f :
		f.write(audio.get_wav_data())
	print("ok!")

