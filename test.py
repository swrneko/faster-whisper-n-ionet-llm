from handlers.convertMdToPdf import ConvertMdToPdf
import re
# Создаем экземпляр класса
converter = ConvertMdToPdf()

# Тестовые примеры дробей
test_cases = [
    r"$\frac{1}{2}$",          # простая дробь
    r"$\dfrac{3}{4}$",         # дробь с displaystyle
    r"$\frac{a}{b} + \frac{c}{d}$",  # сложение дробей
    r"$$\frac{x^2}{y^3}$$",    # блочная дробь
    r"$\frac{\partial f}{\partial x}$"  # частная производная
]

for latex in test_cases:
    result = converter.replace_math(re.search(r'\$\$(.*?)\$\$|\$(.*?)\$', latex))
    print(f"Input: {latex}")
    print(f"Output: {result}")
    print("---")