import cv2
import sys

def genBuffMask(bufferFrames):
    'create bitwise mask for buffer length'
    buffMask = 1
    for i in range(0, BUFF_LEN-1):
        buffMask = (buffMask)<<1 | buffMask
    return buffMask

BUFF_LEN = 30 # 30 seems to be optimal number of frames for buffer

buffMask = genBuffMask(BUFF_LEN)

print sys.argv, len(sys.argv)
cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

# input which camera to use
if len(sys.argv)==3:
    if sys.argv[2] == 0:
        camera = 0
    elif sys.argv[2] == 1:
        camera = 1
    else:
        camera = 0
else:
    camera = 0
cap = cv2.VideoCapture(0)

# create the VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG') # MJPG is encoding supported by Windows
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

currBuff = 0;

while True:

    # Capture frame-by-frame
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # begin face cascade
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.25,
        minNeighbors=5,
        minSize=(30, 30)
    )


    # updates current buffer
    pastBuff = currBuff
    currBuff = ( (currBuff << 1) | (len(faces)>0) ) & buffMask

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    if(currBuff > 0):
        out.write(frame)
    elif((pastBuff>0) & (currBuff == 0)): # after face detected, of face disappears for BUFF_LEN frames, stop recording
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)
    # cv2.imshow('Video', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
out.release()
cap.release()
cv2.destroyAllWindows()
