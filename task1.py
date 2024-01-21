import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)


class ProcessExcel:

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.data = None
        self.result = {}
        
    '''This method will read excel file and then return KPI's/compute values'''    
    def read_excel(self) -> dict:
        try:
            self.data = pd.read_excel(self.file_path)
            self.rename_colums()
            self.calc_daily_return()
            self.result['daily_volatility'] = self.get_daily_volatility()
            self.result['annualizied_volatility'] = self.get_annualizied_volatility()
            return self.result 
            
        except FileNotFoundError:
            logging.error('File path might not be correct')
        except Exception as exc:
            logging.error(f'Error occured while reading excel = {exc}')
            
    '''This method is created for reusablity of class for task 2'''
    def read_csv(self) -> dict:
        try:
            self.data = pd.read_csv(self.file_path)
            self.rename_colums()
            self.calc_daily_return()
            self.result['daily_volatility'] = self.get_daily_volatility()
            self.result['annualizied_volatility'] = self.get_annualizied_volatility()
            return self.result 
            
        except FileNotFoundError:
            logging.error('File path might not be correct')
        except Exception as exc:
            logging.error(f'Error occured while reading excel = {exc}')
    
    '''This method will remove extra space from columns for consistency perpose'''
    def rename_colums(self) -> None:
        try:
            new_col_names = {'Open ': 'Open', 'High ': 'High', 'Low ': 'Low', 'Close ': 'Close', 'Shares Traded ': 'Shares Traded',
                             'Date ': 'Date', 'Turnover (â‚¹ Cr)': 'Turnover'}
            self.data.rename(columns=new_col_names, inplace=True)
            
        except Exception as exc:
            logging.error(f'Some error occured while renaming columns = {exc}')

    '''This method will calc daily returns and save its value in its repective place'''
    def calc_daily_return(self) -> None:
        try:
            for index, row in self.data.iterrows():
                if index != 0:
                    current_close = row['Close']
                    previous_close = self.data.at[index - 1, 'Close']
                    daily_return = (current_close / previous_close) - 1
                else:
                    # Assuming 1st day wont have prev day data, so making it zero
                    daily_return = 0
                self.data.at[index, 'Daily Returns'] = daily_return
                
        except KeyError as ker:
            logging.error(f'Key not found = {ker}')
        except Exception as exc:
            logging.error(f'Some error occured while processing daily returns = f{exc}')

    '''This method will calc and return daily volatility'''
    def get_daily_volatility(self) -> float:
        try:
            self.daily_volatility = self.data['Daily Returns'].std()
            return self.daily_volatility
        
        except KeyError as ker:
            logging.error(ker)
            return 0

    '''This method will calc and return annualizied volatility'''
    def get_annualizied_volatility(self) -> float:
        try:
            length_of_df = self.data.shape[0]
            return self.daily_volatility * (length_of_df ** 2)
        
        except KeyError as ker:
            logging.error(ker)
            return 0


if __name__ == '__main__':
    file_name = 'NIFTY 50.xlsx'
    obj = ProcessExcel(file_name)
    logging.info(f'{obj.read_excel()}')
