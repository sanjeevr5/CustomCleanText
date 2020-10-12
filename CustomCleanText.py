import re
import pickle
import unidecode
import cleantext
import ftfy
import autocorrect
import emoji
from bs4 import BeautifulSoup

class Custom_Clean_Text:

  """
  <b>Objective : Basic text cleaning module </b>
  <b> Features : Demojize, fixing contractions, removes HTML tags and checks spelling</b>
  <b> Input Params </b>
  <ol> 
  <li> lower:boolean - convert the sentece to lower case. Default is False.
  <li> unicode:String - Accepted unicode encoding/decoding params 'NFC' ,'NFD', 'NFKC', 'NFKD'. Default is NFKD.
  <li> to_ascii:boolean - Convert special characters to the closest approximation of ascii representation. Default is False.
  <li> retain_characters_only:boolean - No numbers and special characters allowed. Default is False.
  <li> tokenize_spl_items:boolean - Replace URL, Phone number, number, currency and email with special tokens. Default is False
  </ol>
  <b> Output </b>
  <ol>
  <li> Returns the cleaned string
  </ol>  


  """
  ###
  ####def __new__(cls):
  ####  ct = 0
  ####  required_packages = set(['unidecode', 'cleantext', 'ftfy', 'autocorrect', 'emoji'])
  ####  for package in required_packages:
  ####    if importlib.util.find_spec(package) is None:
  ####      ct += 1
  ####      print(f"{package} is not installed")
  ####      if package == 'cleantext':
  ####        package = 'clean-text'
  ####      print(f'Install using : pip install {package}')
  ####  if ct:
  ####    return None
  ####  else:
  ####    return super().__new__(cls)  

  def __init__(self, lower = False, unicode = 'NFKD', to_ascii = False, retain_chars_only = False, tokenize_spl_items = False):  
    #self.corpus = corpus
    self.lower = lower
    self.unicode =  unicode
    self.to_ascii = to_ascii
    with open('./CustomTextClean/data/collocations.pkl', 'rb') as f:
      self.cList = pickle.load(f)
      self.c_re = re.compile('(%s)' % '|'.join(self.cList.keys()))
    self.retain_chars_only = retain_chars_only
    self.tokenize_spl_items = tokenize_spl_items
    self.spell = autocorrect.Speller()

  def Contractions(self, text, c_re):
      def replace(match):
          return self.cList[match.group(0)]
      return self.c_re.sub(replace, text)

  def fix_sentence(self, sentence):
    sentence = re.sub(r'\s+', r' ', sentence)
    sentence = re.sub(r'\n+', r'', sentence)
    sentence = emoji.demojize(sentence)
    soup = BeautifulSoup(sentence, "html.parser")
    sentence = soup.text
    if self.lower:
      sentence = sentence.lower()
    if self.to_ascii:
      sentence = unidecode.unidecode(sentence)
    sentence = ftfy.fix_text(sentence, normalization = self.unicode)
    if self.tokenize_spl_items:
      sentence = cleantext.clean(sentence, lower = False, fix_unicode= False, to_ascii = False,
                                 replace_with_url="<URL>", replace_with_email="<E-ADDRESS>", replace_with_phone_number="<PHONE>", 
                                 no_urls=True, no_emails=True, no_phone_numbers=True,
                                 no_numbers=True, no_currency_symbols=True,
                               replace_with_number="<NUMBER>", replace_with_currency_symbol="<CUR>")
    sentence = self.Contractions(sentence, self.c_re)
    sentence = re.sub("(.)\\1+",r"\1\1", sentence)
    sentence = self.spell(sentence)
    if self.retain_chars_only:
      sentence = re.sub(r'[^A-Za-z\s]', r'', sentence)
    
    return re.sub(r'\s+', ' ', sentence)  
  
