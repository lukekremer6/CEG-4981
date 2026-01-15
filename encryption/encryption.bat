set image=sample_image.png

openssl enc -aes-256-cbc -pbkdf2 -in %image% -out encrypted_image.png -pass pass:password.txt