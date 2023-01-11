import sys
import os
import unittest

if os.environ.get('ROOT_PRJ_DIR') is None:
    print('ROOT_PRJ_DIR must be set before starting\n')
    sys.exit(1)

from components.impl.processor.CSVTaxReportProcessor import CSVTaxReportProcessor

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 

class CSVTaxReportProcessorTests(unittest.TestCase):

      def setUp(self):
         print("Running ", self._testMethodName)

      def test_noCSVFile(self):
         with self.assertRaises(Exception) as context:
            cSVTaxReportProcessor = CSVTaxReportProcessor()
            cSVTaxReportProcessor.run(ROOT_DIR + os.sep + "test_data/data1.csv")
            self.assertTrue('cannot open csv file' in context.exception)

      def test_readCSV(self):
         expected_record_len = 10
         cSVTaxReportProcessor = CSVTaxReportProcessor()
         cSVTaxReportProcessor.run(ROOT_DIR + os.sep + "test_data/data.csv")
         self.assertEqual(len(cSVTaxReportProcessor.get_records()), expected_record_len)

      def test_computeGrossRevenue(self):
         expected_gross_revenue = 225.0
         cSVTaxReportProcessor = CSVTaxReportProcessor()
         cSVTaxReportProcessor.run(ROOT_DIR + os.sep + "test_data/data.csv")
         self.assertEqual(cSVTaxReportProcessor.get_gross_revenue(), expected_gross_revenue)    

      def test_computeExpenses(self):
         expected_expenses = 72.93
         cSVTaxReportProcessor = CSVTaxReportProcessor()
         cSVTaxReportProcessor.run(ROOT_DIR + os.sep + "test_data/data.csv")
         self.assertEqual(cSVTaxReportProcessor.get_expenses(), expected_expenses) 

      def test_computeNetRevenue(self):
         expected_net_revenue= 152.07
         cSVTaxReportProcessor = CSVTaxReportProcessor()
         cSVTaxReportProcessor.run(ROOT_DIR + os.sep + "test_data/data.csv")
         self.assertEqual(cSVTaxReportProcessor.get_net_revenue(), expected_net_revenue)         


if __name__ == '__main__':
    unittest.main()





  
