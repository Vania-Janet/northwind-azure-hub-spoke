# Ficha Técnica — App Service (Persona 3)

- **Responsable:** Luis Enrique Morales Flores
- **Área del proyecto:** App

---

## Recurso 1: App Service Plan

### 1. Identificación del recurso

- **Servicio de Azure:** App Service Plan
- **Nombre exacto (nomenclatura):** `asp-northwind-mvp-eastus`
- **Azure Resource ID:** `/subscriptions/26ae16d4-2f67-45f7-9d46-6c02d925cf48/resourceGroups/rg-northwind-mvp-eastus/providers/Microsoft.Web/serverFarms/asp-northwind-mvp-eastus`
- **Resource Group:** `rg-northwind-mvp-eastus`
- **Ubicación:** Spoke Ops (por VNet Integration) | Región: `eastus` | Ambiente: `mvp`
- **Tipo de recurso Azure:** `microsoft.web/serverfarms`

### 2. Configuración técnica

- **SKU / tier / tamaño exacto:** Premium v3 P0V3
- **Sistema operativo:** Linux
- **Plan asociado:** N/A (este recurso es el plan)
- **Número de instancias:** 1
- **Para SQL (Modelo de compra):** [x] No Aplica
- **Para Storage (Tipo de servicio):** [x] No Aplica
- **Capacidad / almacenamiento configurado:** N/A
- **Redundancia:** [x] No Aplica
- **Alta disponibilidad:** [x] No
- **Autoapagado configurado:** [x] No (24/7)

### 3. Red y seguridad

- **VNet y Subnet asignada:** N/A (el plan en sí no tiene VNet; la integración VNet es del App Service)
- **Asignación de IP Privada:** [x] No Aplica
- **¿Tiene IP pública?** No Aplica
- **Aislamiento:** N/A
- **Enlace privado:** [x] No Aplica
- **¿Usa Managed Identity?** [x] No

### 4. Secretos y credenciales

- **¿Usa secretos?** [x] No
- **Dónde están guardados:** N/A

### 5. Dependencias

- **Este recurso depende de:** Resource Group `rg-northwind-mvp-eastus`
- **Otros recursos dependen de este:** App Service `app-ops-northwind-mvp-eastus`
- **Recursos dependientes creados junto con este:** Ninguno

### 6. Tags aplicados

`Project = northwind-mvp` | `Environment = mvp` | `Owner = equipo-cloud-iimas`
`CostCenter = CloudClass` | `Workload = PrivateIntranet` | `Criticality = low`

¿Todos los tags fueron aplicados? [x] Sí

### 7. Pruebas

- **Prueba realizada:** Creación exitosa del App Service sobre este plan; verificación de que el App Service corre con runtime Python 3.11
- **Resultado:** [x] Exitoso
- **Retos encontrados y cómo se resolvió:**
  - East US no tenía capacidad disponible para B1 en el resource group original. Se resolvió cambiando el SKU (Premium v3 P0V3). Finalmente el Premium v3 P0V3 en `rg-northwind-mvp-eastus` quedó disponible.

### 8. Datos Técnicos para la Calculadora

- **SKU:** Premium v3 P0V3
- **Horas activas al mes:** 730 (24/7)
- **Almacenamiento estimado:** N/A
- **Usuarios estimados:** N/A

---

## Recurso 2: App Service – Web App

### 1. Identificación del recurso

- **Servicio de Azure:** App Service – Web App
- **Nombre exacto (nomenclatura):** `app-ops-northwind-mvp-eastus`
- **Azure Resource ID:** `/subscriptions/26ae16d4-2f67-45f7-9d46-6c02d925cf48/resourceGroups/rg-northwind-mvp-eastus/providers/Microsoft.Web/sites/app-ops-northwind-mvp-eastus`
- **Resource Group:** `rg-northwind-mvp-eastus`
- **Ubicación:** Spoke Ops (por VNet Integration) | Región: `eastus` | Ambiente: `mvp`
- **Tipo de recurso Azure:** `microsoft.web/sites`
- **URL (acceso privado vía VPN):** `https://app-ops-northwind-mvp-eastus-cwftarh4bqdyhdak.eastus-01.azurewebsites.net`

### 2. Configuración técnica

- **SKU / tier / tamaño exacto:** 
Premium0V3 (P0v3) — heredado del App Service Plan
- **Sistema operativo:** Linux
- **Runtime:** Python 3.11
- **Plan asociado:** `asp-northwind-mvp-eastus`
- **Número de instancias:** 1
- **Startup command:** `gunicorn --bind=0.0.0.0:8000 --timeout=600 --workers=2 --chdir src main:app`
- **Para SQL (Modelo de compra):** [x] No Aplica
- **Para Storage (Tipo de servicio):** [x] No Aplica
- **Capacidad / almacenamiento configurado:** N/A
- **Redundancia:** [x] No Aplica
- **Alta disponibilidad:** [x] No
- **Autoapagado configurado:** [x] No (24/7)

### 3. Red y seguridad

