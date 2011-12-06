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
print files
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
print "read " + str(doc.getNumberOfPages())
outline = PDOutline.PDDocumentOutline()
doc.getDocumentCatalog().setDocumentOutline(outline)

lastpg = -1
cat = doc.getDocumentCatalog()
print cat.getAllPages().size()
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
