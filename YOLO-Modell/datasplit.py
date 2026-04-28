
from pathlib import Path
import shutil
import random

# ------------------------------
# Konfiguration der Verzeichnisse
# ------------------------------
images_dir = Path('./data/images')   # Quellordner mit Bildern
labels_dir = Path('./data/labels')   # Quellordner mit YOLO-Labels (.txt)
output_dir = Path('./dataset')       # Zielordner für das gesplittete Dataset

# ------------------------------
# Zielstruktur anlegen
# ------------------------------
for split in ['train', 'val']:
    (output_dir / 'images' / split).mkdir(parents=True, exist_ok=True)
    (output_dir / 'labels' / split).mkdir(parents=True, exist_ok=True)

# ------------------------------
# Parameter für den Split
# ------------------------------
val_ratio = 0.2     # Anteil der Validierungsdaten (20%)
random_seed = 42    # Seed für Reproduzierbarkeit (gleicher Split bei erneutem Lauf)

random.seed(random_seed)

# ------------------------------
# Unterstützte Bild-Endungen definieren
# ------------------------------
image_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp'}

# ------------------------------
# Paare (Bild, Label) sammeln
# Nur Dateien verwenden, zu denen ein Label existiert.
# ------------------------------
pairs = []
for img_path in images_dir.iterdir():
    # Ist es eine Bilddatei mit unterstützter Endung?
    if img_path.is_file() and img_path.suffix.lower() in image_exts:
        # Label-Datei wird anhand des Basenamens gesucht: <stem>.txt
        lbl_path = labels_dir / (img_path.stem + '.txt')
        if lbl_path.exists():
            pairs.append((img_path, lbl_path))
        else:
            # Optional: Warnung ausgeben, wenn das Label fehlt
            print(f"Warnung: Kein Label für Bild {img_path.name} gefunden (erwartet: {lbl_path.name}).")

# Sicherstellen, dass überhaupt Paare vorhanden sind
if not pairs:
    raise RuntimeError("Es wurden keine (Bild, Label)-Paare gefunden. Prüfe deine Pfade und Dateinamen!")

# ------------------------------
# Zufälliger Split in train / val
# ------------------------------
random.shuffle(pairs)
val_count = int(len(pairs) * val_ratio)
val_pairs = pairs[:val_count]
train_pairs = pairs[val_count:]

print(f"Anzahl Gesamt-Paare: {len(pairs)}")
print(f"→ Train: {len(train_pairs)} | Val: {len(val_pairs)}")

# ------------------------------
# Dateien in die Zielstruktur kopieren
# ------------------------------
for split_name, plist in [('train', train_pairs), ('val', val_pairs)]:
    img_out_dir = output_dir / 'images' / split_name
    lbl_out_dir = output_dir / 'labels' / split_name
    for img_path, lbl_path in plist:
        # Bild kopieren
        shutil.copy2(img_path, img_out_dir / img_path.name)
        # Label kopieren
        shutil.copy2(lbl_path, lbl_out_dir / lbl_path.name)

print("Kopieren abgeschlossen. Die train/val-Struktur wurde erstellt.")
