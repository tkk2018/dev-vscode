# Start debugging with remote gdbserver

The `preLaunchTask` is optional. It uses to start the remote gdbserver. The `run:gdbserver` task is available at [here](https://github.com/tkk2018/dev-vscode/blob/main/tasks.json/gdbserver.md).

```json
{
  "configurations": [
    {
      "MIMode": "gdb",
      "args": [],
      "cwd": "${workspaceFolder}",
      "environment": [],
      "externalConsole": true,
      "miDebuggerPath": "/local/path/to/toolchain/cross-compiler/arm-linux-gnueabihf-gdb",
      "miDebuggerServerAddress": "192.168.8.100:9091",
      "name": "(gdb) Launch",
      "preLaunchTask": "run:gdbserver",
      "program": "${workspaceFolder}/BUILD/app",
      "request": "launch",
      "setupCommands": [
        {
          "description": "Enable pretty-printing for gdb",
          "ignoreFailures": true,
          "text": "-enable-pretty-printing"
        }
      ],
      "stopAtEntry": false,
      "targetArchitecture": "arm",
      "type": "cppdbg"
    }
  ],
  "version": "0.2.0"
}
```
