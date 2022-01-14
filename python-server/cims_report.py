#%%
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER


def generate_report( filename, report_data):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename, pagesize=A4)
    # container for the 'Flowable' objects
    elements = []

    myheading = styles["h4"]
    myheading.alignment = TA_CENTER
    
    mybodytext = styles["BodyText"]

    report = {
    "PCDT ID"               : [report_data["pcdt-id"]],
    "Custodian Payroll"     : [report_data["custodian-payroll"]],
    "custodian Name"        : [report_data["custodian-name"]],
    "custodian Mobile"      : [report_data["custodian-mobile"]],
    "Coins PO No."          : [report_data["coins-po-number"]],
    "GeM PO No."            : [report_data["gem-po-number"]],
    "Assembling Person"     : [report_data["deo"]],

    #                   Heeadings
    # =======================================================
    "Hardware Components"   : [],
    "Part"                  : [ "Brand", "S.No.", "Warranty" ],
    # =======================================================

    "CPU"                   : report_data["cpu"],
    "Motherboard"           : report_data["motherboard"],
    "RAM"                   : report_data["ram"],
    "HDD"                   : report_data["hdd"],
    "SSD"                   : report_data["ssd"],
    "SMPS"                  : report_data["smps"],
    "Cabinet"               : report_data["cabinet"],
    "Monitor"               : report_data["monitor"],
    "Mouse"                 : report_data["mouse"],
    "Keyboard"              : report_data["keyboard"],
    "Speakers"              : report_data["speakers"],
    "Webcam"                : report_data["webcam"],
    }

    output = []
    for k,v in report.items():

        style = mybodytext

        if k in ["Hardware Components","Part"]:
            temp = [Paragraph(k,myheading)]
            style = myheading
        else:
            temp = [k]
        
        for i in v:
            temp.append(Paragraph(i,style))    
        output.append(temp)

    table = Table(output, colWidths="*")

    table.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'LEFT'),
    ('SPAN', (1,0), (3,0)),
    ('SPAN', (1,1), (3,1)),
    ('SPAN', (1,2), (3,2)),
    ('SPAN', (1,3), (3,3)),
    ('SPAN', (1,4), (3,4)),
    ('SPAN', (1,5), (3,5)),
    ('SPAN', (1,6), (3,6)),
    ('SPAN', (0,7), (3,7)),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))

    elements.append(table)
    # write the document to disk
    doc.build(elements)