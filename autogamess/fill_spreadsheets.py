from .config   import *
from .data_finder import *
from .get_data import get_data
from openpyxl import load_workbook

def fill_spreadsheets(projdir=False, sorteddir=False, sheetsdir=False):
    """
    """
    #Defining directory names
    if projdir is not False:
        sorteddir      = projdir + 'Logs/Sorted/'
        sheetsdir      = projdir + 'Spreadsheets/'
        faildir        = projdir + 'Logs/Fail/Unsolved/'
        passdir        = projdir + 'Logs/Pass/'

    #Check to make sure sorteddir and sheetsdir exist
    if not os.path.isdir(sorteddir):
        print(error_head + "sorteddir does not exist" + error_tail)
        return
    if not os.path.isdir(sheetsdir):
        print(error_head + "sheetsdir does not exist" + error_tail)
        return

    #Define Sheet names
    opt = 'Optimization'
    hes = 'Hessian'
    ram = 'Raman'
    vsc = 'VSCF'

    #Define Data Column names
    rt = 'Run Time'
    bs = 'Basis Set'
    cp = 'CPU Percentage'
    te = 'Theory'


    for dir in os.listdir(sorteddir):
        df = pd.read_excel(sheetsdir + dir + '.xlsx', index_col=0,
                           sheet_name=None, header=6)

        for file in os.listdir(sorteddir + dir):
            if '.log' not in file:
                continue
            filename = sorteddir + dir + '/' + file
            theo = file.split('_')[2]
            bset = file.split('_')[3]
            data = get_data(filename)

#---------------OPTIMIZATION FILES-------------------------------------
            if '_opt' in file:
                temp = df[opt]

                if rt not in df[opt]:
                    df[opt][rt] = np.nan
                if cp not in df[opt]:
                    df[opt][cp] = np.nan

                if optimization(filename) == (0,0,0):
                    move2 = faildir + file
                    os.rename(filename, move2)
                    continue

                temp=temp.loc[temp[te]==theo]
                temp=temp.loc[temp[bs]==bset]

                lengths = data.bond_lengths
                for l in lengths:
                    if l not in df[opt]:
                        df[opt][l] = np.nan
                    temp[l] = lengths[l]
                    df[opt].update(temp)

                angles = data.bond_angles
                for a in angles:
                    if a not in df[opt]:
                        df[opt][a] = np.nan
                    temp[a] = angles[a]
                    df[opt].update(temp)

                temp[rt] = data.time
                temp[cp] = data.cpu

                df[opt].update(temp)

                move2 = passdir + opt + '/' + dir + '/' + file
                os.rename(filename, move2)

#-------------------HESSIAN FILES----------------------------------------
            if '_hes' in file:
                temp = df[hes]

                if rt not in df[hes]:
                    df[hes][rt] = np.nan
                if cp not in df[hes]:
                    df[hes][cp] = np.nan

                if hessian(filename) == (0,0,0):
                    move2 = faildir +  file
                    os.rename(filename, move2)
                    continue

                temp=temp.loc[temp[te]==theo]
                temp=temp.loc[temp[bs]==bset]

                frequency = data.vib_freq
                for key in frequency:
                    for i in range(len(frequency[key])):
                        vi = '(' + str(key) + ')Vibrational Frequency ' + str(i)
                        if vi not in df[hes]:
                            df[hes][vi] = np.nan
                        temp[vi] = frequency[key][i]
                        df[hes].update(temp)

                ir = data.ir_inten
                for key in ir:
                    for i in range(len(ir[key])):
                        vi = '(' + str(key) + ')Infrared Intensity ' + str(i)
                        if vi not in df[hes]:
                            df[hes][vi] = np.nan
                        temp[vi] = ir[key][i]
                        df[hes].update(temp)

                temp[rt] = data.time
                temp[cp] = data.cpu

                df[hes].update(temp)

                move2 = passdir + hes + '/' + dir + '/' + file
                os.rename(filename, move2)

#---------------RAMAN FILES------------------------------------------------
            if '_raman' in file:
                temp = df[ram]

                if rt not in df[ram]:
                    df[ram][rt] = np.nan
                if cp not in df[ram]:
                    df[ram][cp] = np.nan

                if raman(filename) == (0,0,0):
                    move2 = faildir + file
                    os.rename(filename, move2)
                    continue

                temp=temp.loc[temp[te]==theo]
                temp=temp.loc[temp[bs]==bset]

                ramans = data.raman
                for key in ramans:
                    for i in range(len(ramans[key])):
                        vi = '(' + str(key) + ')Raman Activity ' + str(i)
                        if vi not in df[ram]:
                            df[ram][vi] = np.nan
                        temp[vi] = ramans[key][i]
                        df[ram].update(temp)

                temp[rt] = data.time
                temp[cp] = data.cpu

                df[ram].update(temp)

                move2 = passdir + ram + '/' + dir + '/' + file
                os.rename(filename, move2)

#-------------------------VSCF Files-------------------------------------
            if '_vscf' in file:
                temp = df[vsc]

                if rt not in df[vsc]:
                    df[vsc][rt] = np.nan
                if cp not in df[vsc]:
                    df[vsc][cp] = np.nan

                if vscf(filename) == (0,0,0):
                    move2 = faildir + file
                    os.rename(filename, move2)
                    continue

                temp=temp.loc[temp[te]==theo]
                temp=temp.loc[temp[bs]==bset]

                vscf_freq = data.vscf_freq
                for key in vscf_freq:
                    vi = '(' + str(key) + ')VSCF Frequency '
                    if vi not in df[vsc]:
                        df[vsc][vi] = np.nan
                    temp[vi] = vscf_freq[key]
                    df[vsc].update(temp)

                vscf_ir = data.vscf_ir
                for key in vscf_ir:
                    vi = '(' + str(key) + ')VSCF IR '
                    if vi not in df[vsc]:
                        df[vsc][vi] = np.nan
                    temp[vi] = vscf_ir[key]
                    df[vsc].update(temp)

                temp[rt] = data.time
                temp[cp] = data.cpu

                df[vsc].update(temp)

                move2 = passdir + vsc + '/' + dir + '/' + file
                os.rename(filename, move2)

        #Write Spreadsheets
        book = load_workbook(sheetsdir + dir + '.xlsx')
        with pd.ExcelWriter(sheetsdir + dir + '.xlsx', engine='openpyxl') as writer:
            writer.book = book
            writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
            df[opt].to_excel(writer, sheet_name=opt, startrow=6)
            df[hes].to_excel(writer, sheet_name=hes, startrow=6)
            df[ram].to_excel(writer, sheet_name=ram, startrow=6)
            df[vsc].to_excel(writer, sheet_name=vsc, startrow=6)

    return
