if [[ "$(tty)" == "/dev/tty1" ]]; then
    # Небольшая пауза, чтобы логи загрузки не перекрыли старт скрипта
    sleep 2
    clear
    
    # Запускаем твой Python-скрипт без буферизации
    python3 -u /usr/local/bin/install.py
fi
