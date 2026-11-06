from pypdf import PdfReader
import os

pdf_path = r'C:\Users\RATNAM\.gemini\antigravity\brain\42f7dfbc-fbdd-4efc-a787-be1bdeb5ffde\.user_uploaded\media_1793581761774_bc026220.pdf'
out_dir = r'C:\Users\RATNAM\.gemini\antigravity\scratch\water-potability-svm\reports\figures'

reader = PdfReader(pdf_path)
page0 = reader.pages[0]
for count, img in enumerate(page0.images):
    ext = img.name.split('.')[-1]
    target = os.path.join(out_dir, f'college_logo.{ext}')
    with open(target, 'wb') as fp:
        fp.write(img.data)
    print('Saved image:', target)
