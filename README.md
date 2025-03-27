# MTT Readme

# **Dokumentation FAIR.rdm Metadata Tables Tool (MTT)**

## Metadataconverter from different repositories into ARIADNE Portal

*MTT Version 0.2 / Dokumentation Version 0.2 / Lukas Lammers / FAIR.rdm (P11) im SPP 2143 “Entangled Africa”*

### **1. Komponenten:**

**Main Script:** GUI mit TKinter, lädt Module und Daten je nach Bedarf

**/documentation:** Enthält diese Doku and andere Files zum Konzept des MTT.

**/geography:** Was war der Sinn dieses Ordners?

**/metadata_mirror:** Enthält die für ARIADNE bereitfestellten Metadaten in XML. Wird zu GitHub gespiegelt, von dort in jOAI und vor dort wiederrum in ARIADNE.

**/metadata_tables:** Enthält gesamte Projektdaten in tabellarischer Form.

**/registered_persons.xlsx:** Enthält alle Individuen und Institutionen, die in den Metadaten auftauchen. Neue Personen können direkt in der Tabelle oder mithilfe der GUI angelegt werden.

**/any_data_collection.xlsx:** Angelegtes Metadatentemplate eines Datensatzes. Kann WIP-tag versehen werden. Nur ohne WIP-tag werden diese Daten in XML konvertiert.

**/log.xlsx:** Erfasst sämtliche Änderungen der Daten und durchgeführte Konvertierungen. Dies ist keine Back-Up-Datei, sondern dient lediglich der Dokumentation der durchgeführten Arbeitsschritte.

**/modules:** Module werden nach Bedarf geladen.

**/repo_specific_modules.py:** Enthält Funktionen und Variablen, die nötig sind um Metadaten soweit wie möglich automatisch zu harvesten

**/config.py:** Enthält grundlegende Einstellungsparameter und Projektspezifische Konstanten

### **2. Features:**
