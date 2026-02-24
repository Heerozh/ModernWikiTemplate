# ModernWiki

Un sistema Wiki minimalista que utiliza repositorios Git como base de datos y Markdown como lenguaje de formato.

La esencia de un Wiki es el control de versiones y la colaboración de código abierto. Utilizar Git, una tecnología madura, permite gestionar mejor los problemas de vandalismo, y Markdown facilita la edición.

## Comenzar rápidamente

## 1. Crear el repositorio de contenido

El repositorio de contenido es el repositorio de páginas del Wiki, abierto para que los usuarios lo modifiquen libremente. Utiliza el repositorio [ModernWikiTemplate](https://github.com/Heerozh/ModernWikiTemplate.git) como plantilla. El repositorio sigue el formato de proyecto Hugo, donde puedes modificar libremente el estilo del sitio web.

### **GitHub:**

Simplemente haz un Fork de [ModernWikiTemplate](https://github.com/Heerozh/ModernWikiTemplate.git).
También se admite Gitee, GitLab.

### **（Recomendado）Repositorio Git privado:**

Omite este paso por ahora y configúralo después de iniciar el sistema:

Accede a <http://localhost/git>, haz clic en "Install Gitea" (Instalar ahora), registra una cuenta de administrador (Admin), haz clic en el ➕ en la esquina superior derecha, selecciona "migrate" (migrar repositorio externo),
clona <https://github.com/Heerozh/ModernWikiTemplate.git>
y cámbiale el nombre a "Wiki".

> Nota: Es necesario habilitar permisos de Push para todos en el repositorio; de lo contrario, se requerirá revisión por PR. Si solo deseas que el directorio Content tenga permisos de Push, mientras que los archivos de configuración del sitio y estilos requieran PR, puedes usar submódulos Git, utilizando 2 repositorios diferentes para lograrlo.

## 2. Configurar variables de entorno

Copia la plantilla de variables de entorno:

```bash
cp .env.example .env
```

Edita el archivo `.env` y configura tu repositorio Git:

```bash
GIT_REPO=https:/domain.com/your-username/your-wiki-content.git
GIT_BRANCH=master
DOMAIN=:80 # Para pruebas locales solo se puede usar :80, de lo contrario no será accesible
```

> [!NOTE]
> Después de cada modificación en `.env`, es necesario reconstruir la imagen: `docker compose build`

## 3. Iniciar el sistema

Primero instala Docker Engine y el plugin docker-compose, luego:

```bash
# Iniciar servicios (alojamiento Git de terceros)
docker compose up -d

# Iniciar servicios (alojamiento con Gitea local)
docker compose --profile with-gitea up -d
```

## 4. Acceder al Wiki

- Sitio principal: <http://localhost>
- Endpoint de Webhook: <http://localhost/webhook>
- Repositorio local Gitea (si está habilitado): <http://localhost/git/>

## 5. Configurar actualización automática

Tomando GitHub como ejemplo, configura un Webhook que se active al hacer Push:

1. Ve a la configuración de tu repositorio en GitHub.
2. Haz clic en la opción "Webhooks".
3. Haz clic en "Add Webhook".
4. Completa la configuración:
   - **Payload URL**: `http://your-domain.com/webhook`
   - **Content type**: `application/json`
   - **Secret**: Ingresa tu contraseña aleatoria.
   - **Which events**: Selecciona "Just the push event".

Cuando se actualice el contenido de tu repositorio Git, este Webhook activará la reconstrucción del sitio web por parte de Hugo.

También se admite Gitea, Gitee (solo modo de contraseña para WebHook) y GitLab, con una configuración similar.

## Análisis de la arquitectura del sistema

ModernWiki está compuesto por múltiples contenedores Docker combinados, utilizando sistemas ligeros, con solo 130M de memoria:

### 1. Contenedor de actualización del sitio (hugo-builder)

- Extrae el repositorio Git público y genera páginas web estáticas usando Hugo.
- La salida se guarda en el directorio compartido `site`.
- Contenedor de una sola ejecución, se cierra después de completar la tarea.

### 2. Contenedor de sitio estático (static-site)

- Sirve continuamente los archivos estáticos del directorio `site`.

### 3. Contenedor controlador de Webhook (webhook)

- Recibe continuamente las solicitudes de webhook al realizar un push en Git.
- Al recibir una solicitud, reinicia hugo-builder a través de la API de Docker.

### 4. Servidor de comentarios

- artalk

### 5. Opcional: Contenedor Gitea (gitea)

- Contenedor opcional para alojar Git de forma autónoma.
- Los datos de Gitea se almacenan en el directorio `data/gitea`, es necesario realizar copias de seguridad.

### 6. Contenedor proxy de entrada (proxy)

- Escucha en el puerto 80 como punto de entrada.
- Reglas de enrutamiento:
  - `/` → Contenedor de sitio estático.
  - `/webhook` → Contenedor Webhook.
  - Admite la importación de configuraciones de sitio Caddyfile adicionales.

## Desarrollo y depuración

### Actualizar

Primero actualiza este repositorio, luego ejecuta la reconstrucción de Docker; todas las imágenes y software se actualizarán a la última versión.

```bash
git pull
docker compose build --pull
```

### Ver registros (logs)

```bash
# Ver registros de todos los servicios
docker compose logs -f

# Ver registros de un servicio específico
docker compose logs -f hugo-builder
docker compose logs -f static-site
docker compose logs -f webhook
docker compose logs -f proxy
```

### Reconstruir el sitio manualmente

```bash
docker compose restart hugo-builder
```

## Despliegue en producción

Este sistema Wiki solo se construye cuando se actualiza el repositorio; normalmente sirve archivos estáticos, con un consumo de recursos extremadamente bajo. Por lo tanto, una instancia de cómputo de ráfaga es suficiente (**precio -50%**).

### 1. Usar un dominio

Modifica `.env`, establece `DOMAIN=` con tu dominio.

### 2. Soporte HTTPS

No requiere configuración; el sistema solicitará y renovará automáticamente certificados gratuitos de Let's Encrypt o ZeroSSL para tu dominio. Asegúrate de:

- Que el DNS de tu dominio apunte a tu servidor.
- Que los puertos 80 y 443 del firewall estén abiertos al exterior.

## Método de despliegue Serverless (TODO)

Este es un método de despliegue de menor costo, solo requiere comprar ancho de banda y almacenamiento, pero es complicado de implementar, tiene menos funciones y no se recomienda; se incluye solo como referencia.

- Utilizar un repositorio alojado por un tercero.
- Usar Function Compute (FC) para recibir Webhooks a través de un desencadenador HTTP, iniciar el contenedor hugo-builder y enviar la salida a OSS.
- Habilitar el alojamiento de sitios web estáticos en OSS y configurar el dominio.
- Configurar otra Function Compute (FC) que se active mensualmente para actualizar y cargar el certificado SSL a OSS.

## Licencia

MIT License
