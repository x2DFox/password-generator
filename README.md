# Password Generator

Минималистичная утилита с открытым исходным кодом для генерации стойких паролей. Надёжность заложена в сам принцип работы - вместо обычного ГПСЧ используется криптографически безопасный модуль.

![interface](https://github.com/x2DFox/PasswordGenerator/blob/main/resources/interface.png)

# Сборка

```Bash
pyinstaller --clean --noconsole --onedir --name password_generator --contents-directory library --icon icon.ico main.py
```
