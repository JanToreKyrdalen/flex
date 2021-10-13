import configparser
from datetime import datetime, timedelta
from os.path import expanduser
from pathlib import Path

import requests
from dateutil import parser
from requests.auth import HTTPBasicAuth


class Workbook:
    def __init__(self):
        """Reads username and password from configfile
            C:/Users/[username]/.workbook/config.cfg on windows
            content:
            [workbook]
            username=username here
            password=password here

            initializes by reading all data and adding to a parameter called
            self.workbook_data
        """
        config = configparser.ConfigParser()
        config.read(Path(expanduser("~")) / r'.workbook\config.cfg')
        username = config['workbook']['username']
        password = config['workbook']['password']
        self.auth = HTTPBasicAuth(username, password)
        res = requests.get('https://noa.workbook.net/api/json/reply/FlexDayOverviewRequest',
                           auth=self.auth)
        self.workbook_data = res.json()

    def total_flex(self):
        """Returns total flex hours avaliable per yesterday

        Returns:
            float: flex hours in base 10
        """
        yesterday = datetime.today() - timedelta(days=1)
        todays_values = [x for x in self.workbook_data if parser.parse(
            x['DayDate']).date() == yesterday.date()][0]
        return (float(todays_values['Flex']))


if __name__ == '__main__':
    wb = Workbook()
    print(f'Du har {wb.total_flex()} timer flex på konto')
