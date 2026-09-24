#!/data/data/com.termux/files/usr/bin/bash

# ╔══════════════════════════════════════════════╗
# ║               ⚡ HDB v1.0                   ║
# ║          High Dynamic Booster               ║
# ║             Termux + Shizuku                ║
# ║               Rish Engine                   ║
# ╚══════════════════════════════════════════════╝

export RISH_APPLICATION_ID="com.termux"

RISH="$(command -v rish)"

# ───────── SETTINGS ─────────

TARGET_FREE_MB=2560
INTERVAL=600

# ───────── ALWAYS PROTECTED ─────────

PROTECTED_APPS=(
    "com.termux"
    "moe.shizuku.privileged.api"
    "com.termux.api"
    "com.termux.widget"
    "com.termux.boot"
    "com.termux.tasker"
    "com.termux.styling"
    "com.termux.float"
    "com.android.systemui"
    "com.android.settings"
)

# ───────── STATE ─────────

PROTECTED_SELECTED=()
HDB_MODE=""

# ───────── RAM ─────────

get_ram() {
    awk '
        /MemAvailable:/ {
            printf "%.0f", $2 / 1024
            exit
        }
    ' /proc/meminfo 2>/dev/null
}

get_total_ram() {
    awk '
        /MemTotal:/ {
            printf "%.0f", $2 / 1024
            exit
        }
    ' /proc/meminfo 2>/dev/null
}

# ───────── PROTECTED CHECK ─────────

is_protected() {
    local app="$1"
    local p

    for p in "${PROTECTED_APPS[@]}"; do
        [ "$app" = "$p" ] && return 0
    done

    for p in "${PROTECTED_SELECTED[@]}"; do
        [ "$app" = "$p" ] && return 0
    done

    return 1
}

# ───────── PACKAGE CHECK ─────────

valid_package() {
    [[ "$1" =~ ^[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)+$ ]]
}

# ───────── USER APPS ─────────

get_apps() {
    "$RISH" -c 'pm list packages -3' 2>/dev/null |
        sed 's/^package://' |
        while IFS= read -r app; do

            [ -z "$app" ] && continue

            if ! is_protected "$app"; then
                printf '%s\n' "$app"
            fi

        done
}

# ───────── LOAD APPS ─────────

load_apps() {
    APPS=()

    while IFS= read -r app; do
        [ -n "$app" ] && APPS+=("$app")
    done < <(get_apps)
}

# ───────── SHOW APPS ─────────

show_apps() {

    load_apps

    echo
    echo "╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮"
    echo "┃          📱 USER APPS          ┃"
    echo "╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯"

    if [ "${#APPS[@]}" -eq 0 ]; then
        echo "❌ No user apps found."
        return 1
    fi

    local i

    for i in "${!APPS[@]}"; do
        printf "%3d) %s\n" "$((i + 1))" "${APPS[$i]}"
    done

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    return 0
}

# ───────── FORCE STOP ─────────

stop_app() {

    local app="$1"

    [ -z "$app" ] && return

    if is_protected "$app"; then
        printf "🛡️ %-42s PROTECTED\n" "$app"
        return 1
    fi

    if ! valid_package "$app"; then
        printf "❌ %-42s INVALID\n" "$app"
        return 1
    fi

    if "$RISH" -c "am force-stop --user 0 $app" >/dev/null 2>&1; then
        printf "🛑 %-42s STOPPED\n" "$app"
        return 0
    else
        printf "⚠️ %-42s FAILED\n" "$app"
        return 1
    fi
}

# ───────── HDB ENGINE ─────────

