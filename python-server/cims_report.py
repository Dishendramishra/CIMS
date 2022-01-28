#%%
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.units import inch, mm

def generate_report( filename, report_data):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename, pagesize=A4)
    # container for the 'Flowable' objects
    elements = []

    myheading = styles["h4"]
    myheading.alignment = TA_CENTER
    
    mybodytext = styles["BodyText"]

    report = {
    f"Date: {report_data['date']}"     :   [],
    Image("python-server/static/img/prl_report.png",12*mm,12*mm)
                      : ["PC-DT assembled Scientific/Office System Details"],
    "PCDT ID"               : [report_data["pcdt-id"]],
    "Custodian Payroll"     : [report_data["custodian-payroll"]],
    "Custodian Name"        : [report_data["custodian-name"]],
    "Custodian Mobile"      : [report_data["custodian-mobile"]],
    "Asset ID"              : [report_data["asset-id"]],
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

    table.setStyle(TableStyle([
        # ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('SPAN', (0,0), (3,0)), ("ALIGN",(0, 0), (0, 0), "RIGHT"),        
        ('SPAN', (1,1), (3,1)), ("VALIGN",(1, 1), (1, 1), "MIDDLE"), 
        
        ('SPAN', (1,2), (3,2)),
        ('SPAN', (1,3), (3,3)),
        ('SPAN', (1,4), (3,4)),
        ('SPAN', (1,5), (3,5)),
        ('SPAN', (1,6), (3,6)),
        ('SPAN', (1,7), (3,7)),
        ('SPAN', (1,8), (3,8)),
        ('SPAN', (1,9), (3,9)),

        # hardware components
        ('SPAN', (0,10), (3,10)),

        ('INNERGRID', (0,2), (-1,-1), 0.25, colors.black),
        ('BOX', (0,2), (-1,-1), 0.25, colors.black),
    ]))

    elements.append(table)
    # write the document to disk
    doc.build(elements)


# data = {
#     "date"                : "01-01-2022",
#     "pcdt-id"             : "1234",
#     'custodian-payroll'   : '1234',
#     'custodian-email'     : 'test@gmail.com',
#     'custodian-name'      : 'Dishendra',
#     'custodian-mobile'    : '9898989898',
#     'coins-po-number'     : '1234',
#     'gem-po-number'       : '1234',

#     'cpu'           : ['Ryzen 5600g','NEW'],
#     'motherboard'   : ['ASRock','NEW'],
#     'ram'           : ['Crucial', 'NEW'],
#     'hdd'           : ['Crucial', 'NEW'],
#     'ssd'           : ['Crucial', 'NEW'],
#     'smps'          : ['Cooler Master', 'NEW'],
#     'cabinet'       : ['ASUS', 'NEW'],
#     'monitor'       : ['AOC', 'NEW'],
#     'mouse'         : ['Dell', 'New'],
#     'keyboard'      : ['Dell', 'New'],
#     'speakers'      : ['Dell', 'New'],
#     'webcam'        : ['Dell', 'New'],
#     'deo'           : 'dishendra'
#     }

# try:
#     import os
#     os.remove("test.pdf")
# except:
#     pass

# generate_report("test.pdf", data)
