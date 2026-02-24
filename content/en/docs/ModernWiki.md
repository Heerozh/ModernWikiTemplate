# ModernWiki

A minimalist Wiki system that uses a Git repository as a database and Markdown as the formatting language.

The essence of a Wiki is version control and open-source collaboration. Using the mature Git system better manages vandalism issues, and Markdown is also easier to edit.

## Quick Start

## 1. Create Content Repository

The content repository is the Wiki's page repository, open for users to modify freely. Please use the [ModernWikiTemplate](https://github.com/Heerozh/ModernWikiTemplate.git) repository as a template. The repository is in Hugo project format, and you can freely modify the website style within it.

### **GitHub:**

Directly Fork [ModernWikiTemplate](https://github.com/Heerozh/ModernWikiTemplate.git)
Also supports Gitee, GitLab.

### **(Recommended) Private Git Repository:**

Skip this for now, set it up after starting the system:

Visit <http://localhost/git>, click Install Gitea (Install Now), register an Admin account, click the ➕ in the top right corner, select migrate (Migrate External Repository),
clone <https://github.com/Heerozh/ModernWikiTemplate.git>,
rename it to Wiki.

> Note: The repository permissions must be set to allow everyone to Push, otherwise changes will require PR review. If you only want the Content directory to be Push-able, while site configuration and style files require PRs, you can use Git submodules with two separate repositories to achieve this.

## 2. Configure Environment Variables

Copy the environment variable template:

```bash
cp .env.example .env
```

Edit the `.env` file to set your Git repository:

```bash
GIT_REPO=https:/domain.com/your-username/your-wiki-content.git
GIT_BRANCH=master
DOMAIN=:80 # For local testing, only :80 can be used, otherwise it will be inaccessible
```

> [!NOTE]
> After each modification to `.env`, you need to rebuild the image: `docker compose build`

## 3. Start the System

First, install Docker Engine and the docker-compose-plugin, then:

```bash
# Start services (third-party Git hosting)
docker compose up -d

# Start services (self-hosted Gitea)
docker compose --profile with-gitea up -d
```

## 4. Access the Wiki

- Main site: <http://localhost>
- Webhook endpoint: <http://localhost/webhook>
- Local Gitea repository (if enabled): <http://localhost/git/>

## 5. Set Up Automatic Updates

Using GitHub as an example, set up a Webhook to trigger on Push:

1. Go to your GitHub repository settings
2. Click the "Webhooks" option
3. Click "Add Webhook"
4. Fill in the configuration:
   - **Payload URL**: `http://your-domain.com/webhook`
   - **Content type**: `application/json`
   - **Secret**: Enter your random password
   - **Which events**: Select "Just the push event"

When your Git repository content is updated, this Webhook will trigger Hugo to rebuild the website.

Also supports Gitea, Gitee (only WebHook password mode), and GitLab, with similar configuration.

## System Architecture Analysis

ModernWiki is composed of multiple Docker containers, using lightweight systems, requiring only 130M memory:

### 1. Site Refresh Container (hugo-builder)

- Pulls the public Git repository and uses Hugo to generate static web pages
- Outputs to the shared `site` directory
- A one-time container that exits after execution.

### 2. Static Site Container (static-site)

- Continuously serves static files from the `site` directory

### 3. Webhook Controller Container (webhook)

- Continuously receives webhook requests on git push
- Upon receipt, restarts the hugo-builder via the Docker API

### 4. Comment Server

- artalk

### 5. Optional: Gitea Container (gitea)

- Optional container for self-hosted Git web hosting
- Gitea data is stored in the `data/gitea` directory and needs backup

### 6. Entry Reverse Proxy Container (proxy)

- Listens on port 80 as the entry point
- Routing rules:
  - `/` → Static site container
  - `/webhook` → Webhook container
  - Supports importing additional Caddyfile site configurations

## Development and Debugging

### Upgrade

First, update this repository, then execute the Docker rebuild; all images and software will be upgraded to the latest version.

```bash
git pull
docker compose build --pull
```

### View Logs

```bash
# View logs for all services
docker compose logs -f

# View logs for a specific service
docker compose logs -f hugo-builder
docker compose logs -f static-site
docker compose logs -f webhook
docker compose logs -f proxy
```

### Manually Rebuild Site

```bash
docker compose restart hugo-builder
```

## Production Deployment

This Wiki system only builds when the repository is updated; normally it serves static files, resulting in extremely low performance overhead. Therefore, burstable performance instances are sufficient (**price -50%**).

### 1. Using a Domain Name

Modify `.env`, set `DOMAIN=` to your domain name.

### 2. HTTPS Support

No configuration needed. The system will automatically and periodically apply for free Let's Encrypt or ZeroSSL certificates for your domain. Ensure:

- Your domain's DNS points to your server
- Firewall ports 80 and 443 are open to the public

## Serverless Deployment Method (TODO)

This is the lowest-cost deployment method, requiring only bandwidth and storage purchases, but it's complex to deploy, has fewer features, and is not recommended, provided for reference only.

- Use a third-party hosted repository
- Utilize Function Compute (FC) to receive Webhooks via HTTP triggers, start the hugo-builder container, and output to OSS storage
- Enable static website hosting for OSS and set up a domain name
- Set up another Function Compute (FC) to trigger monthly, updating and uploading SSL certificates to OSS

## License

MIT License
