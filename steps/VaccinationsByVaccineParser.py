from abc import ABC
from abstract.AbstractStep import AbstractStep, StepError
from misc.Converters import str_to_integer
from io import StringIO
import logging
import csv

class VaccinationsByVaccineParser(AbstractStep):
    def run(self, data):
        with StringIO(data.decode('utf-8')) as vaccine_csv:
            dict = None
            moderna_count = 0
            astrazeneca_count = 0
            janssen_count = 0
            comirnaty_count = 0

            ''' NOTE: the first line is the header '''
            csv_reader = csv.reader(vaccine_csv, delimiter=',')
            index = 0
            for line in csv_reader:
                if index > 0:
                    vacc_name = line[2]
                    vacc_count = line[4]
                    try:
                        vacc_count = str_to_integer(vacc_count, '+')
                    except Exception as e:
                        raise StepError('unexpected vlaue for vacc_count.') from e
                    if vacc_name == 'Moderna':
                        moderna_count += vacc_count
                    elif vacc_name == 'AstraZeneca':
                        astrazeneca_count += vacc_count
                    elif vacc_name == 'Janssen':
                        janssen_count += vacc_count
                    elif vacc_name == 'Comirnaty':
                        comirnaty_count += vacc_count
                    else:
                        self.logger.info(f'unknown vaccine: {vacc_name}')
                index+=1
            dict = {'Moderna':moderna_count, 'AstraZeneca':astrazeneca_count, 'Janssen':janssen_count, 'Comirnaty':comirnaty_count}
            return dict
