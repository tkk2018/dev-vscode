# Task to run gdbserver remotely

You will need the following things:
- The [gdbserver.sh](https://github.com/tkk2018/dev-linux/tree/main/sshpass) to start the gdbserver remotely as the `command` of the task.
- A task to build the application with debug enabled (optional). This can be set in the `dependsOn` of the task so that it will run every time before starting the gdbserver.
- The `isBackground` property set to `true` if using this task as the `preLaunchTask` of the `launch.json`.

The below is an example:

```json
{
  "tasks": [
    {
      "label": "build:debug",
      "command": "The command to build the application"
    },
    {
      "args": [
        "--ssh-user",
        "user",
        "--ssh-host",
        "192.168.8.100",
        "--ssh-pwd",
        "password",
        "--app",
        "${workspaceFolder}/BUILD/app",
        "--remote-app",
        "\\~/remote/path/to/app",
        "--remote-gdbserver",
        "\\~/remote/path/to/gdbserver",
        "--port",
        "9091"
      ],
      "command": "${workspaceFolder}/scripts/gdbserver.sh",
      "dependsOn": [
        "build:debug"
      ],
      "group": "none",
      "isBackground": true,
      "label": "run:gdbserver",
      "type": "shell"
    }
  ]
}
```
