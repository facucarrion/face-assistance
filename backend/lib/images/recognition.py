import cv2

def recognize_and_crop_image(image_to_crop, destine_path):
  image = cv2.imread(image_to_crop)
  image = cv2.rotate(image, cv2.ROTATE_180)
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
  face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

  cropped_face = None
  max_area = 0

  face = face_classifier.detectMultiScale(
    gray_image, scaleFactor=1.1, minNeighbors=5
  )

  for i, (x, y, w, h) in enumerate(face):
    if (w < 120 or h < 120):
      continue

    area = w * h

    if (area > max_area):
      max_area = area
      cropped_face = image[y:y+h, x:x+w]

  if cropped_face is None:
    cropped_face = image
  
  return {
    'destine_path': destine_path,
    'cropped_face': cropped_face
  }
