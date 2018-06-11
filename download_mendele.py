#!/usr/bin/env python2

import sys
import os
import requests
import hashlib
import base64
import getpass
import xml.etree.ElementTree
from functools import partial

class MendeleLibrary(object):
    class MendeleAccessDenied(Exception):
        pass

    def __init__(self, email, password):
        super(MendeleLibrary, self).__init__()
        self._email = email
        self._password = password
        self._request_headers = self._init_headers()
        self._library = {}

    def _init_headers(self):
        passhash = hashlib.md5(self._password).hexdigest().lower()
        auth = base64.encodestring(self._email + ":" + passhash).replace("\n", "")
        headers = {'Accept-Language': 'en-us',
                   'Authorization': 'Basic {}'.format(auth),
                   'Sifrilanguage': 'en-IL',
                   'Sifriuseremail': self._email,
                   'User-Agent': 'Mendele-ver2.2.3-IOS-iPhone'}
        return headers

    def load_library(self):
        if self._library:
            return self._library

        response = requests.post('https://mendele.sifriapp.co.il/myMendelelibrary', headers=self._request_headers)
        if 'NO ACCESS' in response.content:
            raise self.MendeleAccessDenied('Wrong e-mail and password combination!')

        xml_library = xml.etree.ElementTree.fromstring(response.content)
        for book_entry in xml_library.findall("{http://www.w3.org/2005/Atom}entry"):
            title = book_entry.findall("{http://www.w3.org/2005/Atom}title")[0].text
            for link in book_entry.findall("{http://www.w3.org/2005/Atom}link"):
                link = dict(link.items())
                if link["type"] == 'application/epub+zip' or link.get('href', '').endswith('.epub'):
                    break
            else:
                print u"ERROR: did not find epub link for {}".format(title)
                continue

            self._library[title] = link['href']

        return self._library


    def get_book(self, title):
        url = self.load_library()[title]

        response = requests.get(url, headers=self._request_headers)

        if response.status_code != 200:
            print "Download error status code: {}".format(response.status_code)
            return None

        book_data = response.content

        if not book_data.startswith("PK"):
            print u"Download error for title {}, downloaded file doesn't look like an EPUB".format(title)
            return None

        return book_data


def download_all(email, password, output_path):
    mendele = MendeleLibrary(email, password)
    
    library = mendele.load_library()
    if not len(library):
        print "You have no books in your library... Bye!"
        return
    print "Found {} books in your library!".format(len(library))

    for i, book in enumerate(library):
        print u"{}) {}".format(i+1, book)

    print "Downloading them all to: {}".format(output_path)
    
    try:
        os.makedirs(output_path)
    except OSError as e:
        if e.errno != 17: # file exists
            raise

    for book in library:
        print u"Downloading {}...".format(book)
        data = mendele.get_book(book)
        if data is not None:
            open(os.path.join(output_path, book + ".epub"), "wb").write(data)



def main():
    print "This will download your entire book library from mendele.co.il into mendele_books/"
    print "Your user name (e-mail) and password will be required."
    print "They will not be stored or transmitted in any form other than required to authenticate with mendele.co.il"
    print "Don't trust me, check the source"
    print

    output_path = "mendele_books"

    email = raw_input("Enter e-mail: ")
    password = getpass.getpass("Password: ")

    try:
        download_all(email, password, output_path)
    except MendeleLibrary.MendeleAccessDenied as e:
        print >> sys.stderr, e.message



if __name__ == '__main__':
    main()
