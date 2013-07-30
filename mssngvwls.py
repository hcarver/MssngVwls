from bs4 import BeautifulSoup
import random
import string
import re
try:
  import urllib2
except ImportError:
  # Python 3...
  import urllib as urllib2

def parse_wiki_page(url):
  request = urllib2.Request(url)
  request.add_header('User-Agent', 'Firefox ish')
  html = urllib2.build_opener().open(request).read()
  soup = BeautifulSoup(html)

  def extract_items(list):
    return map(lambda li: li.text.encode('ascii', 'ignore'), list.select('li'))

  lists = [extract_items(list) for list in soup.select('ul')]
  lists.extend([extract_items(list) for list in soup.select('ol')])

  def extract_table_items(table):
    col_count = len(table.select('tr')[0].select('td'))
    if col_count == 0:
      col_count = len(table.select('tr')[0].select('th'))
    return [[row.select('td')[col_num].text.encode('ascii', 'ignore') for row in table.select('tr') if len(row.select('td')) == col_count] for col_num in range(0, col_count)]

  tables = soup.select('table')
  for table in tables:
    lists.extend(extract_table_items(table))

  return lists

def test_with(list_array):
  def insert(str, pos):
    return str[:pos] + ' ' + str[pos:]

  while(True):
    sample = random.choice(list_array).upper()
    smpl = re.sub('[AEIOU ]', '', sample)

    spaces = random.sample(range(1, len(smpl)), len(smpl) / 3)    
    for space in spaces:
      smpl = insert(smpl, space)

    guess = raw_input(smpl + '\n')
    if guess.upper() == sample:
      raw_input("You're right!\n")
    else:
      raw_input("Actually, it was " + sample + "\n")
    pass

if __name__ == "__main__":
  url = raw_input('Enter the URL of a page that has a list or table I can test you on:\n')
  content = parse_wiki_page(url)

  content = [c for c in content if len(c) > 0]

  list_index = input('\nChoose a list to play with (based on a random sample):\n' + 
    string.join([str(i) + ': ' + re.sub('[\n\r]', '', random.choice(list)) for i,list in enumerate(content)], '\n')+'\n')
  chosen_list = content[list_index]
  
  test_with(chosen_list)
