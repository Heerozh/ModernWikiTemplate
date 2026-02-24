# ModernWiki

Un système Wiki minimaliste qui utilise un dépôt Git comme base de données et Markdown comme langage de formatage.

L'essence d'un Wiki est le contrôle de version et la collaboration open source. Utiliser Git, une technologie mature, permet de mieux gérer les problèmes de vandalisme, et Markdown est plus facile à éditer.

## Démarrage rapide

## 1. Créer le dépôt de contenu

Le dépôt de contenu est le dépôt des pages du Wiki, ouvert aux modifications par les utilisateurs. Veuillez utiliser le dépôt [ModernWikiTemplate](https://github.com/Heerozh/ModernWikiTemplate.git) comme modèle. Le dépôt est au format projet Hugo, vous pouvez y modifier librement le style du site.

### **GitHub :**

Forkez directement [ModernWikiTemplate](https://github.com/Heerozh/ModernWikiTemplate.git)
Également supporté : Gitee, GitLab.

### **Dépôt Git privé (recommandé) :**

Passez cette étape pour l'instant, revenez-y après avoir démarré le système :

Accédez à <http://localhost/git>, cliquez sur "Install Gitea" (Installer immédiatement), créez un compte Admin, cliquez sur le ➕ en haut à droite, sélectionnez "migrate" (migrer un dépôt externe),
clonez <https://github.com/Heerozh/ModernWikiTemplate.git>
et renommez-le en "Wiki".

> Note : Les permissions du dépôt doivent autoriser tout le monde à Push, sinon les modifications devront passer par une PR. Si vous souhaitez que seul le répertoire Content soit accessible en Push, tandis que les fichiers de configuration du site et de style nécessitent une PR, vous pouvez utiliser des sous-modules Git avec deux dépôts distincts.

## 2. Configurer les variables d'environnement

Copiez le modèle de variables d'environnement :

```bash
cp .env.example .env
```

Éditez le fichier `.env` pour configurer votre dépôt Git :

```bash
GIT_REPO=https:/domain.com/your-username/your-wiki-content.git
GIT_BRANCH=master
DOMAIN=:80 # Pour les tests locaux, vous devez utiliser :80, sinon l'accès sera impossible
```

> [!NOTE]
> Après chaque modification de `.env`, vous devez reconstruire l'image : `docker compose build`

## 3. Démarrer le système

Installez d'abord Docker Engine et le plugin docker-compose, puis :

```bash
# Démarrer les services (hébergement Git tiers)
docker compose up -d

# Démarrer les services (hébergement local avec Gitea)
docker compose --profile with-gitea up -d
```

## 4. Accéder au Wiki

- Site principal : <http://localhost>
- Point de terminaison Webhook : <http://localhost/webhook>
- Dépôt local Gitea (si activé) : <http://localhost/git/>

## 5. Configurer la mise à jour automatique

Prenons GitHub comme exemple, configurez un Webhook déclenché lors d'un Push :

1. Accédez aux paramètres de votre dépôt GitHub
2. Cliquez sur l'option "Webhooks"
3. Cliquez sur "Add Webhook"
4. Remplissez la configuration :
   - **Payload URL** : `http://your-domain.com/webhook`
   - **Content type** : `application/json`
   - **Secret** : Saisissez votre mot de passe aléatoire
   - **Which events** : Sélectionnez "Just the push event"

Lorsque le contenu de votre dépôt Git est mis à jour, ce Webhook déclenchera la reconstruction du site par Hugo.

Également supporté : Gitea, Gitee (mode mot de passe WebHook uniquement) et GitLab, configuration similaire.

## Analyse de l'architecture système

ModernWiki est composé de plusieurs conteneurs Docker combinés, utilisant des systèmes légers, nécessitant seulement 130 Mo de mémoire :

### 1. Conteneur de rafraîchissement du site (hugo-builder)

- Récupère le dépôt Git public et génère des pages web statiques avec Hugo
- Sortie vers le répertoire partagé `site`
- Conteneur à usage unique, s'arrête après exécution.

### 2. Conteneur de site statique (static-site)

- Sert continuellement les fichiers statiques du répertoire `site`

### 3. Conteneur contrôleur Webhook (webhook)

- Reçoit continuellement les requêtes Webhook lors des push Git
- Après réception, redémarre hugo-builder via l'API Docker

### 4. Serveur de commentaires

- artalk

### 5. Optionnel : Conteneur Gitea (gitea)

- Conteneur optionnel pour l'hébergement web Git auto-hébergé
- Les données de Gitea sont stockées dans le répertoire `data/gitea`, nécessitant une sauvegarde

### 6. Conteneur proxy d'entrée (proxy)

- Écoute sur le port 80 comme point d'entrée
- Règles de routage :
  - `/` → Conteneur de site statique
  - `/webhook` → Conteneur Webhook
  - Prend en charge l'import de configurations de site Caddyfile supplémentaires

## Développement et débogage

### Mise à niveau

Mettez d'abord à jour ce dépôt, puis exécutez la reconstruction Docker. Toutes les images et logiciels seront mis à niveau vers la dernière version.

```bash
git pull
docker compose build --pull
```

### Voir les journaux

```bash
# Voir les journaux de tous les services
docker compose logs -f

# Voir les journaux d'un service spécifique
docker compose logs -f hugo-builder
docker compose logs -f static-site
docker compose logs -f webhook
docker compose logs -f proxy
```

### Reconstruire le site manuellement

```bash
docker compose restart hugo-builder
```

## Déploiement en production

Ce système Wiki ne construit que lors des mises à jour du dépôt, servant des fichiers statiques le reste du temps, avec une consommation de ressources très faible. Une instance à performance ponctuelle est donc suffisante (**prix -50%**).

### 1. Utiliser un nom de domaine

Modifiez `.env`, définissez `DOMAIN=` avec votre nom de domaine.

### 2. Support HTTPS

Aucune configuration nécessaire, le système demandera et renouvellera automatiquement et périodiquement des certificats gratuits Let's Encrypt ou ZeroSSL pour votre domaine. Assurez-vous que :

- Le DNS de votre domaine pointe vers votre serveur
- Les ports 80 et 443 du pare-feu sont ouverts vers l'extérieur

## Méthode de déploiement Serverless (TODO)

C'est la méthode de déploiement la moins chère, nécessitant uniquement l'achat de bande passante et de stockage, mais elle est complexe à déployer, offre moins de fonctionnalités et n'est pas recommandée, fournie à titre informatif.

- Utiliser un dépôt d'hébergement tiers
- Utiliser le calcul de fonctions FC, recevoir le Webhook via un déclencheur HTTP, démarrer le conteneur hugo-builder, sortir vers le stockage OSS
- Activer l'hébergement de site statique sur OSS, configurer le nom de domaine
- Configurer un autre calcul de fonctions FC, déclenché mensuellement, pour mettre à jour et télécharger le certificat SSL vers OSS

## Licence

MIT License
