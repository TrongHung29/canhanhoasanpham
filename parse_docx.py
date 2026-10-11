import xml.etree.ElementTree as ET
import sys
import io

def extract_text_from_docx_xml(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        text_lines = []
        # Find paragraphs
        for p in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            para_text = []
            for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                if t.text:
                    para_text.append(t.text)
            if para_text:
                text_lines.append(''.join(para_text))
            else:
                text_lines.append('')
        return '\n'.join(text_lines)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    with io.open('d:\\Dự Án\\extracted_text.txt', 'w', encoding='utf-8') as f:
        f.write(extract_text_from_docx_xml(sys.argv[1]))
