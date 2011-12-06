"""
Copyright 2011 Mike Scarpati. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ''AS IS'' AND ANY EXPRESS OR 
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HODLER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import org.apache.pdfbox.util.PDFMergerUtility as PDFMergerUtility
import org.apache.pdfbox.pdmodel as PDModel
import org.apache.pdfbox.pdmodel.interactive.documentnavigation.outline as PDOutline
import os
import os.path
import glob
import re 

def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)
	
files = sorted_nicely(glob.glob(os.getcwd()+"\\*.pdf"))
fn = os.getcwd() + "\\combined.pdf"
pmerger = PDFMergerUtility()
pmerger.setDestinationFileName(fn)
myPDFs = []

for file in files:
    doc = PDModel.PDDocument.load(file)
    thisPDF = tuple([file, doc.getNumberOfPages(), os.path.basename(file)])
    myPDFs.append(thisPDF)
    doc.close()
    pmerger.addSource(file)
    
pmerger.mergeDocuments()
doc = PDModel.PDDocument.load(fn)
print "read " + str(doc.getNumberOfPages()) + "pages"
outline = PDOutline.PDDocumentOutline()
doc.getDocumentCatalog().setDocumentOutline(outline)

lastpg = -1
cat = doc.getDocumentCatalog()
for pdf in myPDFs:
    bm = PDOutline.PDOutlineItem()
    bm.setTitle(pdf[2])
    ## Get reference page
    pg = cat.getAllPages().get(lastpg+1)
    bm.setDestination(pg)
    outline.appendChild(bm)
    lastpg += pdf[1]

doc.save(fn)
doc.close()
