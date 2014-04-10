Scribe
-------------------------------

Simple speech recognition for Python.  Run the script, say some things into your microphone, and then see what you said (or an approximation).

Powered by [pyaudio](http://people.csail.mit.edu/hubert/pyaudio/) and [Sphinx](http://cmusphinx.sourceforge.net/).

Installation
--------------------------------

### Sphinxbase

Download [sphinxbase](http://sourceforge.net/projects/cmusphinx/files/sphinxbase/0.8) and extract the files.

Now, run:
```
cd sphinxbase
./configure;make clean all;make install
cd python
python setup.py install
```

You may need to use sudo for make install or python setup.py install.

### Pocketsphinx

Download [pocketsphinx](http://sourceforge.net/projects/cmusphinx/files/pocketsphinx/0.8) and extract the files.

Now, run:
```
cd pocketsphinx
./configure;make clean all;make install
cd python
python setup.py install
```

### Packages (Linux only)

Now, run:

```
cd speech-recognizer
sudo xargs -a apt-packages.txt apt-get install
```

### Pyaudio

Now, download the right version of [pyaudio](http://people.csail.mit.edu/hubert/pyaudio/) and install it.

### Language files

If you want to speak english, you need to get the [english language model](http://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/US%20English%20Generic%20Language%20Model/) and the [english acoustic model](http://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/US%20English%20Generic%20Acoustic%20Model/).

You will need to put the acoustic model into `scribe/hmm`, and the language model into `scribe/lm`.

The filetree should look like this for english:

```
scribe
├── dict
│   └── cmu07a.dic
├── hmm
│   ├── feat.params
│   ├── feature_transform
│   ├── mdef
│   ├── means
│   ├── mixture_weights
│   ├── noisedict
│   ├── README
│   ├── transition_matrices
│   └── variances
├── lm
│   └── cmusphinx-5.0-en-us.lm.dmp
```

For other languages, [check here](http://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/), or see below on training your own model.  If you use different language models, acoustic models, or dictionaries, you will want to change these paths in `recognizer.py`:

```
HMDIR = os.path.join(BASE_PATH, "hmm")
LMDIR = os.path.join(BASE_PATH, "lm/cmusphinx-5.0-en-us.lm.dmp")
DICTD = os.path.join(BASE_PATH, "dict/cmu07a.dic")
```

Run
-------------------------------

To run, you just have to:

```
cd speech-recognizer
python recognizer.py
```

You should be able to talk for a few seconds, after which it will spend some time processing, and the show you what you said.

Configure
---------------------------------

There are some options that you can modify at the top of `recognizer.py`.  The easiest one to modify is `RECORD_SECONDS`.

More reading
----------------------------------

To find out more, read up on [sphinx](http://cmusphinx.sourceforge.net/wiki/).

You can train the language models to make them more accurate, use unsupported languages, or be more domain-specific.