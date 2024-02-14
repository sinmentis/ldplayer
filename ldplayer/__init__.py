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
        return process.returncode == len(self.instances()) - 1
    
    
    def launch(self, instance_name: str | None = None, instance_index: int | None = None) -> bool:
        if instance_name == None and instance_index == None:
            raise ValueError("This method requires an instance name or instance index.")
        command = [self.__ldconsole, "launch"]
        if instance_name is not None:
            command.extend(["--name", instance_name])
        else:
            command.extend(["--index", str(instance_index)])
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process.returncode == 0
    
    
    def copy(self, instance_name: str, source: str):
        pass