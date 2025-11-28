# MTT Readme

# **Dokumentation des FAIR.rdm Metadata Tables Tool (MTT)**

## Metadataconverter from different repositories into ARIADNE Portal

*MTT Version 1.0 BETA / Dokumentation Version 0.4 / Lukas Lammers / FAIR.rdm (P11) im SPP 2143 “Entangled Africa” founded by the German Research Foundation (DFG)*

## 1. Funktion

Das Metadata Tables Tool, kurz MTT, wurde entwickelt, um die Dateneingabe in die ARIADNE Research Infrastructure (RI) zu unterstützen und Metadaten aus verschiedenen Repositorien im ARIADNE Portal zu publizieren. Hierzu bietet das MTT zwei grundlegende Funktionen: Erstens das semi-automatische Harvesten und Harmonisieren von Metadaten, zweitens die Konvertierung dieser Metadaten in den SPP-2143-Metadatenstandard.

## 2. Kontext

Das MTT wurde im Projekt FAIR.rdm im, von der Deutschen Forschungsgemeinschaft geförderten SPP 2143 “Entangled Africa” entwickelt. Neben FAIR.rdm arbeiten im SPP 2143 12 weitere Projekte, deren Forschungsdaten über zahlreiche Repositorien verteilt sind. Um die Forschungsdaten jedoch in ihrer Gesamtheit durchsuchen zu können, wurde eine Kooperation mit der ARIADNE RI hergestellt und ein Workflow entwickelt, wie eine Dateneingabe für den SPP 2143 funktionieren kann. Teil dessen ist ein SPP-interner Metadatenstandard, der mit jedem der bisher genutzten Repositorien kompatibel ist. Dennoch ist zur Harmonisierung der Metadaten ein nicht unerheblicher manueller Aufwand nötig. Deswegen wurde mit dem MTT ein Tool entwickelt, das diese Arbeit erleichtern soll.

Im SPP 2143 übernimmt die Bereitstellung der Metadaten das Data Center for the Humanities (DCH) der Universität zu Köln. Die vom MTT erzeugten XML-Metadaten werden in ein GitLab-Repositorium gespiegelt und von dort wiederum in eine mit jOAI aufgesetzte OAI-PMH-Schnittstelle. Dort können die Metadaten automatisch von ARIADNE abgerufen werden. In der RI selbst liegt ein Mapping vor, mit dem die Daten dann in ARIADNEs Datenmodell übertragen werden.

## 3. Installation und erste Ausführung

Das MTT ist eine Python Anwendung. Python kann hier heruntergeladen werden:

