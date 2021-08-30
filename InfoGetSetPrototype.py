import argparse
import logging
from Sequence import Sequence
from Sequence import SequenceRegister
from source.HTTPResponseSource import HTTPResponseSource
from parser.DailyCasesParser import DailyCasesParser
from parser.DailyVaccinationsParser import DailyVaccinationsParser
from parser.WeeklyTestsParser import WeeklyTestsParser
from parser.ICUOccupancyParser import ICUOccupancyParser
from parser.VaccinationsByVaccineParser import VaccinationsByVaccineParser
from sink.JSONFileSink import JSONFileSink

def init_sequences():
    source = HTTPResponseSource('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    parser = DailyCasesParser(source, 'Germany', False)
    sink = JSONFileSink(parser, 'corona_germany_daily_cases.json')
    Sequence(source, parser, sink, 'daily_cases')

    source = HTTPResponseSource('https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx?__blob=publicationFile')
    parser = DailyVaccinationsParser(source)
    sink = JSONFileSink(parser, 'corona_germany_daily_vaccinations.json')
    Sequence(source, parser, sink, 'daily_vaccinations')

    source = HTTPResponseSource('https://raw.githubusercontent.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland/master/Aktuell_Deutschland_Bundeslaender_COVID-19-Impfungen.csv')
    parser = VaccinationsByVaccineParser(source)
    sink= JSONFileSink(parser, 'corona_germany_vaccinations_by_vaccine.json')
    Sequence(source, parser, sink, 'vaccinations_by_vaccine')

    source = HTTPResponseSource('https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Testzahlen-gesamt.xlsx?__blob=publicationFile')
    parser = WeeklyTestsParser(source)
    sink = JSONFileSink(parser, 'corona_germany_weekly_tests.json')
    Sequence(source, parser, sink, 'weekly_tests')

    source = HTTPResponseSource('https://diviexchange.blob.core.windows.net/%24web/zeitreihe-tagesdaten.csv')
    parser = ICUOccupancyParser(source)
    sink = JSONFileSink(parser, 'corona_germany_daily_icuo.json')
    Sequence(source, parser, sink, 'daily_icuo')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--sequence", type=str)
    arg_parser.add_argument("-l", "--loglevel", type=int)
    args = arg_parser.parse_args()
    if (args.loglevel):
        loglevel = args.loglevel*10
        available_loglevels = [logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR, logging.CRITICAL]
        cnt = available_loglevels.count(loglevel)
        if cnt == 1:
            logging.basicConfig(filename='parser-fw.log', encoding='utf-8', level=loglevel, format='%(asctime)s %(name)s %(levelname)s : %(message)s')
            logger = logging.getLogger(__name__)
            logger.info(f'program started with loglevel: {loglevel}')
        else:
            print(f'provided loglevel not recognized.')
    else:
        arg_parser.print_help()
        exit(1)
    if (args.sequence):
        init_sequences()
        if SequenceRegister().has_sequence(args.sequence):
            SequenceRegister().get_sequence(args.sequence).run()
            exit(0)
        else:
            print(f'sequence {args.sequence} not found.')
            print('available sequences:')
            sequences = SequenceRegister().get_sequences()
            for seq in sequences:
                print(sequences[seq].sequence_name)
            exit(1)
    else:
        arg_parser.print_help()
        exit(1)
