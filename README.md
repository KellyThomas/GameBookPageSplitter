# GameBookPageSplitter

## Purpose 

The PDF bootlegs of the classic 80's Grail Quest gamebooks by J. H. Brennan that were produced for Home of The Underdogs are scanned with two portrait orientation book pages per landscape orientation PDF page. This layout may have made sense in 2004 when most readers would be sitting in front of a desktop computer but it seems less than ideal for reading on a phone.

This tool is designed to split these PDF pages so they each contain one book page each.

## Usage

1. install requirements
2. place input PDF file in `input` directory
3. run `build.py`
4. find output PDF files in `output` directory

## What does it do?

In essence it will look for PDF files in the `input` directory and produce PDF files in the `output` directory.

Its basic workflow is:

1. split a PDF into numbered PNG files (e.g. `working/00010.png`, `working/00020.png`, etc.)
    1. if a PDF page is in portrait orientation it will be converted as is, if it has horizontal orientation it will be split in two.
    2. before writing the PNG each image has any left and right white columns trimmed and is then padded evenly back to its original dimensions, for clean scans this has the effect of replacing the uneven left/right margins from the printed book with a horizontally centered layout. 

2. If a PDF (e.g. `input/bookname.pdf`) has a matching directory containing image files (e.g. `input/bookname/00001.png`) these will will be copied to the working directory.  This allows for cover art, character sheets, etc. to be inserted.

3. The contents of the working directory are bundled into a PDF (e.g. `output/bookname.pdf`)

## Limitations

1. This converts text based PDF files to image based PDF files, this will break text-to-speech screen readers, text search, any hyperlinks that may be present, etc.
2. The horizontal trim and re-center tooling is pretty simple.  It is unable to clean up the noise present on the scans on GrailQuest3-TheGatewayOfDoom and these will be poorly aligned.
3. GQ8 is poorly centered, if the pdf page is split in the middle then it cuts through the content of some of the book pages. Centering the PDF page before splitting fixes this.
   But if QG7 is centered before splitting then the uneven outer margins of text only pages an full image pages causes page content to be split.
   It may not be possible to have a simple one size fits all solution.

## License
This tool leans heavily on the works of others, both open source and proprietary.

1. The gamebooks themselves are under copyright with "all rights reserved" and PDF scans of them should not be distributed with this tool. They can be found at various HotU mirrors and general archive sites.  I have included some miscellaneous images (located at `input/*/*.[png,gif]`) as an example of inserting loose pages.
2. It relies on Python, ImageMagick, and various python libraries (see `requirements.txt`).  These are all licensed and distributed separately.
3. This tool itself is offered under MPL-2.0, the files to which this license applies will contain this text:

  >This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

  For the purposes of clarification this license currently extends to:

   * build.py
   * README.md
   * requirements.txt