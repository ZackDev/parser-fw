from Abstract import AbstractStep, StepError
from misc.Converters import str_to_integer
from io import StringIO
import csv


class VaccinationsByVaccineParser(AbstractStep):
    def run(self, data):
        dict = None
        with StringIO(data.decode('utf-8')) as vaccine_csv:
            csv_reader = csv.reader(vaccine_csv, delimiter=',')
            moderna_doses = 0
            astrazeneca_doses = 0
            janssen_doses = 0
            comirnaty_doses = 0

            ''' NOTE: the first line is the header '''
            index = 0
            for line in csv_reader:
                if index > 0:
                    vacc_name = line[2]
                    vacc_doses = line[4]
                    try:
                        vacc_doses = str_to_integer(vacc_doses, '+')
                    except Exception as e:
                        raise StepError('unexpected vlaue for vacc_doses.') from e
                    if vacc_name == 'Moderna':
                        moderna_doses += vacc_doses
                    elif vacc_name == 'AstraZeneca':
                        astrazeneca_doses += vacc_doses
                    elif vacc_name == 'Janssen':
                        janssen_doses += vacc_doses
                    elif vacc_name == 'Comirnaty':
                        comirnaty_doses += vacc_doses
                    else:
                        self.logger.info(f'unknown vaccine: {vacc_name}')
                index += 1
            dict = {'Moderna': moderna_doses, 'AstraZeneca': astrazeneca_doses, 'Janssen': janssen_doses, 'Comirnaty': comirnaty_doses}
        if dict is not None:
            return dict
        else:
            raise StepError('unexpected error: dict is None.')
