from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth


class PDFHighlighter:
    def __init__(self, filename="highlighted_output.pdf"):
        self.filename = filename
        self.font_name = "DejaVu"
        self.font_size = 10
        self.page_width, self.page_height = A4
        self.margin_x = 50
        self.y = 800 
        self.line_height = 14
        self.max_width = self.page_width - 2 * self.margin_x

        self.color_map = {
            'black': colors.black,
            'blue': colors.blue,
            'red': colors.red,
            'green': colors.green,
            'yellow': colors.yellow,
            'default': colors.black,
        }

        
        pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))

        
        self.c = canvas.Canvas(self.filename, pagesize=A4)
        self.c.setFont(self.font_name, self.font_size)

    def render_sentence(self, sent, token_colors):
        self.check_page_break()
        x = self.margin_x

        for i, token in enumerate(sent):
            word = token.text + " "
            word_width = stringWidth(word, self.font_name, self.font_size)

            
            if x + word_width > self.margin_x + self.max_width:
                x = self.margin_x
                self.y -= self.line_height
                self.check_page_break()

            
            color = self.color_map.get(token_colors[i], colors.black)
            self.c.setFillColor(color)

            
            self.c.drawString(x, self.y, word)
            x += word_width

        self.y -= self.line_height

    def newline(self, lines: int = 1):
        self.y -= self.line_height * lines
        
    def check_page_break(self):
        if self.y < 50:
            self.c.showPage()
            self.c.setFont(self.font_name, self.font_size)
            self.y = self.page_height - 50

    def create_result(self, title="Результат"):
        self.c.showPage()
        self.c.setFont(self.font_name, 20)
        title_width = stringWidth(title, self.font_name, 20)
        self.c.drawString((self.page_width - title_width) / 2, self.y, title)
        self.y -= 30
        self.c.setFont(self.font_name, self.font_size)
        
    def render_result_sentence(self, sentence):
        self.check_page_break()
        x = self.margin_x

        for word in sentence.split():
            word_width = stringWidth(word + " ", self.font_name, self.font_size)

            if x + word_width > self.margin_x + self.max_width:
                x = self.margin_x
                self.y -= self.line_height
                self.check_page_break()

            self.c.setFillColor(self.color_map['black'])
            self.c.drawString(x, self.y, word + " ")
            x += word_width

        self.y -= self.line_height
        self.check_page_break()
	
    def save(self):
        self.c.save()
        
'''pdf = PDFHighlighter("output_with_title.pdf")
pdf.create_result("Результат")  # Добавляем заголовок на новую страницу

# Печать нескольких строк
sentences = [
    "Это первое предложение.",
    "Вот второе предложение, которое будет записано.",
    "И третье предложение для демонстрации."
]

for sentence in sentences:
    pdf.render_result_sentence(sentence)

pdf.save()  # Сохранить PDF'''
