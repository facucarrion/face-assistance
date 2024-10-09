import cv2

def recognize_and_crop_image(image_to_crop, destine_path):
    image = cv2.imread(image_to_crop)
    image = cv2.rotate(image, cv2.ROTATE_180)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cropped_face = None
    max_area = 0
    face_detected = False

    faces = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5
    )

    # Itera sobre las caras detectadas y elige la más grande
    for (x, y, w, h) in faces:
        if w < 100 or h < 100:  # Ignora caras demasiado pequeñas
            continue

        face_detected = True  # Si entra en el bucle, se ha detectado al menos una cara
        area = w * h

        if area > max_area:
            max_area = area
            cropped_face = image[y:y+h, x:x+w]

    if cropped_face is None:
        cropped_face = image  # Si no se detecta ninguna cara, usa la imagen completa

    return {
        'destine_path': destine_path,
        'cropped_face': cropped_face,
        'face_detected': face_detected  # Devuelve si se detectó una cara o no
    }
