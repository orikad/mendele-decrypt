# mendele-decrypt
Decrypts mendele's e-books into epubs

# Overview
Mendele ([מנדלי מוכר ספרים](https://mendele.co.il)) is a great site to buy legal DRM-free e-books as epubs.
Although some of the books they're selling can be read only on their Android/iOS app. 
These books are simply encrypted with a const password (md5 of a weird string and your email).

This script takes an encrypted book (they call this 'sifri') and decrypts it into an epub you can use with any e-reader.

The decryption logic was reversed from their iOS app, although I bet the Android app is not too far off.

# Get an encrypted book
In order to get the encrypted 'sifri' book file, I've used a jailbroken iPhone which allowed me access into the Documents folder of the app.

If you use a re-signed app you can also perform this on a non-jailbroken device, but this is outside the scope of this readme.

Also pre-iOS 8.3, iOS had no access prevention to the Documents directory, so an old device would probably work too.

# Usage
Make sure you have the requirements install using
```bash
pip install -r requirements.txt
```

Then to decrypt:
```bash
./decrypt.py your@email.com input-file.sifri output-file.epub
```