from Abstract import AbstractStep, StepError
import json


class JSONFileSink(AbstractStep):
    def run(self, data):
        try:
            json_data = json.dumps(data)
        except Exception as e:
            raise StepError('error reading json from data.') from e

        if json_data is not None:
            try:
                with open(self.target, 'w') as file:
                    file.write(json_data)
            except Exception as e:
                raise StepError('error writing file.') from e
        else:
            raise StepError('JSONFileSink: json_data is None')
