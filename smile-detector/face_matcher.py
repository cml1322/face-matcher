#code forked and tweaked from https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py
#to extend, just add more people into the known_people folder

from typing import ForwardRef
import face_recognition
import cv2
import numpy as np
import os
import glob
import pickle
from pathlib import Path

class FacesLibrary:
    #List of encodings and names of face pictures
    def __init__(self):
        self.known_face_names=[]
        self.known_face_encodings=[]
        self.faces=[]
        self.list_of_files=[f for f in glob.glob(os.path.join(os.path.dirname(__file__),'known_encodings/')+'*.string')]
        return
    def encodePics(self):
        #Gets files from folder known_peoples, encodes files, then saves to known encodings
            #Gets files from folder known_people
        dirname=os.path.dirname(__file__)
        path=os.path.join(dirname,'known_people/')
        list_of_pics=[f for f in glob.glob(path+'*.jpg')]
        names=list_of_pics.copy()
        num_files=len(list_of_pics)
            #Saves files as encoding
        for i in range(num_files):
            globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_pics[i])
            globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
            self.known_face_encodings.append(globals()['image_encoding_{}'.format(i)])
            for x in range(len(names[i])-1,0,-1):
                if names[i][x]=='\\':
                    count=x
                    break
            #Sets name for picture
            self.known_face_names.append(names[i][count+1:-4])
        #Creates Face object and removes file from known_people
            self.faces.append(Face(self.known_face_encodings[len(self.known_face_encodings)-1],self.known_face_names[len(self.known_face_names)-1]))
        with os.scandir(os.path.join(os.path.dirname(__file__),'known_people')) as folder:
            for item in folder:
                os.remove(item)
        return
    def savePics(self):
        #Saves Face object into known encodings folder
        for x in self.faces:
            fileName=x.name+".pyc"
            with open(os.path.join(os.path.join(os.path.dirname(__file__),'known_encodings'),fileName),'wb') as fileName:
                fileName.write("".encode())
                pickle.dump(x,fileName)
        return
    def loadPics(self):
        #Loads Face objects from known encodings folder
        with os.scandir(os.path.join(os.path.dirname(__file__),'known_encodings')) as folder:
            for item in folder:
                with(open(item,"rb")) as personFolder:
                    try:
                        self.faces.append(pickle.load(personFolder))
                    except EOFError:
                        pass
        for x in self.faces:
            self.known_face_encodings.append(x.encoding)
            self.known_face_names.append(x.name)
        print("Loaded faces")
        return
class Face:
    def __init__(self,encoding,name):
        self.encoding=encoding
        self.name=name
        return
    def getName(self):
        return self.name
    def __str__(self):
        return self.name+str(self.encoding)
class Camera:
    def __init__(self):
        self.video_capture=cv2.VideoCapture(1)
        self.process_this_frame=True
        return
    def getFrame(self):
        # Grab a single frame of video
        ret,self.frame=self.video_capture.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        self.rgb_small_frame = small_frame[:, :, ::-1]
        return
    def processFrame(self,lib):
        # Only process every other frame of video to save time
        if self.process_this_frame:
        # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(self.rgb_small_frame)
            face_encodings = face_recognition.face_encodings(self.rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(lib.known_face_encodings, face_encoding)
                name = "Unknown"

                # If match found in known_face_encodings use first one.
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(lib.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = lib.known_face_names[best_match_index]

                self.face_names.append(name)
            

        self.process_this_frame = not self.process_this_frame
        return
    def displayResults(self):
    # Display the results
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(self.frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self.frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', self.frame)
        return
    def exit(self):
        # Release handle to the webcam
        self.video_capture.release()
        cv2.destroyAllWindows()
        return

def init():
    #Set up camera
    camera=Camera()
    print("Camera set up")
    lib = FacesLibrary()
    lib.encodePics()
    lib.savePics()
    lib.loadPics()
    print("Pictures load")
    return camera,lib

def main():
    print("main go brr")
    camera,lib=init()
    while True:
        camera.getFrame()
        camera.processFrame(lib)
        camera.displayResults()
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.exit()
    return
if __name__ == "__main__":
    main()