Set oShell = CreateObject("Wscript.Shell")
Dim strArgs
strArgs = "cmd /c news_launcher.bat"
oShell.Run strArgs, 0, False