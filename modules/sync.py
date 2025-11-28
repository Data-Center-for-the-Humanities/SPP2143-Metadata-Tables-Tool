def mirror_to_gitlab(local_folder, repo_url, target_subdir, token, branch="main"):
    """
    Spiegelt einen lokalen Ordner in einen Unterordner eines GitLab-Repos per temporärem Git-Repo.
    """
    # Token in HTTPS-URL einbetten
    if repo_url.startswith("https://"):
        repo_auth = repo_url.replace("https://", f"https://oauth2:{token}@")
    else:
        raise ValueError("Repo-URL muss mit 'https://' beginnen")

    # Prüfen, ob local_folder existiert und Dateien enthält
    if not os.path.exists(local_folder):
        print(f"Lokaler Ordner nicht gefunden: {local_folder}")
        return
    total_files = 0
    for _, _, files in os.walk(local_folder):
        total_files += len(files)
    print(f"Lokaler Ordner {local_folder} enthält {total_files} Dateien.")
    if total_files == 0:
        print("Keine Dateien zum Kopieren gefunden.")
        return

    # Temporären Arbeitsordner anlegen
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"🕐 Erstelle temporäres Arbeitsverzeichnis: {tmpdir}")

        # Repository klonen (nur den Zielbranch) und Ausgabe sammeln
        clone = subprocess.run(["git", "clone", "--branch", branch, "--depth", "1", repo_auth, tmpdir], capture_output=True, text=True)
        print("git clone stdout:")
        print(clone.stdout)
        if clone.returncode != 0:
            print("git clone failed:")
            print(clone.stderr)
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
            return

        msg = f"Auto sync {datetime.now():%Y-%m-%d %H:%M:%S}"
        commit = subprocess.run(["git", "commit", "-m", msg], cwd=tmpdir, capture_output=True, text=True)
        print("git commit stdout:")
        print(commit.stdout)
        print("git commit stderr:")
        print(commit.stderr)
        print(f"git commit returncode: {commit.returncode}")
        if commit.returncode != 0:
            print("Commit fehlgeschlagen — Abbruch.")
            return

        push = subprocess.run(["git", "push", "origin", branch], cwd=tmpdir, capture_output=True, text=True)
        print("git push stdout:")
        print(push.stdout)
        print("git push stderr:")
        print(push.stderr)
        print(f"git push returncode: {push.returncode}")
        if push.returncode != 0:
            print("Push fehlgeschlagen — Abbruch.")
            return

        # Remote HEAD prüfen (kurzer Check), um zu bestätigen, dass Remote den neuen Commit hat
        local_head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=tmpdir, capture_output=True, text=True)
        remote = subprocess.run(["git", "ls-remote", "origin", f"refs/heads/{branch}"], cwd=tmpdir, capture_output=True, text=True)
        print(f"Lokaler HEAD: {local_head.stdout.strip()}")
        print(f"Remote refs/heads/{branch}: {remote.stdout.strip()}")

        print("✅ Synchronisierung abgeschlossen.")

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