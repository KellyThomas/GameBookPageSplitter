"""
      This Source Code Form is subject to the terms of the Mozilla
      Public License, v. 2.0. If a copy of the MPL was not distributed
      with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import img2pdf
import os
import shutil
import math
from wand.image import Image as Image

step=10

def batch(bookname):
      global i
      i=step
      for loose in os.scandir(f'working'):
            if loose.name != '.gitignore':
                  os.remove(loose.path)

      # copy from pdf
      pdf = Image(filename=f'input/{bookname}.pdf', resolution=300)
      pdfimage = pdf.convert("png")
      pages  = []
      for img in pdfimage.sequence:
            pdfpage = Image(image=img)
            if pdfpage.width>pdfpage.height:
                  autocenter(pdfpage)
                  halfwidth = math.ceil(pdfpage.width/2)
                  left = pdfpage.region(width=halfwidth)
                  pages.append((left, 'left'))
                  right = pdfpage.region(x=pdfpage.width-halfwidth)
                  pages.append((right, 'right'))
            else:
                  pages.append((pdfpage, 'single'))
      for (page, placement) in pages:
            autocenter(page)
            page.reset_coords()
            writeimage(page)

      #nominal page size
      reference = pages[int(len(pages)/2)][0]
      refwidth = reference.width
      refheight = reference.height

      #insert loose pages
      for loose in os.scandir(f'input/{bookname}/'):
            img=Image(filename=loose.path)
            if img.height > refheight or img.width > refwidth:
                  img.resize(width=refwidth,height=refheight)
            img.reset_coords()
            img.save(filename=f"working/{loose.name}")

      #write pdf
      imgs =[]
      for img in os.scandir('working'):
            imgs.append(img.path)
      with open(f"output/{bookname}.pdf","wb") as f:
            f.write(img2pdf.convert(imgs))

def  writeimage(img):
      global i
      width = img.width
      height = img.height

      img.save(filename=f"working/{i:04d}.png")
      print(f"count: {i}")
      i += step

def northmargin(input_image):
      border=10
      img=input_image.clone()
      img.background_color='red'
      img.splice(width=0,height=border,y=img.height)
      img.trim()
      return input_image.height-(img.height-border)

def southmargin(input_image):
      border=10
      img=input_image.clone()
      img.background_color='red'
      img.splice(width=0,height=border,y=0)
      img.trim()
      return input_image.height-(img.height-border)

def trimleft(img):
      border=10
      img.background_color='red'
      img.splice(width=border, height=0,x=0)
      img.trim(reset_coords=True,background_color='white')
      return img

def trimright(img):
      border=10
      img.background_color='red'
      img.splice(width=border, height=0,x=img.width)
      img.trim(reset_coords=True,background_color='white')
      return img

def autocenter(img):
      height=img.height
      width=img.width
      trimleft(img)
      trimright(img)
      img.background_color='none'
      img.extent(width=width, height=height,gravity='center')


def main():
      for file in os.scandir(f'input'):
            if file.name.endswith(".pdf"):
                  bookname = file.name[:-4]
                  batch(bookname)
      # batch('GrailQuest8-LegionOfTheDead')



if __name__ == "__main__":
    main()
