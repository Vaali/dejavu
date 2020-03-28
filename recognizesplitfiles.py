from __future__ import absolute_import
from __future__ import print_function
import os
import logging
import warnings
import time
import shutil
import glob
from itertools import repeat
import concurrent.futures

warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
from subprocess import Popen, PIPE, STDOUT

def get_filename_without_extension(filename):
    filenamewithextension = os.path.basename(filename)
    return os.path.splitext(filenamewithextension)[0]

def getsongmatch(args):
    filename,djv = args
    song = djv.recognize( FileRecognizer, filename )
    return song

if __name__ == '__main__':
    
    dburl = os.getenv('DATABASE_URL', 'sqlite:///dejavu_one.db')
    if(not os.path.exists('soxoutput')):
        os.mkdir('soxoutput',0o755)
    strpath = "mp3/Brad-Sucks--Total-Breakdown.mp3"
    t = time.time()

    djv = Dejavu(dburl=dburl)
    t1 = time.time() - t
    
    #djv.fingerprint_directory("onechannel", [".mp3"])
    return_pool = []
    #song = djv.recognize( FileRecognizer, fileslist[0] )
    #with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #        return_pool = executor.map(getsongmatch, zip(fileslist,repeat(djv)))

    #fileslist = splitfile(strpath)
    #fileslist = glob.glob("chunk*.mp3")
    #print(fileslist)
    #for filename in fileslist:
    #    print( djv.recognize( FileRecognizer, filename ) )
    '''
    t2 = time.time() - t
    '''
    match_list =  djv.recognize( FileRecognizer, strpath )
    
    for match in match_list:
        print(match)
    '''
    print(t1)
    print(t2)
    
    #print(song)
    '''
