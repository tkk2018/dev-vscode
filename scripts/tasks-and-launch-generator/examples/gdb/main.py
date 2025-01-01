#!/usr/bin/python3

import argparse
import json
from libs.jsonable import Jsonable
from libs.dictspec import DictSpec, KeySpec, ValueSpec
from libs.typecheck import TypeCheck
from libs.pathcheck import PathCheck
from libs.dictcheck import DictCheck
from libs.tasks import TaskGroup, TaskBuilder, Tasks

class GlobalConfiguration():
    KEYS = [
        DictSpec(key=KeySpec(name="CMAKE"), value=ValueSpec(value_type=str, validatable=PathCheck(isDiretory=False))),
        DictSpec(key=KeySpec(name="GDB"), value=ValueSpec(value_type=str, validatable=PathCheck(isDiretory=False))),
        DictSpec(key=KeySpec(name="GDBSERVER"), value=ValueSpec(value_type=str, validatable=PathCheck(isDiretory=False))),
        DictSpec(key=KeySpec(name="APP_NAME"), value=ValueSpec(value_type=str, validatable=TypeCheck(str))),
        DictSpec(key=KeySpec(name="OUT_DIR"), value=ValueSpec(value_type=str, validatable=TypeCheck(str))),
        DictSpec(key=KeySpec(name="SSH_HOST"), value=ValueSpec(value_type=str, validatable=TypeCheck(str ))),
        DictSpec(key=KeySpec(name="SSH_USER"), value=ValueSpec(value_type=str, validatable=TypeCheck(str ))),
        DictSpec(key=KeySpec(name="SSH_PWD"), value=ValueSpec(value_type=str, validatable=TypeCheck(str ))),
        DictSpec(key=KeySpec(name="REMOTE_APP_DIR"), value=ValueSpec(value_type=str, validatable=TypeCheck(str ))),
        DictSpec(key=KeySpec(name="REMOTE_GDBSERVER"), value=ValueSpec(value_type=str, validatable=TypeCheck(str ))),
    ]

    @staticmethod
    def load(file_path):
        # type: (str) -> GlobalConfiguration
        with open(file_path, "r") as file:
            data = json.load(file)

        check = DictCheck(GlobalConfiguration.KEYS)
        error = check.validate(data)
        if (error is not None):
            raise error

        CMAKE = data.get("CMAKE") # type: str
        GDB = data.get("GDB")
        GDBSERVER = data.get("GDBSERVER") # type: str
        APP_NAME = data.get("APP_NAME") # type: str
        OUT_DIR = data.get("OUT_DIR") # type: str
        SSH_HOST = data.get("SSH_HOST") # type: str
        SSH_USER = data.get("SSH_USER") # type: str
        SSH_PWD = data.get("SSH_PWD") # type: str
        REMOTE_APP_DIR = data.get("REMOTE_APP_DIR") # type: str
        REMOTE_GDBSERVER = data.get("REMOTE_GDBSERVER") # type: str

        return GlobalConfiguration(
            CMAKE,
            GDB,
            GDBSERVER,
            APP_NAME,
            OUT_DIR,
            SSH_HOST,
            SSH_USER,
            SSH_PWD,
            REMOTE_APP_DIR,
            REMOTE_GDBSERVER,
        )

    def __init__(self,
        CMAKE, # type: str
        GDB, # type:str
        GDBSERVER, # type:str
        APP_NAME, # type:str
        OUT_DIR, # type:str
        SSH_HOST, # type:str
        SSH_USER, # type:str
        SSH_PWD, # type:str
        REMOTE_APP_DIR, # type:str
        REMOTE_GDBSERVER, # type:str
    ):
        self.CMAKE = CMAKE
        self.GDB = GDB
        self.GDBSERVER = GDBSERVER
        self.APP_NAME = APP_NAME
        self.OUT_DIR = OUT_DIR
        self.SSH_HOST = SSH_HOST
        self.SSH_USER = SSH_USER
        self.SSH_PWD = SSH_PWD
        self.REMOTE_APP_DIR = REMOTE_APP_DIR
        self.REMOTE_GDBSERVER = REMOTE_GDBSERVER

