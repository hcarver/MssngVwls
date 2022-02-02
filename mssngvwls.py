from bs4 import BeautifulSoup
import random
import string
import re
import urllib.request

def parse_wiki_page(url):
  request = urllib.request.Request(url, headers=
          {
 'User-Agent': 'Firefox ish'})
  html = urllib.request.urlopen(request).read()
  soup = BeautifulSoup(html, features="html.parser")

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

    guess = input(smpl + '\n')
    if guess.upper() == sample:
      input("You're right!\n")
    else:
      input("Actually, it was " + sample + "\n")
    pass

def create_list_option(index, list_option):
  print(list_option)
  return str(index) + ': ' + re.sub('[\n\r]', '', str(random.choice(list(list_option))))

if __name__ == "__main__":
  print(create_list_option(0, ['a', 'b']))

  url = input('Enter the URL of a page that has a list or table I can test you on:\n')
  content = parse_wiki_page(url)

  content = [list(c) for c in content if len(list(c))]
  print(content)

  content_options = [create_list_option(i, l) for i,l in enumerate(content)]
  list_index = input('\nChoose a list to play with (based on a random sample):\n' +
    '\n'.join(content_options)+'\n')

  chosen_list = content[list_index]

  test_with(chosen_list)
