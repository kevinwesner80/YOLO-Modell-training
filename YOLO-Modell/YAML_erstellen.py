from pathlib import Path
# ------------------------------
# Klassennamen definieren (ANPASSEN!)
# Die Reihenfolge bestimmt die Klassen-IDs (Index = ID).
# ------------------------------
classes = ["prohibitory",
            "danger",
            "mandatory",
            "other"]  # Beispiel; passe diese Liste an deine Klassen an!

# ------------------------------
# YAML-Inhalt zusammenstellen
# Der 'path' zeigt auf den Root des erzeugten Datasets (output_dir).
# ------------------------------
output_dir = Path('./dataset')

yaml_text = (
    f"path: {output_dir.as_posix()}\n"
    f"train: images/train\n"
    f"val: images/val\n"
    f"nc: {len(classes)}\n"
    f"names: {classes}\n"
)

# ------------------------------
# Datei schreiben
# ------------------------------
yaml_path = output_dir / 'dataset.yaml'
yaml_path.write_text(yaml_text, encoding='utf-8')

print("dataset.yaml geschrieben nach:", yaml_path)
print("--- Inhalt ---")
print(yaml_text)
