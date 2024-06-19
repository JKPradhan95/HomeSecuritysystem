import cv2
import yagmail
import time

def email(image_path):
    sender = 'jagdish95p@gmail.com'
    receiver = 'youthfighters2k@gmail.com'
    subject = 'Someone is in your house'
    contents = """
    Hi Jagdish,

    Someone is in your house. See the attached image for more details.
    """

    password = 'vrjz nibl ebjn zwhp'
    if not password:
        print("Error: PASSWORD environment variable not set.")
    else:
        print("PASSWORD environment variable is set.")

    try:
        yag = yagmail.SMTP(user=sender, password=password)
        print("SMTP client initialized.")

        yag.send(to=receiver, subject=subject, contents=contents, attachments=image_path)
        print("Email Sent!")

    except Exception as e:
        print(f"An error occurred: {e}")

video = cv2.VideoCapture(0)

if not video.isOpened():
    print("Error: Could not open video stream.")
    exit()

success, frame = video.read()
if not success:
    print("Error: Could not read frame from video stream.")
    video.release()
    exit()

height = frame.shape[0]
width = frame.shape[1]

face_cascade = cv2.CascadeClassifier('faces.xml')
if face_cascade.empty():
    print("Error: Could not load face cascade.")
    video.release()
    exit()

output = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))

last_email_time = 0
email_interval = 60  

count = 0

while success:
   
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_frame, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 4)

        current_time = time.time()
        if current_time - last_email_time > email_interval:
            image_path = 'detected_face.jpg'
            cv2.imwrite(image_path, frame)
            email(image_path)
            last_email_time = current_time

    output.write(frame)

    success, frame = video.read()
    if not success:
        print("Error: Could not read frame from video stream.")
        break
    count += 1
    print(count)

video.release()
output.release()
print("Video processing complete.")
