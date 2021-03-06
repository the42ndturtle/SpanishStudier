import tdl, threading, random, json, os, sys, numpy.core._methods, numpy.lib.format, tkinter as tk, speech_recognition as sr, urllib.request, io
from tdl import flush
from tkinter import filedialog
root = tk.Tk()
root.withdraw()
conWidth = 80
conHeight = 50
con = tdl.init(conWidth, conHeight, title="Spanish Studier", fullscreen=False)
flush()
lower = 'abcdefghijklmnopqrstuvwxyz'
upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
r = sr.Recognizer()
vocab = {}
if getattr(sys, 'frozen', False):
    dir_ = os.path.dirname(sys.executable)
else:
    dir_ = os.path.dirname(os.path.realpath(__file__))

settingsFile = dir_ + '\\settings.ini'
settingsJson = {}
def load():
    global settingsJson
    with open(settingsFile) as json_file:
        settingsJson = json.load(json_file)

def center(row, text):
    con.draw_str(((conWidth/2)-(len(text)/2)), row, text)
def inCenter(row):
    var = ''
    while 1:
        k = tdl.event.key_wait()
        if k.key == 'ENTER':
            break
        elif k.key == 'BACKSPACE':
            var = var [:len(var)-1]
        elif k.shift and k.char:
            var += upper[lower.find(k.char)]
        else:
            var += k.char
        center(row, '                                                       ')
        center(row, var)
        flush()
    return var
def menu(row, options):
    optionsLen = 0
    for option in options:
        optionsLen += len(option)
    spacing = ((conWidth-optionsLen)/2)/2
    optionStr = ''
    answer = 0
    def makeStr():
        optionStr = ''
        for option in options:
            if options[answer] == option:
                optionStr += '>'
            else:
                optionStr += ' '
            optionStr += option
            if option != options[len(options)-1]:
                optionStr += (' '*int(spacing))
        return optionStr
    while 1:
        center(25, makeStr())
        flush()
        k = tdl.event.key_wait()
        if k.key == 'LEFT':
            answer -= 1
        elif k.key == 'RIGHT':
            answer += 1
        elif k.key == 'ENTER':
            return options[answer]
        answer %= len(options)

def main():
    if settingsJson['isSpanish']:
        questions = list(vocab)
    else:
        questions = list(vocab.values())
    if settingsJson['mix']:
        random.shuffle(questions)
    correct = 0
    for i in questions:
        con.clear()
        center(15, i)
        flush()
        def getAnswer():
            with sr.Microphone() as source:
                center(20, 'listening...')
                flush()
                audio = r.listen(source)
            return audio
        if not settingsJson['voice']:
            answer = inCenter(25)
        else:
            audio = getAnswer()
            try:
                answer = r.recognize_google(audio)
                center(25, answer)
            except sr.UnknownValueError:
                getAnswer()
        flush()
        if settingsJson['isSpanish']:
            if answer == vocab[i]:
                center(30, 'correct')
                center(20, '                 ')
                correct += 1
            else:
                center(30, 'the correct answer was "' + vocab[i] + '"')
        else:
            if answer == list(vocab.keys())[list(vocab.values()).index(i)]:
                center(30, 'correct')
                center(20, '                 ')
                correct += 1
            else:
                center(30, 'the correct answer was "' + list(vocab.keys())[list(vocab.values()).index(i)] + '"')
        flush()
        while 1:
            k = tdl.event.key_wait()
            if k.key == "ENTER" or k.char == ' ':
                break
                con.clear()
    con.clear()
    center(10, 'you got ' + str(correct) + ' correct out of ' + str(len(vocab)))
    center(15, 'practice again?')
    again = menu(25, ['yes', 'no'])
    flush()
    if again == 'yes':
        main()
    else:
        start()
def settings():
    con.clear()
    center(20, 'Spanish or English first?')
    isSpanish = menu(25, ['Spanish', 'English'])
    if isSpanish == 'Spanish':
        settingsJson['isSpanish'] = True
    else:
        settingsJson['isSpanish'] = False
    con.clear()
    center(20, 'Enable voice control?')
    voice = menu(25, ['yes', 'no'])
    if voice == 'yes':
        settingsJson['voice'] = True
    else:
        settingsJson['voice'] = False
    con.clear()
    center(20, 'Randomize vocab?')
    mix = menu(25, ['yes', 'no'])
    if mix == "yes":
        settingsJson['mix'] = True
    else:
        settingsJson['mix'] = False

    # Save to file
    with open(settingsFile, 'w') as out:
        json.dump(settingsJson, out)
    start()
def workshop():
    con.clear()
    center(5, 'Enter a vocab file name')
    flush()
    fileToGet = inCenter(25)
    try:
        with urllib.request.urlopen("http://dhess.com/s/workshop/index.php?type=call&file="+fileToGet) as url:
            data = json.loads(url.read().decode())
            with io.FileIO('VocabLists/' + fileToGet + '.vocab', 'w') as fileToSave:
                fileToSave.write(str(data).replace("'", '"').encode())

            start()
    except urllib.error.URLError:
        con.clear()
        center(15, 'Cannot connect to the internet')
        flush()
        k = tdl.event.key_wait()
        start()
def start():
    global vocab
    con.clear()
    load()
    center(15, "press ctrl+o to choose a voacb file")
    center(20, "press ctrl+s to change settings")
    center(25, 'press ctrl+v to open the vocab manager')
    center(30, "press ESC to close")
    flush()
    while 1:
        k = tdl.event.key_wait()
        if k.keychar == 'o' and k.control:
            file = filedialog.askopenfilename(initialdir = os.path.realpath(dir_)+'/VocabLists',
             title = "Select vocab", filetypes = (("vocab files", '*.vocab'), ('json files', '*.json'), ('all files', '*.*')))
            if file == '':
                start()
            with open(file) as json_file:
                vocab = json.load(json_file)
            main()
        elif k.keychar == 's' and k.control:
            settings()
        elif k.keychar == 'v' and k.control:
            workshop()
        elif k.key == 'ESCAPE':
            os._exit(1)
def isDead():
    threading.Timer(.01, isDead).start()
    if tdl.event.is_window_closed():
        os._exit(1)
def isFull():
    threading.Timer(.01, isFull).start()
    k = tdl.event.key_wait()
    if k.key == "ESCAPE":
        tdl.set_fullscreen(not tdl.get_fullscreen())
isDead()
start()
