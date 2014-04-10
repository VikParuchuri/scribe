import pyaudio
import wave
import sphinxbase
import os

# Import sometimes fails first time around because of a Cython issue.
try:
    import pocketsphinx
except ValueError:
    import pocketsphinx

# Paths
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
HMDIR = os.path.join(BASE_PATH, "hmm")
LMDIR = os.path.join(BASE_PATH, "lm/cmusphinx-5.0-en-us.lm.dmp")
DICTD = os.path.join(BASE_PATH, "dict/cmu07a.dic")

# Options
CHUNK = 128 # The size of each audio chunk coming from the input device.
FORMAT = pyaudio.paInt16 # Should not be changed, as this format is best for speech recognition.
RATE = 16000 # Speech recognition only works well with this rate.  Don't change unless your microphone demands it.
RECORD_SECONDS = 5 # Number of seconds to record, can be changed.
WAVE_OUTPUT_FILENAME = "output.wav" # Where to save the recording from the microphone.

def find_device(p, tags):
    """
    Find an audio device to read input from.
    """
    device_index = None
    for i in range(p.get_device_count()):
        devinfo = p.get_device_info_by_index(i)
        print("Device %d: %s" % (i, devinfo["name"]))

        for keyword in tags:
            if keyword in devinfo["name"].lower():
                print("Found an input: device %d - %s"%(i, devinfo["name"]))
                device_index = i
                return device_index

    if device_index is None:
        print("No preferred input found; using default input device.")

    return device_index

def save_audio(wav_file):
    """
    Stream audio from an input device and save it.
    """
    p = pyaudio.PyAudio()

    device = find_device(p, ["input", "mic", "audio"])
    device_info = p.get_device_info_by_index(device)
    channels = int(device_info['maxInputChannels'])

    stream = p.open(
        format=FORMAT,
        channels=channels,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=device
    )

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()

    p.terminate()

    wf = wave.open(wav_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def recognize(wav_file):
    """
    Run speech recognition on a given file.
    """
    speech_rec = pocketsphinx.Decoder(hmm=HMDIR, lm=LMDIR, dict=DICTD)
    wav_file = file(wav_file, 'rb')
    speech_rec.decode_raw(wav_file)
    result = speech_rec.get_hyp()
    return result

# Run the thing!
if __name__ == '__main__':
    save_audio(WAVE_OUTPUT_FILENAME)
    result = recognize(WAVE_OUTPUT_FILENAME)
    print "You just said: {0}".format(result[0])