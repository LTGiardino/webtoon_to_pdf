#!/bin/python
import requests as req
import PyPDF2 as pdf
from PIL import Image
import io
import re
import sys

full_name = sys.argv[1]
images = sys.argv[2:]
nro_total = len(images)
all_imgs = []

name_season = re.match('.*?/en/.*?/(.*?)/(.*?)/viewer.*', full_name)
name = name_season.group(1).replace('-','_')
seas_epi_nmbs = re.sub('season-(\d)-ep-(\d)',r'\1 \2', name_season.group(2)).split()
episode = f"S{seas_epi_nmbs[0]}E{seas_epi_nmbs[1]}"
epi_nmb = f"S{seas_epi_nmbs[0].zfill(2)}E{seas_epi_nmbs[1].zfill(3)}"

for n, image in enumerate(images):
    episode_img = dict(url='', locname='', web='', nmb=n)
    episode_img['locname'] = f"{name}_{episode}_{episode_img['nmb']}.jpg"
    print(f"\tDownload image {n+1}/{nro_total}          ", end='\r')

    episode_img['web'] = req.get(episode_img['url'], \
                                headers={'referer':'http://webtoons.com/'}, \
                                stream = True)

    assert episode_img['web'].status_code == 200, "No succesful connection"

    try:
        new_img = Image.open(io.BytesIO(episode_img['web'].raw.read()))
        if new_img.getpallete("RGB"): pass
    except AttributeError:
        print(f"\t\t\t\t\t {n+1} -> RGB", end='\r')
        new_img = new_img.convert("RGB")
    all_imgs.append(new_img)

    del episode_img['url']
    del episode_img['locname']
    del episode_img['web']
    del episode_img
print(f"\tCreating PDF                  ", end='\r')
# print(f"Total: {len(all_imgs)}     Expected: {nro_total}")
# for n, i in enumerate(all_imgs):
#     print(f"{n}: {i}\t{type(i)}")
all_imgs[0].save(f"{name}_{epi_nmb}.pdf", "PDF", resolution=20.0, save_all=True, append_images=all_imgs[1:-1])
