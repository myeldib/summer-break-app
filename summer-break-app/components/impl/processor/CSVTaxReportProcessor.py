import csv
import os
from collections import defaultdict, namedtuple

class CSVTaxReportProcessor(object):
    """A processor for csv tax report where total gross revenue, total net revenue, and expenses are computed. """ 

    def __init__(self):

        self._recordname = 'TaxReport'
        self._record_size = 4
        self._record_delimiter = ','
        self._record_headers = ['Date', 'Type', 'Amount' ,'Memo']
        self._transaction_type = ['Income', 'Expense']
        self._records = []
        self._gross_revenue = 0
        self._expenses  = 0
        self._net_revenue = 0
        self._memo_dict = {}

    def run(self, csv_file):

        if not os.path.isfile(csv_file):
            raise Exception('cannot open csv file %s', csv_file)
        
        self._csv_file = csv_file
        self._read_csv()
        self._gross_revenue = self._compute_gross_revenue()
        self._expenses = self._compute_expenses()
        self._net_revenue = self._compute_net_revenue()
        self._memo_dict = self._compute_transaction_memo()   

    def _read_csv(self):
        """ read csv file, and ignore bad entries
        """         
        with open(self._csv_file, 'r') as input_file:
            csv_data = csv.reader(input_file, delimiter=self._record_delimiter, skipinitialspace=True)
            Record = namedtuple(self._recordname, self._record_headers)
            for row in csv_data:
                if len(row) == self._record_size:
                    self._records.append(Record(*row))

            self._valid_fieldnames = set(self._record_headers)

    
    def _compute_gross_revenue(self):
        """ compute gross revenue
        """          
        gross_revenue = 0
        for index, record in enumerate(self._records):
            if getattr(record, self._record_headers[1]) == self._transaction_type[0]:
                gross_revenue += float(getattr(record, self._record_headers[2]))
        return gross_revenue

    def _compute_expenses(self):
        """ compute expenses
        """            
        expenses = 0
        for index, record in enumerate(self._records):
            if getattr(record, self._record_headers[1]) == self._transaction_type[1]:
                expenses += float(getattr(record, self._record_headers[2]))                
       
        return expenses


    def _compute_transaction_memo(self):
        """ compute transaction amount per memo 
        """
        memo_dict = {}

        for index, record in enumerate(self._records):
            memo_value = getattr(record, self._record_headers[3])
            memo_amount = getattr(record, self._record_headers[2])

            if memo_value not in memo_dict:
                memo_dict[memo_value] = float(memo_amount)           
            else:
                memo_dict[memo_value] += float(memo_amount) 

        return memo_dict             

    def _compute_net_revenue(self):
        """ compute net revenue
        """             
        return self._gross_revenue - self._expenses         
       
    def get_records(self):
        """ get csv records
        """          
        return self._records

    def get_gross_revenue(self):
        """ get total gross revenue amount
        """          
        return self._gross_revenue    

    def get_expenses(self):
        """ get total expense amount
        """              
        return self._expenses        

    def get_net_revenue(self):
        """ get total net revenue amount
        """        
        return self._net_revenue
    