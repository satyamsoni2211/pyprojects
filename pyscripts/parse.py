#!/appl/pm/vendor/python/lx-x86_64/2.7.9/bin/python

'''
this process help to find out the missing indexes received  by Markit 
for different composites like cdx, mcdx, itraxx etc.
user just need to fill the indexes and term  in a file seperated by commas 
and pass it into the process. Rest the process will do :)
header = ['Date',
       'Name',
       'Series',
       'Version',
       'Term',
       'RED Code',
       'Index ID',
       'Maturity',
       'On The Run',
       'Composite Price',
       'Composite Spread',
       'Model Price',
       'Model Spread',
       'Depth',
       'Heat']
'''

import re
import os
from datetime import datetime,timedelta
import argparse

#ETL Modules
from EtlPy.Db import Db

global price_date,missing,sent_to
missing = []

def getDate(*date):
   prev_price_date = ''
   today = datetime.strptime(date[0],'%Y%m%d') if len(date)>0 else \
           datetime.today()
   if today.weekday() == 0: #if Monday then Friday
      prev_price_date = today - timedelta(3)
   elif today.weekday() == 6: #if Sunday then Friday
      prev_price_date = today - timedelta(2)
   else: # else day - 1
      prev_price_date = today - timedelta(1)
   prev_price_date = prev_price_date.strftime('%Y%m%d')
   return prev_price_date

def get_connection():
        #Database connection

   syb_Db = Db()
   syb_dbh = syb_Db.dbConn()
   cursor = syb_dbh.cursor()
   return cursor

def fetchData(index,term):
   #definition
   global price_date
   #description map
   desc = {
   'cdx' : 'Markit CDX Index Composites',
   'mcdx' : 'Markit MCDX Index Composites',
   'itraxx' : 'Markit iTraxx Index Composites',
   'itraxx_asia' : 'Markit iTraxx Asia Index Compo',
   'itraxx_sovx' : 'Markit iTraxx SovX Index Compo'}

   term = ','.join([str(i) for i in term]) if len(term)>1 else term[0]
   
   sql = ("select issuer_id,term,currency from pm..cds_hist_multi_terms where asof_date = '{}' "
   "and description like '{}' and source = 'MIP' and term in ({}) "
   "and issuer_id not in "
   "("
   "select issuer_id from pm..cds_hist_multi_terms where asof_date = '{}' "
   "and description like '{}' and source = 'MIP' and term in ({}) "
   ")").format(getDate(price_date),desc[index],term,price_date,desc[index],term)
   
   print sql
   cur = get_connection()
   cur.execute(sql)
   results = list({ (result.rstrip('_MKT').rstrip('_NAV'),term,currency) \
             for result,term,currency in cur.fetchall() })
   return results

def findMissing(index,term):
   #definition
   global missing 

   miss = fetchData(index,term)
   data = parseTab(index) #data is available in data list
   hash = mapComp(index)

   prefix = {
   'cdx' : 'CDX',
   'mcdx' : 'MCDX.',
   'itraxx' : 'Traxx ',
   'itraxx_asia' : 'iTraxx ',
   'itraxx_sovx' : 'iTraxx '}
  
   for i,j,c in miss:
      
      tick = [(hash[k],re.match(k,i).groups()[0]) for k in hash.keys() if re.match(k,i)]
      ticker = prefix[index]+tick[0][0]
      series = tick[0][1]
      term = str(j)+'Y'
      print 'missing ticker {} series {} term {}\n'.format(ticker,series,term)
      try: # if ticker not found in file so it will throw error
         line = data[ticker][series][term][max(data[ticker][series][term].keys())]
         line['Currency'] = c
         missing.append(line)
      except:
         print "Ticker not found in {}_index_composites.tab file".format(index)

def parseTab(index):
   
   header,data = [],{}
   
   file = '/home/datap/prod/U/markit/index_composites/{}/{}_index_composites.tab'.format(index,index)
   
   #to test the code with manual tab file comment the above and uncomment below 
   #and edit the file location
   #file = '/home/sasoni/{}_index_composites.tab'.format(index,index)
   with open(file,'r') as fh:
      for i in fh:
         if re.match('Indices Composites',i) or  re.match('^\s{0,}$',i) :
            continue
         if re.match('Date',i):
            header = i.strip('\n').split('\t')
            continue
         line = dict(zip(header,i.strip('\n').split('\t')))
         
         #parsing the data as nested dictionary so that it can be used later
         if line['Name'] not in data.keys():
            data[line['Name']] = {line['Series']:{line['Term']:{line['Version']:line}}}
         elif line['Series'] not in data[line['Name']].keys():
            data[line['Name']][line['Series']] = {line['Term']:{line['Version']:line}}
         elif line['Term'] not in data[line['Name']][line['Series']].keys():
            data[line['Name']][line['Series']][line['Term']] = {line['Version']:line}
         else:
            data[line['Name']][line['Series']][line['Term']][line['Version']] = line
   return data

def createFile():
   
   #function to create challenge sheet
   global missing,send_to
   
   file = 'dataChallenge.csv'
   with open(file,'w') as cs:
      cs.write("Date challenged,RED Code/Ticker,Tenor(s),Currency,Series,Version\n")
      for i in missing:
         cs.write(','.join([i['Date'],'{}/{}'.format(i['RED Code'],i['Name']),\
               'Term={}'.format(i['Term']),i['Currency'],i['Series'],i['Version']])+'\n')
   if missing: mailFile(sent_to,file)


