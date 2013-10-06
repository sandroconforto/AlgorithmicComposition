# Copyright (c) 2013, Sandro Conforto
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


##########################################
# The Embrace of The Python              #
# Project B - Survey of Music Technology #
# Sandro Conforto                        #

"""
    DISCLAIMER: Given I had no previous Python experience something could surely be better coded.
"""

from earsketch import *
from random import *
from math import *

# The song will be in C major tonality: so from now on every note or chord will refer to C major

# init Reaper project
init()

# setting tempo
setTempo(120)

# our time base will a sixteenth
time_base = 1.0/16.0


# clips containing our sounds (the clips contain a scale and the apporopriate portion will be selected)
notes = PIANO_NOTES_C_MAJOR_SCALE
chords = PIANO_CHORDS_C_MAJOR
bass = BASS_NOTES_C_MAJOR_SCALE
drumClips = [OS_KICK01, OS_LOWTOM02, OS_CLAP01]

# track definition
solo_track = 1
melody_track_2 = 2
melody_track = 3
chords_track = 4
bass_track = 5
drum_tracks = [6,7,8]


# global variable used by function to track and update current song position
global_current_location = 1.0

# actual song beginning
song_start = 1.0

# symbolic constants for note names
C1='C1';D1='D1';E1='E1';F1='F1';G1='G1';A1='A1';B1='B1'; C2='C2';D2='D2';E2='E2';F2='F2';G2='G2';A2='A2';B2='B2';C3='C3'

# list of note symbolic names
note_names = [C1,D1,E1,F1,G1,A1,B1,C2,D2,E2,F2,G2,A2,B2,C3]

# list of corresponding index position in the sound clip
note_indexes =  range(0,15)

# dictionary to access to notes through symbolic notation (note dictionary)
nd = dict(zip(note_names, note_indexes))

# constants used by makeNote function to retrieve notes at index positions into clip
total_notes_length_in_measures = 15.00
single_note_length_in_time_base = 16.0
note_length_in_time_base = total_notes_length_in_measures / len(note_names) / time_base
total_note_duration_in_clip = note_length_in_time_base * time_base


# this is a list of lists: each contains the notes that will be used to make the melody over the corresponding chord 
allowed_notes_list = [ [C1,E1,G1,C2,E2,G2,C3], [D1,F1,A1,C2,D2,F2,A2,C3], [D1,E1,G1,B1,D2,E2,G2,B2], [C1,D1,F1,A1,C2,D2,F2,A2,C3],
                       [D1,F1,G1,B1,D2,F2,G2,B2], [C1,E1,G1,A1,C2,E2,G2,A2,C3], [C1,D1,F1,A1,B1,C2,D2,F2,A2,B2,C2] ]

allowed_notes_dict = dict(zip(note_names[0:7], allowed_notes_list))


def makeClipSection(clip, track, note_name, note_duration_in_time_base, update_location = True):
    """
    function to extract a desired section from a clip and put it into a track

    parameters:
        track (Integer): the track we will put the section into
        note_name (String): the name of the note we will put into track
        note_duration_in_time_base (Float): duration in sixteenth
        update_location (Boolean): determines if global_current_location will be updated after note insertion    
    """

    println('----- makeClipSection ----')
        
    # we want to have a side effect on global_current_location
    global global_current_location
    
    #println('note_name ' + note_name)
    note_index = nd[note_name]
    
    note_duration = ( note_duration_in_time_base / single_note_length_in_time_base)
    
    note_start_position =  1.0 + note_index  * total_note_duration_in_clip
    note_stop_position = ((note_start_position + (total_note_duration_in_clip * note_duration)) )

    insertMediaSection(clip, track, global_current_location, note_start_position, note_stop_position)
    
    tmp = global_current_location
    if(update_location):
        global_current_location += note_duration_in_time_base * time_base
    println('----- makeClipSection end ----')



def makeChord(track, chord_name, note_duration_in_time_base, update_location = True):
    """
    function to create each chord at track, with name and duration, if update_location is True we shift on global_current_location

    parameters:
        track  (Integer): the track we will put notes into
        note_name (String): the name of the chord we will put into track
        duration (Float): duration in sixteenth
        update_location (Boolean): determines if global_current_location will be updated after note insertion
    """
    if chord_name is None:
        if update_location:
            makePause(note_duration_in_time_base)
        return
    makeClipSection(chords, track, chord_name, note_duration_in_time_base, update_location)

