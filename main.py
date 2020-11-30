import glob, time, sys, os
from multiprocessing import Pool


args = sys.argv
output_file_dir = "./script/output_csv_detection.txt"

try:
  if args[1] == '-out':
    output_file_dir == args[2]
except:
  print("Could not parse arguments running default")
  output_file_dir = "./script/output_csv_detection.txt"

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

def is_csv(filename, accuracy=90, sepparator=';'):
  with open(filename, "r") as file:
    valid_line_count = 0
    total_lines = 0
    for line in file:
      columns = [col.strip() for col in line.split(sepparator) if invalid_column_contents(col, sepparator)]      
      column_count = len(columns)

      if column_count > 2:
        valid_line_count += 1
      elif column_count > 1:
        if valid_columns(columns):
          valid_line_count += 1

      total_lines += 1

  precent_of_valid_lines = valid_line_count / (total_lines / 100)

  if precent_of_valid_lines >= accuracy:
    return filename
  else:
    return ''

if __name__ == '__main__':
  file_list = glob.glob("./*.txt")
  start_time = time.time()
  with Pool(4) as process_pool:
    processed_files = [filename for filename in process_pool.map(is_csv, file_list) if filename != '']

    os.makedirs(os.path.dirname(output_file_dir), exist_ok=True)

    with open(output_file_dir, "w") as out:
      for file in processed_files:
        out.write("{} \n".format(file))
      
      out.write("\n\nFinished in {} seconds".format(time.time() - start_time))
    print("Finished in {} seconds".format(time.time() - start_time))