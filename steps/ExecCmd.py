from Abstract import AbstractStep, StepError
import os


class ExecCmd(AbstractStep):
    def run(self, data):
        # get current working directory
        cwd = os.getcwd()
        if os.path.exists(self.path) is True:
            # change directory, run commands
            os.chdir(self.path)
            for cmd in self.cmds:
                os.system(cmd)
            # change directory back to cwd
            os.chdir(cwd)
        else:
            raise StepError(f'path: {self.path} not found')
