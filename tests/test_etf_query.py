import unittest
from unittest.mock import patch, MagicMock
import yfinance as yf
from yfinance.screener.screener import screen
from yfinance.screener.query import ETFQuery
import pandas as pd

class TestETFQuery(unittest.TestCase):
    def test_setup_query(self):
        #test if format acceptable for request
        q_test = yf.ETFQuery('eq', ['exchange', 'NGM'])

        q_test_dict = q_test.to_dict()

        expected_json_format = {
            "operator": 'EQ',
            "operands": ['exchange', 'NGM']
        }

        self.assertEqual(q_test_dict, expected_json_format)

    def test_etf_with_screen(self):
        #test using query with screen(), ensure only etfs returned
        q_etf = yf.ETFQuery('eq', ['exchange', 'NGM'])
        q_etf_results = yf.screen(query=q_etf, size=30)

        df_query = pd.DataFrame(q_etf_results['quotes']) 
        print(df_query[['symbol', 'shortName']])

        #check whether any etfs returned (should be > 0 since only filter is on nasdaq)
        self.assertGreater(len([q_etf_results['quotes']]), 0)

        #check whether all results were etfs
        for quote in q_etf_results['quotes']:
            print(quote.get('shortName'))
            print("      ")
            print(quote.get('quoteType'))
            print("\n")
            #mutual fund tickers = 5 chars so ensure not mutual fund
            self.assertLess(len(quote.get('symbol')), 5)
            
            #etfs do not have return on equity ratio (ensure not equity)
            self.assertNotIn('returnonequity.lasttwelvemonths', quote)


if __name__ == '__main__':
    unittest.main()

        

