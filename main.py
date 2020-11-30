import glob

def valid_columns(columns, length=-1):
  for column in columns:
    if len(column) <= 1:
      return False
  
  return True

white_spaces = [
  '', '\t', '\n', '\r', '\v', '\f'
]
comments = [
  '//', '#', '/*', '/*', '`' 
]

def is_comment(column):
  for comment in comments:
    if column.startswith(comment):
      return True

  return False  

def invalid_column_contents(column, sepparator):
  return not column in white_spaces and not is_comment(column) and not column.endswith('{\n') or not column.endswith('{')

def is_csv(file, min_valid_lines=1, sepparator=';'):
  with open(file, "r") as file:
    valid_line_count = 0
    total_lines = 0
    for line in file:
      columns = [col.strip() for col in line.split(sepparator) if invalid_column_contents(col, sepparator)]      
      column_count = len(columns)

      if column_count > 2:
        valid_line_count += 1
          
      if column_count > 1:
        if valid_columns(columns):
          valid_line_count += 1

      total_lines += 1
  if min_valid_lines > total_lines:
    min_valid_lines = total_lines
  return valid_line_count >= min_valid_lines

for text_file in glob.glob("./*.txt"):
  if is_csv(text_file, min_valid_lines=150, sepparator=';'):
    print(text_file, " is valid!")  