import subprocess

"""
TODO:
8. install, uninstall, run and kill app
installapp <--name mnq_name | --index mnq_idx> --filename
installapp <--name mnq_name | --index mnq_idx> --packagename
uninstallapp <--name mnq_name | --index mnq_idx> --packagename
runapp <--name mnq_name | --index mnq_idx> --packagename
killapp <--name mnq_name | --index mnq_idx> --packagename

 

9. setprop/getprop/adb
setprop <--name mnq_name | --index mnq_idx> --key name --value val
getprop <--name mnq_name | --index mnq_idx> --key name

For example：

setprop --index 0 --key "phone.imei" --value "auto"
setprop --index 0 --key "phone.imsi" --value "auto"
setprop --index 0 --key "phone.simserial" --value "auto"
dnconsole.exe adb --name "LDPlayer" --command "shell pm list packages"
dnconsole.exe adb --index 0  --command "shell pm list packages"

 

10. list2
F:\changzhi\LDPlayer>dnconsole.exe list2
0,LDPlayer,2032678,1704928,1,7456,3500
1,LDPlayer-1,852422,590830,1,3772,3180
List2 returns multiple messages at one time, in turn:
index, title, top window handle, bind window handle, android started, pid, pid of vbox

4. property setting
modify <--name mnq_name | --index mnq_idx>
    [--resolution ]
    [--cpu <1 | 2 | 3 | 4>]
    [--memory <512 | 1024 | 2048 | 4096 | 8192>]
    [--manufacturer asus]
    [--model ASUS_Z00DUO]
    [--pnumber 13812345678]
    [--imei ]
    [--imsi ]    
    [--simserial ]
    [--androidid ]
    [--mac ]
    [--autorotate <1 | 0>]
    [--lockwindow <1 | 0>]

For example：
dnconsole.exe modify --index 0 --resolution 600,360,160 --cpu 1 --memory 1024 --imei auto

"""

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