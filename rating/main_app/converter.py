
def render_pdf(html, file):

    from xhtml2pdf import pisa

    resultFile = open(file, "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=resultFile, encoding='UTF-8')
    resultFile.close()