def makeNote(track, note_name, note_duration_in_time_base, update_location = True):
    """
    function to create each note at track, with name and duration , if update_location is True we shift on global_current_location
    
    parameters:
        track  (Integer): the track we will put notes into
        note_name (String): the name of the note we will put into track
        duration  (Float): duration in sixteenth
        update_location (Boolean): determines if global_current_location will be updated after note insertion
    """    
    if note_name is None:
        if update_location:
            makePause(note_duration_in_time_base)
        return
    makeClipSection(notes, track,note_name, note_duration_in_time_base, update_location)

def makeBassNote(track, note_name, note_duration_in_time_base, update_location = True):
    """
    function to create each bass at track, with name and duration, if update_location is True we shift on global_current_location
    
    parameters:
        track (Integer): the track we will put notes into
        note_name (String): the name of the note we will put into track
        duration (Float): duration in sixteenth
        update_location (Boolean): determines if global_current_location will be updated after note insertion
    """
    if note_name is None:
        if update_location:
            makePause(note_duration_in_time_base)
        return
    makeClipSection(bass, track,note_name, note_duration_in_time_base, update_location)

def makeSoloOverChord(track, chord, note_duration_in_time_base, note_number):
    """
    function to create an arpeggio, using allowed notes over passed chord 
    
    parameters:
        track  (Integer): the track we will put notes into
        chord (String): the chord to take from allowed notes from allowed_notes array
        note_duration_in_time_base (Float): total solo duration in sixteenth
        note_number (Integer): the number of notes used to make the solo
    """
    if chord is None:
        makePause(note_duration_in_time_base)
    else:
        println('----- makeSoloOverChord ---- ' + chord)
        allowed_notes = allowed_notes_dict[chord]
        
        note_index = note_names.index(chord)
        interval = 4
        makeNote(track, note_names[(note_index+interval)%len(note_names)], float(note_duration_in_time_base)/float(note_number))
        makeNote(track, note_names[(note_index+interval)%len(note_names)], float(note_duration_in_time_base)/float(note_number))
        tmp = note_index+interval
        for i in range(0,note_number-2):
           random_n1 = randint(0,len(allowed_notes)-1)
           while(tmp == random_n1 or (math.fabs(random_n1 - tmp) > 4)):
             random_n1 = randint(0,len(allowed_notes)-1)
           tmp = random_n1
           println(allowed_notes[random_n1])
           makeNote(track, allowed_notes[random_n1], float(note_duration_in_time_base)/float(note_number))
    println('----- makeSoloOverChord end ----')

def makeMelodyOnTrack(track, note_sequence, note_duration_in_time_base, update_location):
    """
    function to insert a series of notes into a track: the notes are defined by note_sequence list
    
    parameters:
        track  (Integer): the track we will put the section into
        note_sequence (List of Strings): the list containing the sequence of notes we will put into track
        note_duration_in_time_base (Float): duration in sixteenth
        update_location (Boolean): determines if global_current_location will be updated after note insertion    
    """
    global global_current_location
    tmp = global_current_location
    for i in range(0,len(note_sequence)):
           makeNote(track, note_sequence[i], float(note_duration_in_time_base)/len(note_sequence))
    if update_location:
        return
    global_current_location = tmp
    return

def makeMelody(note_sequence,duration,update_location):
    """ auxiliary function to avoid writing track name form melody 1    """
    makeMelodyOnTrack(melody_track,note_sequence,duration,update_location)

def makeMelody2(note_sequence,duration,update_location):
    """ auxiliary function to avoid writing track name form melody 2 """
    makeMelodyOnTrack(melody_track_2,note_sequence,duration,update_location)

def makeChordSection(chord,bass_note,solo_chord,duration,solo_density):
    """ auxiliary function to make a section of a bass note, a chord, and a solo based on solo_chord """
    makeBassNote(bass_track, bass_note, duration,False)
    makeChord(chords_track, chord, duration,False)
    makeSoloOverChord(solo_track,solo_chord,duration,solo_density)

def makePause(pause_duration_in_time_base):
    """
    function to increment global_current_location
    
    parameters:
        pause_duration_in_time_base (Float): represents how many time reference global_current_location will be incremented
    """
    println('----- makePause ----')
    global global_current_location
    
    tmp = global_current_location
    global_current_location = global_current_location + (pause_duration_in_time_base * time_base)
    println('----- makePause end ----')

