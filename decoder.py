import requests
from bs4 import BeautifulSoup

url = 'https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub'

# Parses out a table from the given content into an array of the rows excluding
# the header
def parse_table(content):
    soup = BeautifulSoup(content)
    table = soup.table
    rows = []
    trs = table.find_all('tr')
    for tr in trs:
        rows.append([td.get_text(strip=True) for td in tr.find_all('td')])
    rows = rows[1:]
    return rows
    
def prettyPrintMatrix(matrix):
    num_cols = len(matrix) - 1
    num_rows = len(matrix[0]) - 1
    while num_cols >= 0:
        rows = 0
        line = ''
        while rows <= num_rows:
            line = line + matrix[num_cols][rows]
            rows = rows + 1
        print(line)
        num_cols = num_cols - 1
    

def decoder(url):
    # Get the Google Doc and parse the table into an array of the rows
    response = requests.get(url)
    rows = parse_table(response.content)
    
    # Run through the rows in the table, and for each set of coordinates
    # expand the output matrix with spaces if necessary
    # and set the indicated coordinates to the given character
    num_rows = -1
    num_cols = -1
    output = []
    for row in rows:
        x = int(row[0])
        y = int(row[2])
        char = row[1]
        # If the matrix height is too small, expand up with spaces
        if y > num_cols:
            diff = y - num_cols
            while diff > 0:
                new_col = []
                rows_to_add = num_rows + 1
                while rows_to_add > 0:
                    new_col.append(" ")
                    rows_to_add = rows_to_add - 1
                output.append(new_col)
                diff = diff - 1
            num_cols = y
        # If the matrix width is too small, expand right with spaces
        if x > num_rows:
            diff = x - num_rows
            while diff > 0:
                for col in output:
                    col.append(" ")
                diff = diff - 1
            num_rows = x
        # Set the indicated coordinates to the given character
        output[y][x] = char
    
    # Run through the matrix rows, top to bottom, building a line
    # of the characters in the row from left to right, and print it
    prettyPrintMatrix (output)
        
decoder(url)