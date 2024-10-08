import cv2
import os

ROOT = os.path.join(os.getcwd(),'picture')
FACES  = os.path.join(os.getcwd(),'faces')
TRAIN = os.path.join(os.getcwd(),'training')

def detect(srcdict=ROOT,tgtdir=FACES,dir=TRAIN):
    for fname in os.listdir(srcdir):
        if not fname.upper().endswith('.JPC'):
            continue
        fullname = os.path.join(srcdir,fname)
        newname = os.path.join(tgtdir,fname)
        img = cv2.imread(fullname)
        if img is None:
            continue

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        training = os.path.join(train_dir,'haarcascade_frontalface.xml')
        cascade = cv2.CascadeClassifier(training)
        rects = cascade.detectMultiscale(gray,1.3,5)
        try:
            if rects.any():
                print('Got a face')
                rects[:,2] += rects[:,:2]
        except AttributeError:
            print(f'No faces found in {fname}')
            continue
        for x1,y1,x2,y2 in rects:
            cv2.rectangle(img,(x1,y1),(x2,y2),(127,255,0),2)
        cv2.imwrite(newname,img)

if name == '__main__':
    detect()