def generateDrumsFromPatterns(audio, tracks, beatStrings, start, stop):
    """
    function to generate a drum section from start to stop measure using the give beatString

    paramters:
        audio (List of Strings): the list of audio files used to make the drum section
        traks (List of Strings): the tracks on which the clips will be put into
        start (Integer): the start measure
        stop (Integer): the stop measure
    """
    numMeasures = stop-start
    
    for i in range(0,len(beatStrings)):
        makeBeat(audio[i], tracks[i], start, beatStrings[i] * numMeasures)

def generateRandomicDrums(audio, tracks, probabilityDistributions, start, stop, density):
    """
    function to generate a drum section from start to stop measure based on probabilities defined in probabilities list
    
    parameters:
       audio (List of Strings): the list of audio files used to make the drum section
        traks (List of Strings): the tracks on which the clips will be put into
        start (Integer): the start measure
        stop (Integer): the stop measure
        density (Float): the higher this value the more a beat is generated in the current position
    """
    numMeasures = stop-start

    # create beat strings
    kickBeatString = generateBeatString(probabilityDistributions[0], density)
    lowtomBeatString = generateBeatString(probabilityDistributions[1], density)
    snareBeatString = generateBeatString(probabilityDistributions[2], density)
    
    println('start ' + str(start))
    println('kickBeatString ' + kickBeatString)
    println('lowtomBeatString ' + lowtomBeatString)
    println('snareBeatString ' + snareBeatString)

    # make the beats numMeasures long and put on tracks
    makeBeat(audio[0], tracks[0], start, kickBeatString * numMeasures)
    makeBeat(audio[1], tracks[1], start, lowtomBeatString * numMeasures)
    makeBeat(audio[2], tracks[2], start, snareBeatString * numMeasures)

def generateBeatString(probabilityDistr, density):
    """
    function to generate a beat string pattern usable by makeBeat

    parameters:
        probabilityDistr (List of Floats): probability distribution
        density (Float): the higher this value the more a beat is generated in the current position
    """
    #Construct a beat string from drumAudio list based on designated beat probabilities and a given density

    # start with empty beats list since strings are immutable, later joined to string 
    beatString = ""

    # Add "0" or "-" cumulatively based on given probabilities of beat events until a measure has been created
    for i in range(0, 16):
        if random() < probabilityDistr[i] * density:
            beatString += "0"
        else:
            beatString += "-"

    return beatString # return passes the beatString back so we can use it after the function finishes

# setting track volumes


setEffect(MASTER_TRACK, VOLUME, GAIN, -3)

setEffect(solo_track, VOLUME, GAIN, -0.5)
setEffect(melody_track_2, VOLUME, GAIN, -0.5)
setEffect(melody_track, VOLUME, GAIN, -0.5)
setEffect(chords_track, VOLUME, GAIN, -1.5)
setEffect(bass_track, VOLUME, GAIN, -2)
setEffect(drum_tracks[0], VOLUME, GAIN, -6)
setEffect(drum_tracks[1], VOLUME, GAIN, -7)
setEffect(drum_tracks[2], VOLUME, GAIN, -7)

### and now... the music: The Embrace of the Python

def makeChordTheme():
    # I V IV VI I V IV I - bass and chord progression
    makeChordSection(C1,C2,None,16.0,4)
    makeChordSection(G1,B1,None,16.0,4)
    makeChordSection(F1,D2,None,16.0,4)
    makeChordSection(A1,E2,None,16.0,4)
    makeChordSection(C2,C2,None,16.0,4)
    makeChordSection(G1,G1,None,16.0,4)
    makeChordSection(F1,A1,None,16.0,4)
    makeChordSection(C1,E1,None,16.0,4)

