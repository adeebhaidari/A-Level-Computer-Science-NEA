import sqlite3, os
from fpdf import FPDF

def save_solve(scramble, solution, preferred):
    connection = sqlite3.connect('speedcubing.db')
    cursor = connection.cursor()

    scramble_str = ' '.join(scramble)
    solution_str = ' '.join(solution)
    move_count = len(solution)
    
    cursor.execute('''
    INSERT INTO ExportedSolves (Scramble, Solution, SolutionLength, PreferredMethod)
    VALUES (?, ?, ?, ?)
    ''', (scramble_str, solution_str, move_count, preferred))
    
    connection.commit()
    connection.close()

def sort_solves(data):
    if len(data) <= 1:
        return data
    
    middle = len(data) // 2
    left = sort_solves(data[:middle])
    right = sort_solves(data[middle:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i][2] <= right[j][2]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[i])
            j += 1
            
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def download_history():
    connection = sqlite3.connect('speedcubing.db')
    cursor = connection.cursor()

    cursor.execute('SELECT Scramble, Solution, SolutionLength, PreferredMethod, Date FROM ExportedSolves')
    rows = cursor.fetchall()
    connection.close()
    
    if not rows:
        return None
    
    sorted_rows = sort_solves(rows)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Solve History', ln=True)
    pdf.ln(5)

    pdf.set_font('Arial', '', 10)

    for i, row in enumerate(sorted_rows, 1):
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, f'Solve #{i} - {row[4][:16]}', ln=True)
        
        pdf.set_font('Arial', '', 10)
        
        pdf.write(5, 'Scramble: ')
        pdf.write(5, f'{row[0]}\n')

        pdf.write(5, 'Solution: ')
        pdf.write(5, f'{row[1]}\n')

        pdf.write(5, f'Length: {row[2]} moves\n')
        pdf.write(5, f'Preferred: {row[3]}\n')

        pdf.ln(10)

    file_path = 'cube_history.pdf'
    pdf.output(file_path)
    return os.path.abspath(file_path)