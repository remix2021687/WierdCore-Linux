if [ -z "$WAYLAND_DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
    clear
    echo "🚀 Запускаем WierdCore Linux..."
    exec Hyprland
fi
