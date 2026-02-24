# ModernWiki

Ein minimalistisches Wiki-System, das Git-Repositories als Datenbank und Markdown als Formatierungssprache verwendet.

Das Wesen eines Wikis ist Versionskontrolle und Open-Source-Kollaboration. Die Verwendung des ausgereiften Git-Systems ermöglicht eine bessere Verwaltung von Vandalismus, und Markdown ist zudem einfacher zu bearbeiten.

## Schnellstart

## 1. Inhalts-Repository erstellen

Das Inhalts-Repository ist das Seiten-Repository des Wikis, das Benutzern zur freien Bearbeitung zur Verfügung steht. Bitte verwenden Sie das Repository [ModernWikiTemplate](https://github.com/Heerozh/ModernWikiTemplate.git) als Vorlage. Das Repository hat das Hugo-Projektformat, Sie können das Website-Design darin beliebig anpassen.

### **GitHub:**

Forken Sie direkt [ModernWikiTemplate](https://github.com/Heerozh/ModernWikiTemplate.git).
Unterstützt auch Gitee, GitLab.

### **(Empfohlen) Privates Git-Repository:**

Zunächst überspringen, nach dem Start des Systems zurückkehren und einrichten:

Besuchen Sie <http://localhost/git>, klicken Sie direkt auf "Install Gitea (Jetzt installieren)", registrieren Sie einen Admin-Account, klicken Sie oben rechts auf ➕, wählen Sie "migrate (Externes Repository migrieren)",
klonen Sie <https://github.com/Heerozh/ModernWikiTemplate.git>
und benennen Sie es in "Wiki" um.

> Achten Sie darauf, die Repository-Berechtigungen so zu öffnen, dass alle Push-Zugriff haben, andernfalls ist eine PR-Überprüfung erforderlich. Wenn nur das Content-Verzeichnis Push-fähig sein soll, während Site-Konfiguration und Stil-Dateien per PR eingereicht werden müssen, können Sie Git-Submodule verwenden und dies mit 2 verschiedenen Repositories umsetzen.

## 2. Umgebungsvariablen konfigurieren

Kopieren Sie die Umgebungsvariablen-Vorlage:

```bash
cp .env.example .env
```

Bearbeiten Sie die `.env`-Datei und setzen Sie Ihr Git-Repository:

```bash
GIT_REPO=https:/domain.com/your-username/your-wiki-content.git
GIT_BRANCH=master
DOMAIN=:80 # Für lokale Tests kann nur :80 verwendet werden, sonst ist kein Zugriff möglich
```

> [!NOTE]
> Nach jeder Änderung an `.env` muss das Image neu gebaut werden: `docker compose build`

## 3. System starten

Installieren Sie zuerst Docker Engine und das docker-compose-plugin, dann:

```bash
# Dienste starten (Externes Git-Hosting)
docker compose up -d

# Dienste starten (Lokales Gitea-Hosting)
docker compose --profile with-gitea up -d
```

## 4. Wiki aufrufen

- Hauptsite: <http://localhost>
- Webhook-Endpunkt: <http://localhost/webhook>
- Lokales Gitea-Repository (falls aktiviert): <http://localhost/git/>

## 5. Automatische Updates einrichten

Am Beispiel von GitHub: Richten Sie einen Webhook ein, der bei Push ausgelöst wird:

1. Gehen Sie zu den Einstellungen Ihres GitHub-Repositorys
2. Klicken Sie auf die Option "Webhooks"
3. Klicken Sie auf "Add Webhook"
4. Füllen Sie die Konfiguration aus:
   - **Payload URL**: `http://your-domain.com/webhook`
   - **Content type**: `application/json`
   - **Secret**: Geben Sie Ihr zufälliges Passwort ein
   - **Which events**: Wählen Sie "Just the push event"

Wenn der Inhalt Ihres Git-Repositorys aktualisiert wird, löst dieser Webhook einen Neubau der Hugo-Website aus.

Auch Gitea, Gitee (nur WebHook-Passwort-Modus) und GitLab werden unterstützt, die Konfiguration ist ähnlich.

## Systemarchitektur-Analyse

ModernWiki besteht aus mehreren kombinierten Docker-Containern, es werden leichtgewichtige Systeme verwendet, nur 130M RAM:

### 1. Site-Aktualisierungs-Container (hugo-builder)

- Pullt das öffentliche Git-Repository und generiert mit Hugo statische Webseiten
- Gibt die Ausgabe in das freigegebene `site`-Verzeichnis aus
- Einmaliger Container, beendet sich nach Ausführung.

### 2. Statischer Site-Container (static-site)

- Bedient kontinuierlich die statischen Dateien im `site`-Verzeichnis

### 3. Webhook-Controller-Container (webhook)

- Empfängt kontinuierlich Webhook-Anfragen bei git push
- Startet nach Empfang über die Docker-API den hugo-builder neu

### 4. Kommentar-Server

- artalk

### 5. Optional: Gitea-Container (gitea)

- Optionaler Container für selbst gehostetes Git-Webhosting
- Gitea-Daten werden im Verzeichnis `data/gitea` gespeichert, Backups sind erforderlich

### 6. Eingangs-Reverse-Proxy-Container (proxy)

- Hört auf Port 80 als Einstiegspunkt
- Routing-Regeln:
  - `/` → Statischer Site-Container
  - `/webhook` → Webhook-Container
  - Unterstützt den Import zusätzlicher Caddyfile-Site-Konfigurationen

## Entwicklung und Debugging

### Upgrade

Zuerst dieses Repository aktualisieren, dann den Docker-Rebuild ausführen, alle Images und Software werden auf die neueste Version aktualisiert.

```bash
git pull
docker compose build --pull
```

### Logs anzeigen

```bash
# Logs aller Dienste anzeigen
docker compose logs -f

# Logs eines bestimmten Dienstes anzeigen
docker compose logs -f hugo-builder
docker compose logs -f static-site
docker compose logs -f webhook
docker compose logs -f proxy
```

### Site manuell neu bauen

```bash
docker compose restart hugo-builder
```

## Produktions-Deployment

Dieses Wiki-System baut nur bei Repository-Updates, dient sonst statische Dateien aus und hat einen extrem geringen Leistungsverbrauch. Daher reichen Burstable-Performance-Instanzen aus (**Preis -50%**).

### 1. Domain verwenden

Bearbeiten Sie `.env`, setzen Sie `DOMAIN=` auf Ihre Domain.

### 2. HTTPS-Unterstützung

Keine Konfiguration erforderlich, das System beantragt automatisch und regelmäßig kostenlose Zertifikate von Let's Encrypt oder ZeroSSL für Ihre Domain. Stellen Sie sicher:

- Die DNS-Einträge Ihrer Domain zeigen auf Ihren Server
- Die Firewall-Ports 80 und 443 sind nach außen geöffnet

## Serverless-Bereitstellungsmethode (TODO)

Dies ist die preisgünstigste Bereitstellungsmethode, erfordert nur den Kauf von Bandbreite und Speicher, ist aber aufwändig in der Bereitstellung, hat weniger Funktionen und wird nur als Referenz nicht empfohlen.

- Verwenden Sie ein extern gehostetes Repository
- Nutzen Sie Function Compute (FC), um über HTTP-Trigger Webhooks zu empfangen, den hugo-builder-Container zu starten und die Ausgabe in OSS-Speicher zu schreiben
- Aktivieren Sie für OSS statisches Website-Hosting und richten Sie eine Domain ein
- Richten Sie eine weitere FC-Funktion ein, die monatlich zeitgesteuert ausgelöst wird, um SSL-Zertifikate zu aktualisieren und in OSS hochzuladen

## Lizenz

MIT License
