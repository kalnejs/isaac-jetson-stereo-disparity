import cv2
import pathlib
import os


def loop(gstreamer_pipeline_string):
    capture = None
    grabbed = False
    frame = None
    count = 0

    try:
        # capture = cv2.VideoCapture(
        #     gstreamer_pipeline_string, cv2.CAP_GSTREAMER
        # )
        capture = cv2.VideoCapture("/dev/video0") # check this
    except RuntimeError:
        capture = None
        print("Unable to open camera")
        print("Pipeline: " + gstreamer_pipeline_string)
        return

    cv2.namedWindow("Capture", cv2.WINDOW_AUTOSIZE)

    os.mkdir(str(pathlib.Path(__file__).parent.resolve())+"/captured")

    while(True):

        if cv2.getWindowProperty("Capture",cv2.WND_PROP_VISIBLE) < 1:        
            break

        try:        
            grabbed, frame = capture.read()
            if(grabbed):
                cv2.imshow("Capture", frame)
        except RuntimeError:
            print("Could not read image from camera")

        # This also acts as
        keyCode = cv2.waitKey(1) & 0xFF
        # Stop the program on the ESC key
        if keyCode == 27:
            break

        if keyCode == 32:
            print("Saving {}".format(count))
            path = pathlib.Path(__file__).parent.resolve()
            cv2.imwrite("{}/captured/{}.jpg".format(path, count), frame)
            count = count + 1

#https://github.com/JetsonHacksNano/CSI-Camera/blob/master/dual_camera.py
def gstreamer_pipeline(
        sensor_id=0,
        capture_width=1920,
        capture_height=1080,
        display_width=1920,
        display_height=1080,
        framerate=30,
        flip_method=1,
    ):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


if __name__ == "__main__":
    loop(gstreamer_pipeline())