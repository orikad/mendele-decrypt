# mendele scripts
A couple of scripts to get DRM-free versions of e-books that can be purchased on [מנדלי מוכר ספרים](https://mendele.co.il) but intended to be available only on their (pretty crappy) iOS/Android apps.

## download_mendele.py
Downloads your entire Mendele e-book library to .epub files.
This needs your user name (e-mail) and password.

### Usage
Make sure you have the requirements install using
```bash
pip install -r requirements.txt
```

Then simply:
```bash
python download_mendele.py 
```
This will ask for you e-mail and password, and then will download your e-book library to `mendele_books`.









___
Note that the `decrypt.py` script is really not needed anymore. Just use `download_mendele.py` instead. You can ignore the rest of this README.

## decrypt.py
Decrypts mendele's e-books into epubs. 
These books are simply encrypted with a const password (md5 of a weird string and your email).

This script takes an encrypted book (they call this 'sifri') and decrypts it into an epub you can use with any e-reader.

The decryption logic was reversed from their iOS app, although I bet the Android app is not too far off.

### Get an encrypted book
In order to get the encrypted 'sifri' book file, I've used a jailbroken iPhone which allowed me access into the Documents folder of the app.

If you use a re-signed app you can also perform this on a non-jailbroken device, but this is outside the scope of this readme.

Also pre-iOS 8.3, iOS had no access prevention to the Documents directory, so an old device would probably work too.

#### Usage
Then to decrypt:
```bash
./decrypt.py your@email.com input-file.sifri output-file.epub
```
