@echo off
echo Kopiranje...

mpremote resume cp msrgb565.py :msrgb565.py
mpremote resume cp sprite_data.py :sprite_data.py
mpremote resume cp lang_strings.py :lang_strings.py
mpremote resume cp main.py :main.py
mpremote resume cp boot.py :boot.py

mpremote resume cp alien.rgb565 :alien.rgb565
mpremote resume cp coin.rgb565 :coin.rgb565
mpremote resume cp cup.rgb565 :cup.rgb565
mpremote resume cp life.rgb565 :life.rgb565
mpremote resume cp life2times.rgb565 :life2times.rgb565

echo Kopirano! Samo napravi reset.