[https://www.python.org/](https://www.python.org/)

Außerdem werden einige Python-Bibliotheken benötigt. Diese können unter Windows im Terminal mit pip installiert werden:

`pip install pandas`

`pip install requests`

`pip install openpyxl`

Die Ordnerstruktur des MTT ist unbedingt einzuhalten. Es kann über das Terminal mit Python gestartet werden:

`python MTT_MainProgram.py`

Bestimmte Dinge im MTT müssen fallspezifisch angepasst werden. Mehr dazu im Folgenden Abschnitt (4. Anpassung).

## 4. Anpassung

Der Code des MTT ist nicht kompiliert, um maximale Anpassungsfähigkeit zu gewähren.

Als erstes müssen im Unterordner */modules* die Variablen in der mtt_config.py geändert werden. 

Standardmäßig spiegelt das MTT den Inhalt des Ordners metadata_mirror in ein Git-Repositorium. Dieses muss nach bei Bedarf erstellt oder ein alternativer Weg implementiert werden. In der ursprünglichen Disposition des Workflows mit dem MTT als Metadatenkonverter, werden die XML-Metadaten vom Git-Repo in die OAI-PMH-Schnittstelle gespiegelt. Andere Varianten des Datenflusses von metadata_mirror zu ARIADNE sind jedoch möglich und sollten von entsprechendem Fachpersonal umgesetzt werden können.

Mehr zu mtt_config.py in den Kompontenbeschreibungen.

Das Mapping eines Metadatenschemas eines Repositoriums erfolgt in Modulen, die mit “metadataimport_” beginnen. Die vorliegenden Module können als Beispiele und Entwicklungsgrundlagen verwendet werden. Grundlegende Python-Kenntnisse sind hierzu erforderlich.

Neue Module müssen in recognize_repository.py aufgenommen werden, damit sie von der Anwendung verwendet werden können.

Personen- und institutionsbezogene Daten werden in *metadata_tables/registered_persons.xlsx* eingetragen. Beim Ausfüllen des Metadatentemplates wird dann lediglich der Name benötigt, die restlichen Informationen werden aus dieser Tabelle abgefragt.

Eine Veränderung des zugrunde liegenden Datenschemas (dem SPP2143-Metadatenstandard) ist nicht unmöglich, erfordert jedoch Anpassungen in sämtlichen Modulen, inklusive der GUI.

## **5. Unterordner und ihre Komponenten:**

**Main Script:** GUI mit TKinter, lädt Module und Daten je nach Bedarf. Ausführen im CMD/Shell mit `python MTT_MainProgram.py`

**/documentation:** Enthält diese Doku, eine Beschreibung des SPP-2143-Metadatenstandards und eine Referenz des AO Cat, der in Gänze auch auf Zenodo zu finden ist.

**/metadata_mirror:** Enthält die für ARIADNE bereitgestellten Metadaten in XML. Wird zu GitLab gespiegelt, von dort in die OAI-PMH Schnittstelle (jOAI via DCH GitLab) und vor dort wiederrum in ARIADNE.

**/metadata_tables:** Enthält gesamte Projektdaten in tabellarischer Form. In diesem Ordner befinden sich außerdem die wichtigen Tabellen:

**/registered_persons.xlsx:** Enthält alle Individuen und Institutionen, die in den Metadaten auftauchen. Neue Personen können direkt in der Tabelle oder mithilfe der GUI angelegt werden.

**/log.xlsx** Logdatei über die Arbeitsschritte und Prozesse des MTT. Erfasst sämtliche Änderungen der Daten und durchgeführte Konvertierungen. Dies ist keine Back-Up-Datei, sondern dient lediglich der Dokumentation der durchgeführten Arbeitsschritte.

**/modules:** Module werden nach Bedarf geladen.

**/repo_specific_modules.py:** Enthält Funktionen und Variablen, die nötig sind um Metadaten soweit wie möglich automatisch zu harvesten. Können nach Bedarf angepasst werden.

**/recognize_repository.py**: Bestimmt anhand der angegebenen URI, welches Modul zum Harvesten der Daten benötigt wird. Muss bei neuen Modulen entsprechend angepasst werden.

**/mtt_config.py:** Enthält grundlegende Einstellungsparameter und Projektspezifische Konstanten.
1. Konstante Werte für Datenfelder, die allen Metadatensätzen feststehen. / 2. Eingaben zur Synchronisation mit einem Git-Repositorium / 3. Online-Ressourcen die im weiteren Verlauf des Workflows relevant sind

**/xml_conversion.py:** Dieses Modul führt die Konvertierung tabellarischer Metadaten in XML-Metadaten durch und speichert diese in metadata_mirror.

**/sync.py:** spiegelt den Inhalt des Ordner metadata_mirror in ein Git-Repo.  

**/wikidata_country_info.py:** Zu jeder Lokalisierung ist eine nähere Beschreibung in ARIADNE erforderlich. Diese wird mithilfe dieses Moduls aus Wikidata abgefragt. Wird diese Funktion nicht benötigt, kann das Modul deaktiviert werden.

**/menu/:** Enthält die GUI-Module und Funktionsaufrufe der oben genannten Module. 

**/change_dataset.py:** Ist das Fenster zum Ändern und Löschen von Datensätzen.

**/main_menu.py:** Ist das Hauptmenü

**/new_dataset.py:** Ist das Fenster zum Erstellen eines neuen Datensatzes

**/new_person_and_institution.py:** Ist das Menü zum Anlegen einer neuen Person oder Institution.

Außerdem enthält der Ordner die grafischen Elemente der Anwendung.

**/templates:** Enthält die Excel-Templates zur Eingabe der Metadaten. Derzeit stehen Collections und Individual Data Resources (IDR) zur Verfügung:

**/SPP2143_ARIADNE_Collection_Import_Template.xlsx:** Template für Collections. Collections können Teil von anderen Collections sein und beliebig vernestet werden.

**/SPP2143_ARIADNE_IDR_Import_Template.xlsx**: Template für IDRs. IDRs sind unteilbar. Sie sind Childs von Collections können aber selbst keine Parents sein.

## **6. Benutzeranleitung:**

### 6.1 Das Hauptmenü

Oben links befinden sich fünf Schaltflächen deren Funktionen weiter unten detailliert beschrieben werden:

- “New Person / Institution” unter 6.1
- “New Data Record” unter 6.2
- “Change Data Record” unter 6.3
- “Push to GitLab” unter 6.4
- “View Online Infrastructure” unter 6.5

Darunter befindet sich der “Data Selector”. Er gibt einen Überblick über bisher angelegte Datensätze. Die einzelnen Einträge lassen sich auswählen. Sie erscheinen dann rechts im “Data Viewer”.

Mit dem “Exit”-Button wird die Anwendung beendet. “Open Documentation” öffnet diese Dokumentation. “Open Configuration” öffnet die “mtt_config.py” in /modules.

### 6.1 Anlegen neuer Person/Institution

Der Button “New Person / Institution” öffnet ein neues Menü zum Anlegen einer neuen Person oder Institution.

Mit dem Radio-Button muss zwischen Person oder Institution gewählt werden.

Nur der Name ist ein Pflichtfeld. Siehe die SPP2143-Metadatenstandard-Dokumentation für nähere Feldbeschreibungen.

Wichtig ist, dass nur Personen einer Institution angehören können. Keine Institution kann in dieser Ontologie einer anderen Institution angehören.

“Save Entry” speichert den Eintrag. Er wird in der Tabelle “registered_persons.xlsx” gespeichert.

“Cancel without Saving” bricht den Vorgang ab und kehrt ohne zu speichern zum Hauptmenü zurück.

“Back” kann nach dem Speichern verwendet werden, um ins Hauptmenü zurück zu gelangen.

### 6.2 Anlegen eines neuen Metadatensatzes

Mit dem Button “New Data Record” lässt sich ein neuer Metadatensatz anlegen.

Zunächst öffnet sich ein kleines Dialogfenster und fordert die wichtigsten Daten vorab.

Der Typ der Ressource muss gewählt werden. Aktuell stehen Collections und IDRs zur Auswahl.

Der “Dataset Name” wird der interne Identifier für das MTT und ARIADNE. Er sollte einem klaren Benennungsschema folgen. Im SPP 2143 z.B. Projektnummer-Ressourcentyp-Laufnummer. Während der Eingabe werden ähnliche Namen von vorhandenen Datensätzen eingeblendet, um die Benennung zu erleichtern und doppelte Namen zu vermeiden.

Zuletzt muss die URI zum Datensatz eingetragen werden. Diese wird später verwendet, um Metadaten automatisch abzufragen und zu integrieren, gemäß dem jeweiligen Modul. Wird der Default-Wert “blank” beibehalten, wird ein leeres Template geladen.

Mit einem Klick auf “OK” öffnet sich das Menü zum Anlegen eines neuen Metadatensatzes. Alle zuvor eingegebenen Infos erscheinen im Data Viewer. Der Data Selector zeigt nun an, welche Angaben noch eingetragen werden müssen.

Der Button “Retrieve Data” aktiviert das Metadatenharvesting und fügt alle verfügbaren (natürlich zuvor im entsprechenden Modul gemappten) Metadaten ein.

Die Datenfelder lassen sich im Data Viewer auch manuell bearbeiten. Instruktionen dazu befinden sich unter dem Data Viewer.

“Save Progress” speichert alle Änderungen.

”Open with Excel” erlaubt die Bearbeitung direkt in Excel.

Wenn alle mit “mandatory” bezeichneten Felder ausgefüllt sind, kann der Datensatz mit “Convert to XML” in XML-Daten umgewandelt werden. Diese befinden sich dann im Ordner “metadata_mirror”.

Mit dem Button “Show XML” kann die soeben generierte XML-Datei geöffnet werden.

### 6.3 Ändern eines Metadatensatzes

Zum Ändern oder Löschen eines Metadatensatzes muss der entsprechende Datensatz im Data Selector ausgewählt werden. Nur dann öffnet sich das weiterführende Menü.

Der Button “Retrieve Data” aktiviert das Metadatenharvesting und fügt alle verfügbaren (natürlich zuvor im entsprechenden Modul gemappten) Metadaten ein.

Die Datenfelder lassen sich im Data Viewer auch manuell bearbeiten. Instruktionen dazu befinden sich unter dem Data Viewer.

“Save Progress” speichert alle Änderungen.

”Open with Excel” erlaubt die Bearbeitung direkt in Excel.

Wenn alle mit “mandatory” bezeichneten Felder ausgefüllt sind, kann der Datensatz mit “Convert to XML” in XML-Daten umgewandelt werden. Diese befinden sich dann im Ordner “metadata_mirror”.

Mit der Schaltfläche “Delete Dataset” kann ein Datensatz vollständig gelöscht werden.

### 6.4 Push to GitLab

Diese Schaltfläche löst eine Synchronisierung zwischen dem Ornder “metadata_mirror” und dem zugewiesenen Git-Repo aus. Im Git-Repo werden alle Datensätze neu hochgeladen, die neu erstellt oder geändert wurden. Einträge, die aus “metadata_mirror” entfernt wurden, werden auch im Git-Repo entfernt.

### 6.5 View Online Infrastructure

Der Knopf öffnet im Browser in der mtt_config.py vordefinierte URLs und verschafft einen Überblick über den weiteren Workflow. Dies können beispielsweise das Git-Repo sein, die OAI-PMH-Schnittstelle oder das ARIADNE-Portal.

## 7. Last Notes

Entwickelt von Lukas Lammers
Mitarbeiter im Data Center for the Humanities (DCH) der Universität zu Köln
im Projekt FAIR.rdm
teil des SPP 2143 “Entangled Africa”
gefördert von der Deutschen Forschungsgemeinschaft 2021-2026 (Projektnummer 467208261)

MIT License, Copyright (c) 2025 Lukas Lammers
