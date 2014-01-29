import ast

def partition(parts):
  for i in range(0, 10):
    lower = i * 300000
    upper = (i + 1) * 300000
    ids = ast.literal_eval(open(str(lower) + '.' + str(upper), 'r').read())

    partition_size = len(ids) / parts
    print(partition_size)
    for j in range(0, parts - 1):
      lower_part = j * partition_size
      upper_part = (j + 1) * partition_size
      print('Putting in ' + str(lower_part) + ':' + str(upper_part))
      open(str(lower_part + lower) + '.' + str(upper_part + lower) + '.part', 'a+').write(str(ids[lower_part:upper_part]))
    print('Putting in ' + str(upper_part) + ':')
    open(str(upper_part + lower) + '.' + str(upper) + '.part', 'a+').write(str(ids[upper_part:]))

partition(3)
