def process_xml_relationships(local_folder, target_path, xml_extension=".xml"):
    """
    Verarbeitet XML-Dateien und erstellt gegenseitige dct:isPartOf / dct:hasPart Beziehungen.
    
    Wenn eine Datei einen dct:isPartOf Tag enthält:
    1. Wird die dort genannte Datei geladen (ohne Endung im Tag)
    2. Wird der ursprünglichen Datei ein dct:hasPart Tag hinzugefügt (auch ohne Endung)
    3. dct:hasPart wird auf der gleichen Ebene wie dct:isPartOf eingefügt
    4. Änderungen werden sowohl im local_folder als auch in target_path vorgenommen
    
    Beispiel:
    - Datei A.xml (dct:isPartOf="B") → Datei B.xml wird geladen
    - Datei B.xml erhält: dct:hasPart="A" neben anderen dct:* Tags
    """
    import xml.etree.ElementTree as ET
    
    # Finde alle XML-Dateien (Map: Dateiname ohne Ext -> Dateipfad)
    xml_files_local = {}
    xml_files_target = {}
    file_to_basename = {}
    
    # Local folder
    for root, _, files in os.walk(local_folder):
        for file_name in files:
            if file_name.endswith(xml_extension):
                file_path = os.path.join(root, file_name)
                basename_no_ext = os.path.splitext(file_name)[0]
                xml_files_local[basename_no_ext] = file_path
                file_to_basename[basename_no_ext] = file_name
    
    # Target path (Repo)
    for root, _, files in os.walk(target_path):
        for file_name in files:
            if file_name.endswith(xml_extension):
                file_path = os.path.join(root, file_name)
                basename_no_ext = os.path.splitext(file_name)[0]
                xml_files_target[basename_no_ext] = file_path
    
    if not xml_files_local and not xml_files_target:
        print(f"Keine XML-Dateien gefunden.")
        return
    
    print(f"🔗 Verarbeite XML-Dateien für dct:isPartOf/dct:hasPart Beziehungen...")
    
    # Namespaces definieren und registrieren
    namespaces = {
        'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
        'crm':'http://www.cidoc-crm.org/cidoc-crm/',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'dct': 'http://purl.org/dc/terms/',
        'foaf': 'http://xmlns.com/foaf/0.1/',
        'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
        'dch': 'http://oai.dch.phil-fak.uni-koeln.de/',
        'owl': 'http://www.w3.org/2002/07/owl#',
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'
    }
    
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)
    
    # Verarbeite Dateien aus local_folder
    for basename_no_ext, file_path in xml_files_local.items():
        try:
            tree = ET.parse(file_path)
            root_elem = tree.getroot()
            
            # Finde den oai_dc:dc Element
            oai_dc_ns = namespaces['oai_dc']
            dc_elem = root_elem.find(f'{{{oai_dc_ns}}}dc')
            if dc_elem is None:
                dc_elem = root_elem
            
            # Suche dct:isPartOf Tags
            dct_ns = namespaces['dct']
            is_part_of_elems = dc_elem.findall(f'{{{dct_ns}}}isPartOf')
            
            if is_part_of_elems:
                for is_part_of_elem in is_part_of_elems:
                    referenced_basename_no_ext = None
                    
                    if is_part_of_elem.text and is_part_of_elem.text.strip():
                        referenced_basename_no_ext = is_part_of_elem.text.strip()
                    elif '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource' in is_part_of_elem.attrib:
                        referenced_basename_no_ext = is_part_of_elem.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']
                    
                    if referenced_basename_no_ext and referenced_basename_no_ext in xml_files_local:
                        print(f"  ✓ {basename_no_ext} ist Teil von {referenced_basename_no_ext}")
                        
                        # Verarbeite beide Orte: local_folder und target_path
                        for file_dict in [xml_files_local, xml_files_target]:
                            if referenced_basename_no_ext not in file_dict:
                                continue
                            
                            ref_file_path = file_dict[referenced_basename_no_ext]
                            try:
                                ref_tree = ET.parse(ref_file_path)
                                ref_root = ref_tree.getroot()
                                
                                ref_dc_elem = ref_root.find(f'{{{oai_dc_ns}}}dc')
                                if ref_dc_elem is None:
                                    ref_dc_elem = ref_root
                                
                                # Prüfe, ob dct:hasPart bereits existiert
                                existing_has_part = ref_dc_elem.findall(f'{{{dct_ns}}}hasPart')
                                has_existing = False
                                
                                for has_part_elem in existing_has_part:
                                    has_part_text = has_part_elem.text or has_part_elem.attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', '')
                                    if has_part_text == basename_no_ext:
                                        has_existing = True
                                        break
                                
                                if not has_existing:
                                    # Erstelle neuen dct:hasPart Tag direkt nach dct:isPartOf
                                    new_has_part = ET.Element(f'{{{dct_ns}}}hasPart')
                                    
                                    # Kopiere Struktur von dct:isPartOf
                                    if is_part_of_elem.text:
                                        new_has_part.text = basename_no_ext
                                    else:
                                        new_has_part.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'] = basename_no_ext
                                    
                                    # Finde die Position von dct:isPartOf und füge danach ein
                                    # Oder am Ende der dct: Tags
                                    is_part_of_index = None
                                    for idx, child in enumerate(ref_dc_elem):
                                        if child.tag == f'{{{dct_ns}}}isPartOf':
                                            is_part_of_index = idx
                                            break
                                    
                                    if is_part_of_index is not None:
                                        ref_dc_elem.insert(is_part_of_index + 1, new_has_part)
                                    else:
                                        ref_dc_elem.append(new_has_part)
                                    
                                    ref_tree.write(ref_file_path, encoding='utf-8', xml_declaration=True)
                                    
                                    location = "local" if file_dict == xml_files_local else "repo"
                                    print(f"    ➜ Hinzugefügt: dct:hasPart '{basename_no_ext}' zu {referenced_basename_no_ext} ({location})")
                            
                            except ET.ParseError as e:
                                print(f"    ❌ Fehler beim Parsen von {referenced_basename_no_ext}: {e}")
        
        except ET.ParseError as e:
            print(f"⚠️ Fehler beim Parsen von {file_path}: {e}")
        except Exception as e:
            print(f"⚠️ Fehler bei der Verarbeitung von {basename_no_ext}: {e}")