class TaskFactory(object):
    def __init__(self, environment, configuration):
        # type: (str, GlobalConfiguration) -> TaskFactory
        self.config = configuration

        self.label_setup = "setup:"
        self.label_setup_gdbserver = self.label_setup + "gdbserver"

        self._label_prefix_ = environment + ":" if environment else ""

        self.label_build = self._label_prefix_ + "build"
        self.label_build_debug = self.label_build + ":debug"
        self.label_build_clean = self.label_build + ":clean"

        self.label_run = self._label_prefix_ + "run"
        self.label_run_app = self.label_run + ":app"
        self.label_run_gdbserver = self.label_run + ":gdbserver"

    def setup_gdbserver(self):
        builder = TaskBuilder(label= self.label_setup_gdbserver)
        (builder
            .command(r"${workspaceFolder}/scripts/sshpass.scp.sh")
            .args(r"--ssh-user").args(self.config.SSH_USER)
            .args(r"--ssh-host").args(self.config.SSH_HOST)
            .args(r"--ssh-pwd").args(self.config.SSH_PWD)
            .args(r"--file").args(self.config.GDBSERVER)
            .args(r"--dest").args(self.config.REMOTE_GDBSERVER)
            .type("shell")
            )

        return builder.build()

    def build(self):
        pass

    def build_debug(self):
        pass

    def build_clean(self):
        builder = TaskBuilder(label= self.label_build_clean)
        (builder
            .command(r"rm -rf ${workspaceFolder}/" + self.config.OUT_DIR)
            .type("shell")
            )
        return builder.build()

    def run_app(self):
            app = r"${workspaceFolder}" + "/" + self.config.OUT_DIR + "/" + self.config.APP_NAME
            remote_app = self.config.REMOTE_APP_DIR + "/" + self.config.APP_NAME
            builder = TaskBuilder(label= self.label_run_app)
            (builder
                .command(r"${workspaceFolder}/scripts/run.app.sh")
                .args(r"--ssh-user").args(self.config.SSH_USER)
                .args(r"--ssh-host").args(self.config.SSH_HOST)
                .args(r"--ssh-pwd").args(self.config.SSH_PWD)
                .args(r"--app").args(app)
                .args(r"--remote-app").args(remote_app)
                .type("shell")
                )
            return builder.build()

    def run_gdbserver(self):
            app = r"${workspaceFolder}" + "/" + self.config.OUT_DIR + "/" + self.config.APP_NAME
            remote_app = self.config.REMOTE_APP_DIR + "/" + self.config.APP_NAME
            builder = TaskBuilder(label= self.label_run_gdbserver)
            (builder
                .command(r"${workspaceFolder}/scripts/gdbserver.sh")
                .args(r"--ssh-user").args(self.config.SSH_USER)
                .args(r"--ssh-host").args(self.config.SSH_HOST)
                .args(r"--ssh-pwd").args(self.config.SSH_PWD)
                .args(r"--app").args(app)
                .args(r"--remote-app").args(remote_app)
                # .args(r"--gdbserver").args(self.config.GDBSERVER)
                .args(r"--remote-gdbserver").args(self.config.REMOTE_GDBSERVER)
                .args(r"--port").args("9091")
                .isBackground(True)
                .type("shell")
                .dependsOn(self.label_build_debug)
                )
            return builder.build()

class ProductionTaskFactory(TaskFactory):
    def __init__(self, configuration):
        # type: (GlobalConfiguration) -> ProductionTaskFactory
        super(ProductionTaskFactory, self).__init__("production", configuration)

    def build(self):
        builder = TaskBuilder(label= self.label_build)
        (builder
            .command(r"${workspaceFolder}/scripts/build.sh") # the application build script
            .type("shell")
            .group(TaskGroup(kind="build", isDefault=True))
            )
        return builder.build()

    def build_debug(self):
        builder = TaskBuilder(label= self.label_build_debug)
        (builder
            .command(r"${workspaceFolder}/scripts/build.sh") # the application build script
            .args(r"--debug") # with debug flag
            .type("shell")
            .group(TaskGroup(kind="build", isDefault=False))
            )
        return builder.build()

class Launch(Jsonable):
    def __init__(self, config, label):
        # type: (GlobalConfiguration, str) -> Launch
        self.version = "0.2.0"
        self.configurations = [{
            "name": "(gdb) Launch",
            "type": "cppdbg",
            "request": "launch",
            "program": r"${workspaceFolder}/" + config.OUT_DIR + "/" + config.APP_NAME,
            "miDebuggerServerAddress": config.SSH_HOST + ":9091",
            "args": [],
            "stopAtEntry": False,
            "cwd": r"${workspaceFolder}",
            "environment": [],
            "externalConsole": True,
            "targetArchitecture": "arm",
            "miDebuggerPath": config.GDB,
            "MIMode": "gdb",
            "setupCommands": [{
                "description": "Enable pretty-printing for gdb",
                "text": "-enable-pretty-printing",
                "ignoreFailures": True
            }],
            "preLaunchTask": label,
        }]

def write_file(content, file):
    with open(file, "w") as f:
        f.write(content)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="""\
    Set up development environment:
    - Copy the gdbserver to the remote machine.
    - Generate the tasks.json file.
    - Generate the launch.json file.

    Use the setup.template.json file as a guide to create your custom configuration file.
    Ensure that your configuration file follows the naming convention: setup.<name>.json.
    """,
    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--config", required=True, help="The configuration file.")

    # Parse arguments
    args = parser.parse_args()

    configuration = GlobalConfiguration.load(args.config)
    factory = ProductionTaskFactory(configuration)

    tasks = Tasks()
    tasks.tasks.append(factory.setup_gdbserver())

    tasks.tasks.append(factory.build())
    tasks.tasks.append(factory.build_debug())
    tasks.tasks.append(factory.build_clean())
    tasks.tasks.append(factory.run_app())
    run_gdbserver_task = factory.run_gdbserver()
    tasks.tasks.append(run_gdbserver_task)

    tasksjson = json.dumps(dict(tasks), sort_keys=True, indent=2)
    write_file(tasksjson, "./.vscode/tasks.json")

    launch = Launch(configuration, run_gdbserver_task.label)
    launchjson = json.dumps(dict(launch), sort_keys=True, indent=2)
    write_file(launchjson, "./.vscode/launch.json")
