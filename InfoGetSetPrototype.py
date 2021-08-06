import argparse
from Sequence import Sequence
from Sequence import SequenceRegister
from HTTPResponseSource import HTTPResponseSource
from DailyCasesParser import DailyCasesParser
from DailyVaccinationsParser import DailyVaccinationsParser
from WeeklyTestsParser import WeeklyTestsParser
from JSONFileSink import JSONFileSink

def init_sequences():
    source = HTTPResponseSource('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    parser = DailyCasesParser(source, False)
    sink = JSONFileSink(parser, 'corona_germany_daily_cases.json')
    Sequence(source, parser, sink, 'daily_cases')

    source = HTTPResponseSource('https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx?__blob=publicationFile')
    parser = DailyVaccinationsParser(source)
    sink = JSONFileSink(parser, 'corona_germany_daily_vaccinations.json')
    Sequence(source, parser, sink, 'daily_vaccinations')

    source = HTTPResponseSource('https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Testzahlen-gesamt.xlsx?__blob=publicationFile')
    parser = WeeklyTestsParser(source)
    sink = JSONFileSink(parser, 'corona_germany_weekly_tests.json')
    Sequence(source, parser, sink, 'weekly_tests')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", "--sequence", type=str)
    args = arg_parser.parse_args()
    if (args.sequence):
        init_sequences()
        if SequenceRegister().has_sequence(args.sequence):
            SequenceRegister().get_sequence(args.sequence).run()
            exit(0)
        else:
            print(f'sequence {args.sequence} not found.')
            exit(1)
    else:
        arg_parser.print_help()
        exit(1)