def mirror_to_gitlab(local_folder, repo_url, target_subdir, token, branch="main"):
    """
    Spiegelt einen lokalen Ordner in einen Unterordner eines GitLab-Repos per temporärem Git-Repo.
    Bearbeitet XML-Dateien und erstellt gegenseitige dct:isPartOf/dct:hasPart Beziehungen.
    """
    import tkinter as tk
    
    # Statusfenster erstellen
    status_window = tk.Tk()
    status_window.title("Synchronisierung")
    status_window.geometry("400x100")
    status_label = tk.Label(status_window, text="🚀 Synchronisierung wird gestartet...", font=("Arial", 12), pady=20)
    status_label.pack()
    status_window.update()
    
    # Token in HTTPS-URL einbetten
    if repo_url.startswith("https://"):
        repo_auth = repo_url.replace("https://", f"https://oauth2:{token}@")
    else:
        status_label.config(text="❌ Fehler: Repo-URL muss mit 'https://' beginnen")
        status_window.update()
        status_window.after(5000, status_window.destroy)
        status_window.mainloop()
        raise ValueError("Repo-URL muss mit 'https://' beginnen")

    # Prüfen, ob local_folder existiert und Dateien enthält
    if not os.path.exists(local_folder):
        print(f"Lokaler Ordner nicht gefunden: {local_folder}")
        status_label.config(text=f"❌ Lokaler Ordner nicht gefunden: {local_folder}")
        status_window.update()
        status_window.after(5000, status_window.destroy)
        status_window.mainloop()
        return
    total_files = 0
    for _, _, files in os.walk(local_folder):
        total_files += len(files)
    print(f"Lokaler Ordner {local_folder} enthält {total_files} Dateien.")
    if total_files == 0:
        print("Keine Dateien zum Kopieren gefunden.")
        status_label.config(text="⚠️ Keine Dateien zum Kopieren gefunden")
        status_window.update()
        status_window.after(5000, status_window.destroy)
        status_window.mainloop()
        return

    # Temporären Arbeitsordner anlegen
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"🕐 Erstelle temporäres Arbeitsverzeichnis: {tmpdir}")
        status_label.config(text="🕐 Erstelle temporäres Arbeitsverzeichnis...")
        status_window.update()

        # Repository klonen (nur den Zielbranch) und Ausgabe sammeln
        status_label.config(text="📥 Repository wird geklont...")
        status_window.update()
        clone = subprocess.run(["git", "clone", "--branch", branch, "--depth", "1", repo_auth, tmpdir], capture_output=True, text=True)
        print("git clone stdout:")
        print(clone.stdout)
        if clone.returncode != 0:
            print("git clone failed:")
            print(clone.stderr)
            status_label.config(text="❌ Git clone fehlgeschlagen")
            status_window.update()
            status_window.after(5000, status_window.destroy)
            status_window.mainloop()
            raise RuntimeError("git clone failed")

        # Zielordner im Repo bestimmen
        target_path = os.path.join(tmpdir, target_subdir)
        os.makedirs(target_path, exist_ok=True)

        # Liste der Dateien im Repo (vor Änderungen) ausgeben
        ls_before = subprocess.run(["git", "ls-files"], cwd=tmpdir, capture_output=True, text=True)
        repo_files_before = ls_before.stdout.splitlines()
        print(f"Anzahl getrackter Dateien im Repo (vorher): {len(repo_files_before)}")
        print("Beispiele (vorher):", repo_files_before[:10])

        # Inhalt aus local_folder dorthin kopieren
        status_label.config(text="📂 Dateien werden kopiert...")
        status_window.update()
        copied_files = []
        source_rel_paths = set()
        for root, _, files in os.walk(local_folder):
            rel_root = os.path.relpath(root, local_folder)
            if rel_root == '.':
                rel_root = ''
            for file_name in files:
                src_file = os.path.join(root, file_name)
                rel_path = os.path.normpath(os.path.join(rel_root, file_name))
                source_rel_paths.add(rel_path)
                dest_file = os.path.join(target_path, rel_path)
                dest_dir = os.path.dirname(dest_file)
                os.makedirs(dest_dir, exist_ok=True)
                shutil.copy2(src_file, dest_file)
                copied_files.append(dest_file)

        print(f"Kopiert {len(copied_files)} Dateien nach {target_path} (Beispiele: {copied_files[:5] if copied_files else []})")

        # --- Bearbeite XML-Dateien für gegenseitige dct:isPartOf/dct:hasPart Beziehungen ---
        status_label.config(text="🔗 XML-Beziehungen werden verarbeitet...")
        status_window.update()
        process_xml_relationships(local_folder, target_path)

        # --- Synchronisation: entferne Dateien im Repo, die nicht mehr in source vorhanden sind ---
        repo_rel_paths = set()
        for root, _, files in os.walk(target_path):
            rel_root = os.path.relpath(root, target_path)
            if rel_root == '.':
                rel_root = ''
            for file_name in files:
                rel_path = os.path.normpath(os.path.join(rel_root, file_name))
                repo_rel_paths.add(rel_path)

        to_remove = sorted(repo_rel_paths - source_rel_paths)
        print(f"Gefundene veraltete Pfade (rel): {to_remove[:20]}{'...' if len(to_remove)>20 else ''}")
        removed = []
        for rel_path in to_remove:
            full = os.path.join(target_path, rel_path)
            try:
                os.remove(full)
                removed.append(full)
            except IsADirectoryError:
                # should not happen as we iterate files, but handle defensively
                shutil.rmtree(full, ignore_errors=True)
                removed.append(full)
        # Remove empty directories in repo target_path
        for root, dirs, files in os.walk(target_path, topdown=False):
            if not dirs and not files:
                try:
                    os.rmdir(root)
                except OSError:
                    pass

        print(f"Entfernt {len(removed)} veraltete Dateien aus dem Repo (Beispiele: {removed[:5] if removed else []})")

        # Liste der Dateien im Repo (nach Entfernen) ausgeben
        ls_after = subprocess.run(["git", "ls-files"], cwd=tmpdir, capture_output=True, text=True)
        repo_files_after = ls_after.stdout.splitlines()
        print(f"Anzahl getrackter Dateien im Repo (nachher): {len(repo_files_after)}")
        print("Beispiele (nachher):", repo_files_after[:10])

        # Lokalen Git-User konfigurieren (nur für dieses Repo), damit Commit nicht fehlschlägt
        subprocess.run(["git", "config", "user.email", "autosync@example.com"], cwd=tmpdir, check=True)
        subprocess.run(["git", "config", "user.name", "Auto Sync Bot"], cwd=tmpdir, check=True)

        # Git-Befehle ausführen (ohne das Arbeitsverzeichnis global zu wechseln), Ausgabe sammeln
        add = subprocess.run(["git", "add", "--all"], cwd=tmpdir, capture_output=True, text=True)
        print("git add stdout:")
        print(add.stdout)
        print("git add stderr:")
        print(add.stderr)

        # Zeige, was gestaged wurde (z. B. D <path> für deletions)
        staged = subprocess.run(["git", "status", "--porcelain"], cwd=tmpdir, capture_output=True, text=True)
        print("git status --porcelain (nach add):")
        print(staged.stdout)

        result = subprocess.run(["git", "status", "--porcelain"], cwd=tmpdir, capture_output=True, text=True)
        print("git status --porcelain output:")
        print(result.stdout)
        if not result.stdout.strip():
            print("Keine Änderungen zum Commit gefunden.")
            status_label.config(text="ℹ️ Keine Änderungen zum Commit gefunden")
            status_window.update()
            status_window.after(5000, status_window.destroy)
            status_window.mainloop()
            return

        msg = f"Auto sync {datetime.now():%Y-%m-%d %H:%M:%S}"
        status_label.config(text="💾 Änderungen werden committet...")
        status_window.update()
        commit = subprocess.run(["git", "commit", "-m", msg], cwd=tmpdir, capture_output=True, text=True)
        print("git commit stdout:")
        print(commit.stdout)
        print("git commit stderr:")
        print(commit.stderr)
        print(f"git commit returncode: {commit.returncode}")
        if commit.returncode != 0:
            print("Commit fehlgeschlagen — Abbruch.")
            status_label.config(text="❌ Commit fehlgeschlagen")
            status_window.update()
            status_window.after(5000, status_window.destroy)
            status_window.mainloop()
            return

        status_label.config(text="📤 Änderungen werden gepusht...")
        status_window.update()
        push = subprocess.run(["git", "push", "origin", branch], cwd=tmpdir, capture_output=True, text=True)
        print("git push stdout:")
        print(push.stdout)
        print("git push stderr:")
        print(push.stderr)
        print(f"git push returncode: {push.returncode}")
        if push.returncode != 0:
            print("Push fehlgeschlagen — Abbruch.")
            status_label.config(text="❌ Push fehlgeschlagen")
            status_window.update()
            status_window.after(5000, status_window.destroy)
            status_window.mainloop()
            return

        # Remote HEAD prüfen (kurzer Check), um zu bestätigen, dass Remote den neuen Commit hat
        local_head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=tmpdir, capture_output=True, text=True)
        remote = subprocess.run(["git", "ls-remote", "origin", f"refs/heads/{branch}"], cwd=tmpdir, capture_output=True, text=True)
        print(f"Lokaler HEAD: {local_head.stdout.strip()}")
        print(f"Remote refs/heads/{branch}: {remote.stdout.strip()}")

        # Statusfenster aktualisieren und nach kurzer Zeit schließen
        status_label.config(text="✅ Synchronisierung erfolgreich abgeschlossen!")
        status_window.update()
        status_window.after(3000, status_window.destroy)  # Schließt nach 3 Sekunden
        status_window.mainloop()

if __name__ == "__main__":
    import os
    import shutil
    import subprocess
    import tempfile
    from datetime import datetime
            
    # Beispielaufruf
    local_folder = r"/metadata_mirror/"
    repo_url = "https://gitlab.git"
    target_subdir = "test_metadata"
    token = "token_with_maintainer_read_and_write_rights"  # Ersetzen durch echten Token
    mirror_to_gitlab(local_folder, repo_url, target_subdir, token)
else:
    import os
    import shutil
    import subprocess
    import tempfile
    from datetime import datetime
    import xml.etree.ElementTree as ET