- **VNet y Subnet asignada (VNet Integration — salida):** `vnet-spk-ops-northwind-mvp-eastus` / `snet-app-ops` (10.1.1.0/24)
- **Asignación de IP Privada del Private Endpoint:** [x] Dinámica (DHCP) — IP asignada: `10.1.3.4`
- **¿Tiene IP pública?** [x] Sí — pero bloqueada por Access Restrictions. Justificación: necesaria para que GitHub Actions pueda hacer deploy vía SCM endpoint.
- **Aislamiento:** [x] Bloqueado por Firewall/NSG — Access Restrictions configuradas: Main site = Deny all; SCM (Advanced tool site) = Allow (para CI/CD).
- **Enlace privado:** [x] Usa Private Endpoint [x] Usa Private DNS Zone
- **Nombre y subnet del Private Endpoint:** `pe-app-ops-mvp-eastus` en `snet-private-endpoints-ops`
- **DNS Zone:** `privatelink.azurewebsites.net` — vinculada a `vnet-hub-northwind-mvp-eastus` y `vnet-spk-ops-northwind-mvp-eastus`
- **Reglas relevantes:**
  - Main site: Unmatched rule action = Deny (bloquea acceso público)
  - SCM site: Unmatched rule action = Allow, sin heredar reglas del main site
  - Public network access: Enabled from select virtual networks and IP addresses
- **¿Usa Managed Identity?** [x] No

### 4. Secretos y credenciales

- **¿Usa secretos?** [x] Sí
- **Dónde están guardados:** [x] App Service Configuration (Application Settings)
- **Variables configuradas:**
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_API_KEY`
  - `AZURE_OPENAI_DEPLOYMENT` = `gpt-4o-mini`
  - `AZURE_SQL_SERVER`
  - `AZURE_SQL_DATABASE` = `sqldb-ops-mvp`
  - `AZURE_SQL_USER`
  - `AZURE_SQL_PASSWORD`
  - `FLASK_SECRET_KEY`
  - `SCM_DO_BUILD_DURING_DEPLOYMENT` = `true`
  - `AZURE_STORAGE_CONN` = connection string del Storage Account `stnorthwindmvp`

### 5. Dependencias

- **Este recurso depende de:**
  - App Service Plan `asp-northwind-mvp-eastus`
  - VNet Integration: `vnet-spk-ops-northwind-mvp-eastus` / `snet-app-ops`
  - Private Endpoint: `pe-app-ops-mvp-eastus`
  - Azure OpenAI `aoai-northwind-mvp-eastus` (para el agente IA)
  - Azure SQL `sqldb-ops-mvp` en servidor `sql-ops-northwind-mvp-centralus` (para historial de chat)
  - GitHub repo (`app_privada_spoke` branch) para CI/CD
- **Otros recursos dependen de este:** Ninguno (es el frontend de la solución)
- **Recursos dependientes creados junto con este:**
  - Private Endpoint `pe-app-ops-mvp-eastus`
  - NIC del private endpoint
  - Registro A en `privatelink.azurewebsites.net` (auto-creado al crear el private endpoint)

### 6. Tags aplicados

`Project = northwind-mvp` | `Environment = mvp` | `Owner = equipo-cloud-iimas`
`CostCenter = CloudClass` | `Workload = PrivateIntranet` | `Criticality = low`

¿Todos los tags fueron aplicados? [x] Sí

### 7. Pruebas

- **Prueba realizada:** Acceso a `/health` con y sin VPN P2S conectada. Verificación de aislamiento de red.
- **Resultado:** [x] Exitoso
- **Retos encontrados y cómo se resolvió:**
  1. **Capacidad de East US:** La región East US no tenía instancias disponibles inicialmente. Se resolvió cambiando el SKU a 
  Premium0V3 (P0v3) en la misma región.
  2. **Startup command con Oryx:** Oryx comprime el build en `output.tar.zst` y lo extrae en `/tmp/` en tiempo de ejecución, no en `/home/site/wwwroot/`. El startup command usaba rutas absolutas que no existían. Se resolvió usando el comando gunicorn directamente con `--chdir src` en la configuración del App Service.
  3. **Basic Auth deshabilitado:** Azure deshabilita Basic Auth por defecto en suscripciones nuevas, impidiendo descargar el Publish Profile para GitHub Actions. Se habilitó desde Configuration → General settings.
  4. **Acceso SCM con sitio privado:** Al deshabilitar el acceso público, el SCM (Kudu) también quedaba bloqueado, impidiendo el deploy de GitHub Actions. Se resolvió configurando Access Restrictions con Main site = Deny y SCM site = Allow independiente.
  5. **Resolución DNS para clientes VPN:** Los clientes P2S VPN usaban DNS local y no resolvían la zona privada `privatelink.azurewebsites.net`. Workaround implementado: entrada manual en `C:\Windows\System32\drivers\etc\hosts` apuntando `10.1.3.4 app-ops-northwind-mvp-eastus-cwftarh4bqdyhdak.eastus-01.azurewebsites.net` al hostname del App Service. Fix permanente pendiente: re-descargar perfil VPN con `168.63.129.16` configurado en hub VNet DNS.

### 8. Datos Técnicos para la Calculadora

- **SKU:** Premium v3 P0V3
- **Horas activas al mes:** 730 (24/7)
- **Almacenamiento estimado:** N/A (sin almacenamiento propio; usa SQL y Blob externos)
- **Usuarios estimados:** N/A
