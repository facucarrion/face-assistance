import cv2

def preprocess_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    gray_image = cv2.equalizeHist(gray_image) 
    return gray_image

def recognize_and_crop_image(image_to_crop, destine_path):
    image = cv2.imread(image_to_crop)
    image = cv2.rotate(image, cv2.ROTATE_180)
    processed_image = preprocess_image(image)
    
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cropped_face = None
    max_area = 0
    face_detected = False

    faces = face_classifier.detectMultiScale(
        processed_image, scaleFactor=1.1, minNeighbors=5
    )

    for (x, y, w, h) in faces:
        if w < 100 or h < 100:
            continue

        face_detected = True
        area = w * h

        if area > max_area:
            max_area = area
            cropped_face = processed_image[y:y+h, x:x+w]
            cropped_face = cv2.resize(cropped_face, (200, 200))
            

    if cropped_face is None:
        cropped_face = processed_image 

    return {
        'destine_path': destine_path,
        'cropped_face': cropped_face,
        'face_detected': face_detected 
    }

def compare_images(db_img, input_img):
    orb = cv2.ORB_create(nfeatures=1000)

    # Read the images
    db_img = cv2.imread(db_img)
    input_img = cv2.imread(input_img)
  
    # Check if images are loaded properly
    if db_img is None or input_img is None:
        return 0


  kpa, descr_a = orb.detectAndCompute(db_img, None)
  kpb, descr_b = orb.detectAndCompute(input_img, None)

    # Check if descriptors are valid
    if descr_a is None or descr_b is None:
        return 0

    # Create a Brute Force Matcher with Hamming distance
    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    # Match descriptors
    matches = comp.match(descr_a, descr_b)


    regiones_similares = [i for i in matches if i.distance < 50]


    # Avoid division by zero
    if len(matches) == 0:
        return 0

    # Calculate the coincidence ratio
    coincidence = len(regiones_similares) / len(matches)

    return coincidence