def mapComp(index):
   
   #regex map for indexes
   
   cdx = {'EM(\d+).*': 'EM',
            'EMDIV(\d+).*': 'EMDIV',
            'HV(\d+).*': 'NAIGHVOL',
            'HY(\d+).*': 'NAHY',
            'HY(\d+).*B': 'NAHYB',
            'HY(\d+).*BB': 'NAHYBB',
            'HY(\d+).*HB': 'NAHYHB',
            'IG(\d+).*': 'NAIG',
            'IG(\d+).*CONS': 'NAIGCONS',
            'IG(\d+).*ENRG': 'NAIGENRG',
            'IG(\d+).*FIN': 'NAIGFIN',
            'IG(\d+).*INDU': 'NAIGINDU',
            'IG(\d+).*TMT': 'NAIGTMT',
            'XO(\d+).*': 'NAXO'}
   
   itraxx = {'IT(\d+).*': 'Eur',
            'IT(\d+).*AUTO': 'Eur Autos',
            'IT(\d+).*CONS': 'Eur Cons',
            'IT(\d+).*CORP': 'Eur Corp',
            'IT(\d+).*CYCCON': 'Eur Cons Cyc',
            'IT(\d+).*ENRG': 'Eur Energy',
            'IT(\d+).*INDU': 'Eur Indls',
            'IT(\d+).*NCYCCON': 'Eur Cons Non Cyc',
            'IT(\d+).*NFIN': 'Eur Non Finl',
            'IT(\d+).*SENFIN': 'Eur Sr Finls',
            'IT(\d+).*SUBFIN': 'Eur Sub Finls',
            'IT(\d+).*TMT': 'Eur TMT',
            'IV(\d+).*': 'Eur HiVol',
            'IX(\d+).*': 'Eur Xover'}
   
   itraxx_asia = {
            'ITJ(\d+).*': 'Japan'
               }
   
   itraxx_sovx = {
            'SV(\d+).*': 'SovX Westn Europe'
   }
   
   mcdx = {
            'MCDX(\d+).*': 'NA'
   }
   
   #returning map matching to index
   if index=='cdx':
      return cdx
   elif index=='mcdx':
      return mcdx
   elif index =='itraxx':
      return itraxx
   elif index=='itraxx_asia':
      return itraxx_asia
   elif index=='itraxx_sovx':
      return itraxx_sovx

def mailFile(send_to,file) :
#Function to mail the challenge sheet
   
   import smtplib
   from email.mime.application import MIMEApplication
   from email.mime.multipart import MIMEMultipart
   from email.mime.text import MIMEText
   from email.utils import COMMASPACE, formatdate

   global price_date
   mail_path = os.getenv('TRDATADIR')+ "/mail_ids/%s"%send_to
   f = open(mail_path)
   mail_id = f.read()
   f.close()
   	
   strTo = mail_id
   
   msgRoot = MIMEMultipart()
   msgRoot['Subject'] = 'Data challenge sheet for missing composites from Markit [ {} ]'.format(price_date)
   msgRoot['From'] = 'Techops@Pimco.com'
   msgRoot['To'] = strTo
   msgRoot['Date'] = formatdate(localtime=True)
   
   msgText = MIMEText('Please find attached Data Challenge sheet to escalate to Markit')
   msgRoot.attach(msgText)
   
   with open(file, "rb") as fil:
      part = MIMEApplication(
            fil.read(),
            Name=os.path.basename(file)
            )
   #attaching the file after file is closed
   part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(file)
   msgRoot.attach(part)
   
   #Connecting to server and sending mail
   smtp = smtplib.SMTP()
   smtp.connect('mail')
   smtp.sendmail('techops@pimco.com', strTo.split(","), msgRoot.as_string())
   print "Data Challenge sheet {} sent to {}. Please check".format(file,strTo)
   smtp.quit()

if __name__ == '__main__':

   #parsing argument
   parser = argparse.ArgumentParser()
   parser.add_argument('--price_date', action='store', dest='price_date',  help='Provide price date in format YYYYMMDD')
   parser.add_argument('--index_file', action='store', dest='index_file', help="Please provide the file for indexes to check as index_name,term")
   parser.add_argument('--mail_ids', action='store', dest='mail_id', required=True, help="Please provide mail id to send the file")

   args = parser.parse_args()
   
   price_date = getDate() 
   if args.price_date:
      price_date = args.price_date
   print 'Price date is {}'.format(price_date)
   
   #to test the code for harcoded date uncomment the below
   #price_date = '20170329'
  
   #Check if mail id is provided or not else raise exception
   if args.mail_id:  sent_to = args.mail_id

   index_file = '/home/sasoni/index.txt'
   
   if args.index_file:
      index_file = args.index_file
   
   with open(index_file) as idx:
      for i in idx:
         i = i.strip('\n').split(',')
         findMissing(i[0],i[1:])
   
   
   if len(missing)==0:
      print "No missing indexes for today {}\n".format(price_date)
   else:
      createFile() # Creating data challenge sheet 
      print "Challenge sheet available at {}\n".format(os.getcwd()+'/dataChallenge.csv')
