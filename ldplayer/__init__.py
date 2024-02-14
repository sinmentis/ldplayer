import subprocess


class LDPlayer:
    
    
    __ldconsole: str
    
    
    def __init__(self, ldconsole: str) -> None:
        self.__ldconsole = ldconsole
        
        
    def instances(self) -> list:
        process = subprocess.Popen([self.__ldconsole, "list"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = process.communicate()
        output = output.decode("utf-8")
        return [ins for ins in output.split("\r\n") if ins != '']
    
    
    def create(self, instance_name: str) -> bool:
        process = subprocess.Popen([self.__ldconsole, "add", "--name", instance_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()
        return process.returncode == len(self.instances()) - 1
    
    
    def launch(self, instance: str) -> bool:
        command = [self.__ldconsole, "launch"]
        if str(instance).isnumeric():
            command.extend(["--index", str(instance)])
        else:
            command.extend(["--name", instance])
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()
        return process.returncode == 0
    
    
    def copy(self, instance_name: str, source: str) -> bool:
        before = len(self.instances())
        subprocess.Popen([self.__ldconsole, "copy", "--name", instance_name, "--from", str(source)])
        after = len(self.instances())
        return (before + 1) == after
    
    
    def remove(self, instance: str) -> bool:
        command = [self.__ldconsole, "remove"]
        if str(instance).isnumeric():
            command.extend(["--index", str(instance)])
        else:
            command.extend(["--name", instance])
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()
        return process.returncode == 0
    
    
    def quit(self, instance: str) -> bool:
        command = [self.__ldconsole, "quit"]
        if str(instance).isnumeric():
            command.extend(["--index", str(instance)])
        else:
            command.extend(["--name", instance])
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()
        return process.returncode == 0