def makeMelodyTheme():
    # I V IV VI I V IV I - with theme melody
    makeMelody([E2,D2,C2,B1], 16.0,False)
    makeMelody2([G2,F2,E2,D2], 16.0,False)
    makeChordSection(C1,C2,None,16.0,4)

    makeMelody([G1,A1,B1,G1], 16.0,False)
    makeMelody2([B1,C2,D2,B1], 16.0,False)
    makeChordSection(G1,B1,None,16.0,4)

    makeMelody([A1,B1,C2,G1], 16.0,False)
    makeMelody2([C2,D2,E2,B1], 16.0,False)
    makeChordSection(F1,D2,None,16.0,4)

    makeMelody([A1,B1,C2,A1], 16.0,False)
    makeMelody2([C2,D2,E2,C2], 16.0,False)
    makeChordSection(A1,E2,None,16.0,4)

    makeMelody([E2,D2,C2,B1], 16.0,False)
    makeMelody2([G2,F2,E2,D2], 16.0,False)
    makeChordSection(C1,C2,None,16.0,4)

    makeMelody([G1,A1,B1,G1], 16.0,False)
    makeMelody2([B2,C2,D2,B1], 16.0,False)
    makeChordSection(G1,G1,None,16.0,4)

    makeMelody([A1,B1,C2,D2], 16.0,False)
    makeMelody2([C2,D2,E2,F2], 16.0,False)
    makeChordSection(F1,F1,None,16.0,4)

def makeSolo():
    #  IV I V VI IV II V VI VII(V7) I - chord progression with solo
    part_duration = 16.0
    part_notes_number = 8

    makeChordSection(A1,E1,A1,part_duration,part_notes_number)
    makeChordSection(F1,F1,F1,part_duration,part_notes_number)
    makeChordSection(C1,C1,C1,part_duration,part_notes_number)
    makeChordSection(G1,D1,G1,part_duration,part_notes_number)
    makeChordSection(A1,E1,A1,part_duration,part_notes_number)
    makeChordSection(F1,F1,F1,part_duration,part_notes_number)
    makeChordSection(D1,G1,G1,part_duration,part_notes_number)
    makeChordSection(G1,E1,A1,part_duration,part_notes_number)
    makeChordSection(A1,F1,F1,part_duration,part_notes_number)
    makeChordSection(B1,G1,B1,part_duration,part_notes_number)

def makeEnding():
    makeMelody([C2], 16.0,False)
    makeMelody2([C2], 16.0,False)
    makeChord(chords_track, C1, 16.0,False)
    makeBassNote(bass_track, C1, 16.0,False)

def makeDrums():
    # defining the beat strings

    mainBeatStrings =   ["0-------------0-",
                         "---------0-0-0--",
                         "--------0-------"]

    fillBeatStrings =   ["0--------------0",
                         "----------------",
                         "0-----0---0-0-00"]

    endingBeatStrings = ["0---------------",
                         "----------------",
                         "0---------------"]

    # These respresent the probability of the existence of each drum sound in
    # the style of drumming desired. Each list represents a measure (i.e. 16 16th notes)
    kickProbabilities = [0.95, 0.2, 0.4, 0.2, 0.8, 0.2, 0.5, 0.2, 0.85, 0.2, 0.5, 0.2, 0.8, 0.2, 0.5, 0.2]
    lowtomProbabilities = [0.9, 0.8, 0.6, 0.6, 0.9, 0.8, 0.6, 0.4, 0.9, 0.9, 0.6, 0.8, 0.5, 0.6, 0.2, 0.8]
    snareProbabilities = [0.1, 0.1, 0.6, 0.1, 0.4, 0.1, 0.6, 0.1, 0.3, 0.1, 0.6, 0.1, 0.3, 0.1, 0.6, 0.1]
    probabilityDistributions = [kickProbabilities, lowtomProbabilities,snareProbabilities]

    # generating the drum beats
    generateDrumsFromPatterns(drumClips, drum_tracks, mainBeatStrings, 1, 9)   
    generateDrumsFromPatterns(drumClips, drum_tracks, fillBeatStrings, 9, 10)  
    generateDrumsFromPatterns(drumClips, drum_tracks, mainBeatStrings, 10, 16) 
    generateDrumsFromPatterns(drumClips, drum_tracks, fillBeatStrings, 16, 17)
    generateRandomicDrums(drumClips, drum_tracks, probabilityDistributions, 17, 26, 0.4)
    generateDrumsFromPatterns(drumClips, drum_tracks, fillBeatStrings, 26, 27)
    generateDrumsFromPatterns(drumClips, drum_tracks, mainBeatStrings, 27, 32)  
    generateDrumsFromPatterns(drumClips, drum_tracks, fillBeatStrings, 33, 34)
    generateDrumsFromPatterns(drumClips, drum_tracks, endingBeatStrings, 34, 35)



makePause( song_start * 16.0)

makeChordTheme()
makeMelodyTheme()
makeSolo()
makeMelodyTheme()
makeEnding()
makeDrums()

finish()