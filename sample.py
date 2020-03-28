from __future__ import absolute_import
from __future__ import print_function
import os
import logging
import warnings
import time
warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer

def splitfile(strpath):
    try:
        #sox Brad-Sucks--Total-Breakdown.mp3 output.mp3 trim 0 4 : newfile : restart
        curr_folder_name = get_filename_without_extension(strpath)
        output_directory = 'soxoutput/'+curr_folder_name
        if(os.path.exists(output_directory)):
            shutil.rmtree(output_directory)
        os.mkdir(output_directory,0o755)
        output_filename = output_directory+ '/' + '0.mp3'
        command = "sox '{}' '{}' trim 0 {} : newfile : restart ".format( strpath, output_filename, 4 )
        print(command)
        p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True )
        output, errors = p.communicate()
        if errors:
            print(errors)
            return []
        filelist = glob.glob(output_directory+"/*.mp3")
        return filelist
    except Exception as ex:
        print(ex)
    return []



dburl = os.getenv('DATABASE_URL', 'sqlite:///dejavu_one.db')
djv = Dejavu(dburl=dburl)
t = time.time()
#djv.fingerprint_directory("onechannel", [".mp3"])
song = djv.recognize( FileRecognizer, "onechannel/output002.mp3")
#song = djv.recognize( FileRecognizer, "onechannel/Brad-Sucks--Total-Breakdown.mp3")
t = time.time() - t
#print(song)
print(t)
