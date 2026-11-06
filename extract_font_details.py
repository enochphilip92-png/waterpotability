"""
Extract font sizes and text from the reference PDF to match typography exactly.
"""
from pypdf import PdfReader

pdf_path = r'C:\Users\RATNAM\.gemini\antigravity\brain\42f7dfbc-fbdd-4efc-a787-be1bdeb5ffde\.user_uploaded\media_1793581761774_bc026220.pdf'
reader = PdfReader(pdf_path)

print(f"Total pages: {len(reader.pages)}")
print()

for p_num in range(min(8, len(reader.pages))):
    page = reader.pages[p_num]
    visitor_data = []

    def make_visitor(data):
        def visitor(text, cm, tm, font_dict, font_size):
            if text and text.strip():
                size = round(abs(font_size), 2) if font_size else 0
                font_name = ''
                if font_dict:
                    font_name = str(font_dict.get('/BaseFont', font_dict.get('/FontFamily', '')))
                data.append({'text': text.strip()[:80], 'size': size, 'font': font_name})
        return visitor

    page.extract_text(visitor_text=make_visitor(visitor_data))
    print(f'=== PAGE {p_num + 1} ===')
    for item in visitor_data[:40]:
        print(f"  size={item['size']:6.2f} | font={item['font'][:40]:<40} | {item['text']}")
    print()
