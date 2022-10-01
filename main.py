import os
import re
import sys
from urllib.parse import urljoin
import requests

from bs4 import BeautifulSoup


def savepage(url, pagepath='page'):
    def savenrename(sp, pgfolder, s, u, tg, ier):

        if not os.path.exists(pgfolder):  # create only once
            os.mkdir(pgfolder)

        for res in sp.findAll(tg):  # images, css, etc..

            if res.has_attr(ier):  # check inner tag (file object) MUST exists

                try:
                    filename, ext = os.path.splitext(os.path.basename(res[ier]))  # get name and extension
                    filename = re.sub('\W+', '', filename) + ext  # clean special chars from name
                    fileurl = urljoin(u, res.get(ier))
                    filepath = os.path.join(pgfolder, filename)

                    # rename html ref so can move html and folder of files anywhere

                    res[ier] = os.path.join(os.path.basename(pgfolder), filename)

                    if not os.path.isfile(filepath):  # was not downloaded

                        with open(filepath, 'wb') as f:
                            filebin = s.get(fileurl)
                            f.write(filebin.content)

                except Exception as exc:
                    print(exc, file=sys.stderr)

    session = requests.Session()

    # ... whatever other requests config you need here

    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    path, _ = os.path.splitext(pagepath)
    pagefolder = path + '_files'  # page contents folder
    tags_inner = {'img': 'src', 'link': 'href', 'script': 'src'}  # tag&inner tags to grab

    for tag, inner in tags_inner.items():  # saves resource files and rename refs
        savenrename(soup, pagefolder, session, url, tag, inner)

    with open(path + '.html', 'wb') as file:  # saves modified html doc
        file.write(soup.prettify('utf-8'))


savepage('https://matronet.com/demo/builder-5', 'ksr')
