from Abstract import AbstractStep, StepError
from misc.Converters import str_to_integer
from io import StringIO
import csv


class VaccinationsByVaccineParser(AbstractStep):
    def run(self, data):
        dict = {}
        with StringIO(data.decode('utf-8')) as vaccine_csv:
            csv_reader = csv.reader(vaccine_csv, delimiter=',')

            ''' NOTE: the first line is the header '''
            ''' reads name of vaccine and administered doses line by line '''
            ''' adds vaccine and doses to dict if vaccine_name not present in dict '''
            ''' else: updates dict's vaccine_name doses count with count from dict plus count from current line '''
            index = 0
            for line in csv_reader:
                if index < 1:
                    index += 1
                    pass
                else:
                    vacc_name = line[2]
                    vacc_doses = line[4]
                    try:
                        vacc_doses = str_to_integer(vacc_doses, '+')
                    except Exception as e:
                        raise StepError('unexpected value for vacc_doses.') from e
                    try:
                        doses = dict[vacc_name]
                        dict.update({vacc_name: doses + vacc_doses})
                    except KeyError:
                        dict.update({vacc_name: vacc_doses})
        if len(dict) > 0:
            return dict
        else:
            raise StepError('unexpected error: dict is empty.')