hdb_engine() {

    local before
    local current
    local total
    local stopped=0

    before="$(get_ram)"
    total="$(get_total_ram)"

    echo
    echo "╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮"
    echo "┃           ⚡ HDB ENGINE         ┃"
    echo "╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯"

    echo
    echo "🧠 RAM Free   : ${before:-?} MiB"
    echo "🎯 RAM Target : ${TARGET_FREE_MB} MiB"
    echo "💾 RAM Total  : ${total:-?} MiB"
    echo

    if [ -n "$before" ] && [ "$before" -ge "$TARGET_FREE_MB" ]; then
        echo "✅ RAM target already reached."
        return 0
    fi

    load_apps

    if [ "${#APPS[@]}" -eq 0 ]; then
        echo "❌ No user apps available."
        return 1
    fi

    echo "⚡ HDB scanning apps..."
    echo

    local app

    for app in "${APPS[@]}"; do

        current="$(get_ram)"

        if [ -n "$current" ] &&
           [ "$current" -ge "$TARGET_FREE_MB" ]; then

            echo
            echo "🎯 Target reached!"
            break
        fi

        if is_protected "$app"; then
            printf "🛡️ %-42s SKIPPED\n" "$app"
            continue
        fi

        if stop_app "$app"; then
            stopped=$((stopped + 1))
        fi

        sleep 0.25

    done

    current="$(get_ram)"

    echo
    echo "╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮"
    echo "┃           🧠 HDB REPORT         ┃"
    echo "╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯"

    echo "Before : ${before:-?} MiB"
    echo "After  : ${current:-?} MiB"
    echo "Target : ${TARGET_FREE_MB} MiB"
    echo "Stopped: $stopped"

    if [ -n "$current" ] && [ "$current" -ge "$TARGET_FREE_MB" ]; then
        echo "Status : ✅ TARGET REACHED"
    else
        echo "Status : ⚠️ TARGET NOT REACHED"
    fi

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# ───────── PROTECT SELECT ─────────

protect_apps() {

    show_apps || return 1

    echo
    echo "🛡️ PROTECT APPS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Example: 1,3,8"
    echo

    read -r -p "🛡️ Select For Protect: " NUMBERS

    PROTECTED_SELECTED=()

    IFS=',' read -ra LIST <<< "$NUMBERS"

    local n
    local index

    for n in "${LIST[@]}"; do

        n="${n// /}"

        if [[ "$n" =~ ^[0-9]+$ ]] &&
           [ "$n" -ge 1 ] &&
           [ "$n" -le "${#APPS[@]}" ]; then

            index=$((n - 1))

            PROTECTED_SELECTED+=("${APPS[$index]}")

        else
            echo "⚠️ Invalid number: $n"
        fi

    done

    echo
    echo "🛡️ Protected Apps:"

    if [ "${#PROTECTED_SELECTED[@]}" -eq 0 ]; then
        echo "❌ Nothing selected."
        return 1
    fi

    for app in "${PROTECTED_SELECTED[@]}"; do
        echo "   ✓ $app"
    done
}

# ───────── PROTECTED LIST ─────────

show_protected() {

    echo
    echo "╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮"
    echo "┃        🛡️ PROTECTED LIST       ┃"
    echo "╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯"

    echo
    echo "ALWAYS PROTECTED:"

    for app in "${PROTECTED_APPS[@]}"; do
        echo "   ✓ $app"
    done

    echo
    echo "USER PROTECTED:"

    if [ "${#PROTECTED_SELECTED[@]}" -eq 0 ]; then
        echo "   — None —"
    else
        for app in "${PROTECTED_SELECTED[@]}"; do
            echo "   ✓ $app"
        done
    fi

    echo
}

# ───────── MAIN ─────────

clear

echo "╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮"
echo "┃            ⚡ HDB v1.0         ┃"
echo "┃       High Dynamic Booster     ┃"
echo "┃          Rish + Shizuku        ┃"
echo "╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯"
echo

# ───────── RISH CHECK ─────────

if [ -z "$RISH" ]; then
    echo "❌ rish not found."
    echo
    echo "Check Shizuku + rish."
    exit 1
fi

# ───────── SHIZUKU CHECK ─────────

SHIZUKU_ID="$("$RISH" -c 'id' 2>/dev/null)"

if [ -z "$SHIZUKU_ID" ]; then
    echo "❌ Shizuku is not connected."
    echo
    echo "Test:"
    echo "RISH_APPLICATION_ID=com.termux rish -c 'id'"
    exit 1
fi

echo "✅ Shizuku : Connected"
echo "👤 $SHIZUKU_ID"
echo

# ───────── MENU ─────────

echo "01) 🛡️ Protect Apps"
echo "02) 🚀 Start HDB"
echo "03) 🛡️ Protected List"
echo "04) 📊 RAM Status"
echo "99) ❌ Exit"
echo

read -r -p "Select: " CHOICE

case "$CHOICE" in

    01)

        protect_apps || exit 1

        echo
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🛡️ Protected apps configured."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ;;

    02)

        HDB_MODE="auto"

        while true; do

            hdb_engine

            echo
            echo "💤 Sleeping for 10 minutes..."
            echo "⏱️ Next HDB cycle: ${INTERVAL} seconds"
            echo

            sleep "$INTERVAL"

        done
        ;;

    03)

        show_protected
        ;;

    04)

        RAM="$(get_ram)"
        TOTAL="$(get_total_ram)"

        echo
        echo "🧠 RAM Free  : ${RAM:-?} MiB"
        echo "💾 RAM Total : ${TOTAL:-?} MiB"
        echo "🎯 HDB Target: ${TARGET_FREE_MB} MiB"
        ;;

    99)

        exit 0
        ;;

    *)

        echo "❌ Invalid selection."
        exit 1
        ;;

esac

نصب به‌عنوان Shortcut

mkdir -p ~/.shortcuts

nano ~/.shortcuts/HDB

کد بالا را Paste کن، ذخیره کن و بعد:

chmod +x ~/.shortcuts/HDB

برای تست مستقیم:

~/.shortcuts/HDB

اگر از Termux:Widget استفاده می‌کنی، "HDB" باید در لیست Shortcutها ظاهر شود.

نکته: این نسخه برنامه‌های سیستمی را دستکاری نمی‌کند و "Termux" و "Shizuku" همیشه Protected هستند. همچنین هدف "2560 MiB" است؛ اگر سیستم نتواند واقعاً این مقدار RAM آزاد ایجاد کند، HDB بی‌نهایت برنامه را متوقف نمی‌کند و در پایان "TARGET NOT REACHED" نشان می‌دهد.