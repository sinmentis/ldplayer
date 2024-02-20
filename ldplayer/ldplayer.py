import subprocess


class LDPlayer:
    def __init__(self, ldconsole: str) -> None:
        self.__ldconsole = ldconsole

    def _run(self, cmd: list) -> tuple:
        process = subprocess.Popen([self.__ldconsole] + cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, err = process.communicate()
        return output.decode("utf-8"), err

    def list_instances(self) -> list:
        output, err = self._run(["list"])
        return output.split()

    def create(self, instance_name: str):
        output, err = self._run(["add", "--name", instance_name])
        if output != "":
            raise Exception(output)

    def launch(self, instance: str):
        if self.is_running(instance):
            raise Exception(f"{instance} is already running")
        command = ["launch"]
        if str(instance).isnumeric():
            command.extend(["--index", str(instance)])
        else:
            command.extend(["--name", instance])
        output, err = self._run(command)
        if output != "":
            raise Exception(output)

    def copy(self, instance_name: str, source: str):
        output, err = self._run(["copy", "--name", instance_name, "--from", str(source)])
        if output != "":
            raise Exception(output)

    def remove(self, instance: str):
        command = ["remove"]
        if str(instance).isnumeric():
            command.extend(["--index", str(instance)])
        else:
            command.extend(["--name", instance])
        output, err = self._run(command)
        if output != "":
            raise Exception(output)

    def quit(self, instance: str):
        command = ["quit"]
        if str(instance).isnumeric():
            command.extend(["--index", str(instance)])
        else:
            command.extend(["--name", instance])
        output, err = self._run(command)
        if output != "":
            raise Exception(output)

    def quitAll(self):
        output, err = self._run(["quitall"])
        if output != "":
            raise Exception(output)

    def reboot(self, instance: str):
        if not self.is_running(instance):
            raise Exception(f"{instance} not running")
        command = ["reboot"]
        if str(instance).isnumeric():
            command.extend(["--index", str(instance)])
        else:
            command.extend(["--name", instance])
        output, err = self._run(command)
        if output != "":
            raise Exception(output)

    def running_lists(self) -> list:
        command = ["runninglist"]
        output, err = self._run(command)
        return output.split()

    def is_running(self, instance: str) -> bool:
        command = ["isrunning"]
        if str(instance).isnumeric():
            command.extend(["--index", str(instance)])
        else:
            command.extend(["--name", instance])
        output, err = self._run(command)
        return output == "running"