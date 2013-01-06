import os
import shutil

def remove_gsus(att_dir):
  for file in os.listdir(att_dir):
    tmp_file = att_dir + os.sep + file + '_bu'
    att_file = att_dir + os.sep + file
    with open(tmp_file,'w') as out_f:
      with open(att_dir + os.sep + file,'r') as f:
        title_list = f.readline().split()
        att_list = f.readline().split()
      title_line = ''
      att_line = ''
      for att in title_list:
        if att == 'GSus':
          continue
        else:
          title_line += att + ' '
          att_line += '{:>{l}}'.format(att_list[title_list.index(att)],l=len(att)) + ' '
      out_f.write(title_line + '\n')
      out_f.write(att_line + '\n')
    os.remove(att_file)
    shutil.copy(tmp_file,att_file)
  return