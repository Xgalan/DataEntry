from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import NamedStyle, Font, Border, Side


def export_xlsx(self, filename):
    um = self.units.description
    data = [(i+1,v,um) for (i,v) in enumerate(self.values)]
    wb = Workbook(write_only = True)
    ws = wb.create_sheet()
    # create some styles
    cellstyle = NamedStyle(name="highlight")
    headerstyle = NamedStyle(name='headercell')
    wb.add_named_style(cellstyle)
    wb.add_named_style(headerstyle)
    cellstyle.font = Font(name='Calibri', size=11)
    headerstyle.font = Font(name='Calibri', size=11, bold=True)
    bd = Side(border_style='thin')
    cellstyle.border = Border(bottom=bd, right=bd, top=bd, left=bd)
    headerstyle.border = Border(bottom=bd, right=bd, top=bd, left=bd)
    header_labels = ['#', 'Value', 'Units']
    # write header
    header = []
    for el in header_labels:
        cell = WriteOnlyCell(ws, value=el)
        cell.style = 'headercell'
        header.append(cell)
    ws.append(header)
    # write data
    for t in data:
        row = []
        for el in t:
            cell = WriteOnlyCell(ws, value=el)
            cell.style = 'highlight'
            row.append(cell)
        ws.append(row)
    wb.save(filename) # doctest: +SKIP
