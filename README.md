# face-matcher
Detects persons name from live video based off of a saved picture.

Add a .jpg picture of person into known_people. The program will base the name of the person off of the file's name. The first time the program runs after adding the picture, it deletes the file from known_profile and moves all necessary information into known_encodings, so the file will appear as missing. This is intentional design and won't cause any errors.
