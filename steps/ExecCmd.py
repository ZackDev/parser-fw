from Abstract import AbstractStep, StepError
import os


class ExecCmd(AbstractStep):
    def run(self, data):
        pexists = os.path.exists(self.path)
        if pexists is True:
            os.system(f'cd {self.path}')
            for cmd in self.cmds:
                os.system(cmd)
        else:
            raise StepError(f'path: {self.path} not found')
