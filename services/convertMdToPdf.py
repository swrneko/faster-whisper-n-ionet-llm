import re
from pylatexenc.latex2text import LatexNodes2Text
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section

class ConvertMdToPdf:
    # Конвертирует md в pdf
    def convertLatexToText(self, text:str):
        # Обрабатываем только математические выражения
        text = re.sub(
            r'\$\$(.*?)\$\$|\$(.*?)\$', 
            self.replace_math, 
            text, 
            flags=re.DOTALL
        )
        pdf = MarkdownPdf(toc_level=0, optimize=True)
        pdf.add_section(Section(text))
        return pdf, text

    def replace_math(self, match):
        math_content = match.group(1) or match.group(2)  # $$...$$ или $...$
        try:
            # Преобразуем только математическое выражение
            converted = LatexNodes2Text().latex_to_text(math_content)

            return converted
        except:
            return math_content  # В случае ошибки оставляем как есть

