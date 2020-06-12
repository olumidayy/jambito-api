from openpyxl import load_workbook


excel_file = 'jambito.xlsx'
wb = load_workbook(excel_file, data_only=True)
sh = wb.get_sheet_names()
jamb, olevel = wb[sh[1]], wb[sh[0]]

codeMap = {olevel[f'B{i}'].value: olevel[f'A{i}'].value for i in range(2, 28)}


def getHex(cell):
    return cell.fill.start_color.index


def getCodes(row):
    hexes = set([getHex(cell) for cell in row if cell.value is not None])
    # return hexes
    codes = []
    for hx in hexes:
        if hx == '00000000':
            codes.extend(
                [[codeMap[cell.value]] for cell in row if getHex(
                    cell) == '00000000' and isinstance(cell.value, float)])
        else:
            codes.append(
                [codeMap[cell.value] for cell in row if getHex(
                    cell) == hx and isinstance(cell.value, float)])
    codes.sort()
    return {
        f'{i}': codes[i]
        for i in range(len(codes))
    }


def getData():
    data = {}

    for row in range(2, 665):
        data[jamb[f'N{row}'].value] = getCodes(jamb[row])
    return data