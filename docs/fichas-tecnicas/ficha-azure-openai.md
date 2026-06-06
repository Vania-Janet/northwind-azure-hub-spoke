# Ficha Técnica — Azure OpenAI (Persona 3)

- **Responsable:** Luis Enrique Morales Flores
- **Área del proyecto:** App / IA

---

## Recurso 1: Azure OpenAI Account

### 1. Identificación del recurso

- **Servicio de Azure:** Azure OpenAI (Cognitive Services)
- **Nombre exacto (nomenclatura):** `aoai-northwind-mvp-eastus`
- **Azure Resource ID:** `/subscriptions/26ae16d4-2f67-45f7-9d46-6c02d925cf48/resourceGroups/rg-northwind-mvp-eastus/providers/Microsoft.CognitiveServices/accounts/aoai-northwind-mvp-eastus`
- **Resource Group:** `rg-northwind-mvp-eastus`
- **Ubicación:** Región: `eastus` | Ambiente: `mvp`
- **Tipo de recurso Azure:** `microsoft.cognitiveservices/accounts`

### 2. Configuración técnica

- **SKU / tier:** S0 (Standard)
- **Modelo deployado:** `gpt-4o-mini`
- **Nombre del deployment:** `gpt-4o-mini`
- **Deployment type:** Standard
- **Context window:** 128,000 tokens
- **Para SQL (Modelo de compra):** [x] No Aplica
- **Para Storage (Tipo de servicio):** [x] No Aplica
- **Redundancia:** [x] No Aplica
- **Alta disponibilidad:** [x] No Aplica
- **Autoapagado configurado:** [x] No Aplica

### 3. Red y seguridad

- **VNet y Subnet asignada:** N/A — acceso público por ahora
- **Asignación de IP Privada:** [x] No Aplica
- **¿Tiene IP pública?** [x] Sí — acceso público habilitado (MVP). En producción se recomienda Private Endpoint.
- **Aislamiento:** Acceso público habilitado para MVP
- **Enlace privado:** [x] No Aplica (MVP)
- **¿Usa Managed Identity?** [x] No — autenticación por API Key almacenada en App Service Configuration

  > ⚠️ Deuda técnica: en producción se recomienda acceso por Private Endpoint + Managed Identity para eliminar el manejo de API keys.

### 4. Secretos y credenciales

- **¿Usa secretos?** [x] Sí
- **Dónde están guardados:** [x] App Service Configuration (Application Settings) del App Service `app-ops-northwind-mvp-eastus`
- **Variables configuradas en el App Service:**
  - `AZURE_OPENAI_ENDPOINT` = `https://aoai-northwind-mvp-eastus.openai.azure.com/`
  - `AZURE_OPENAI_API_KEY` = (API key del recurso)
  - `AZURE_OPENAI_DEPLOYMENT` = `gpt-4o-mini`

### 5. Dependencias

- **Este recurso depende de:** Resource Group `rg-northwind-mvp-eastus`
- **Otros recursos dependen de este:** App Service `app-ops-northwind-mvp-eastus` (agente IA en `ai/agent.py`)
- **Recursos dependientes creados junto con este:** Model deployment `gpt-4o-mini`

### 6. Tags aplicados

`Project = northwind-mvp` | `Environment = mvp` | `Owner = equipo-cloud-iimas`
`CostCenter = CloudClass` | `Workload = PrivateIntranet` | `Criticality = low`

¿Todos los tags fueron aplicados? [x] Sí

### 7. Pruebas

- **Prueba realizada:** Llamada a `/api/chat` desde la UI del agente IA con pregunta sobre documentos del departamento de operaciones
- **Resultado:** [x] Exitoso
- **Retos encontrados y cómo se resolvió:** Conflicto de versiones entre `openai` y `httpx`: `openai==1.51.0` pasa el argumento `proxies` a httpx pero `httpx>=0.28` lo eliminó. Se resolvió fijando `openai==1.57.0` + `httpx==0.27.2` en `requirements.txt`.

### 8. Datos Técnicos para la Calculadora

- **SKU:** S0 Standard
- **Modelo:** gpt-4o-mini
- **Precio:** Pay-per-use (por tokens). Input: ~$0.15/1M tokens, Output: ~$0.60/1M tokens
- **Horas activas al mes:** N/A (solo cobra por uso)
- **Tokens estimados al mes:** Bajo (MVP con pocos usuarios, ~5 docs por departamento en contexto)

---

## Recurso 2: Private Endpoint — App Service

### 1. Identificación del recurso

- **Servicio de Azure:** Private Endpoint
- **Nombre exacto (nomenclatura):** `pe-app-ops-mvp-eastus`
- **Resource Group:** `rg-northwind-mvp-eastus`
- **Ubicación:** Spoke Ops | Región: `eastus` | Ambiente: `mvp`
- **Tipo de recurso Azure:** `microsoft.network/privateendpoints`
- **Recurso destino:** App Service `app-ops-northwind-mvp-eastus` (sub-resource: `sites`)

### 2. Configuración técnica

- **SKU / tier:** N/A
- **IP privada asignada:** `10.1.3.4` (dinámica DHCP)
- **Subnet:** `snet-private-endpoints-ops` en `vnet-spk-ops-northwind-mvp-eastus`
- **Alta disponibilidad:** [x] No Aplica
- **Autoapagado:** [x] No Aplica

### 3. Red y seguridad

- **VNet y Subnet:** `vnet-spk-ops-northwind-mvp-eastus` / `snet-private-endpoints-ops`
- **Asignación de IP Privada:** [x] Dinámica (DHCP) — IP: `10.1.3.4`
- **¿Tiene IP pública?** [x] No
- **Enlace privado:** [x] Usa Private DNS Zone — `privatelink.azurewebsites.net`
  - Registro A: `app-ops-northwind-mvp-eastus-cwftarh4bqdyhdak.eastus-01` → `10.1.3.4`
  - DNS Zone vinculada a: `vnet-hub-northwind-mvp-eastus` y `vnet-spk-ops-northwind-mvp-eastus`

### 4. Secretos y credenciales

- **¿Usa secretos?** [x] No

### 5. Dependencias

- **Este recurso depende de:** App Service `app-ops-northwind-mvp-eastus`, subnet `snet-private-endpoints-ops`
- **Otros recursos dependen de este:** Clientes VPN P2S que acceden a la app por red privada
- **Recursos creados junto con este:** NIC, registro A en `privatelink.azurewebsites.net`

### 6. Tags aplicados

`Project = northwind-mvp` | `Environment = mvp` | `Owner = equipo-cloud-iimas`
`CostCenter = CloudClass` | `Workload = PrivateIntranet` | `Criticality = low`

¿Todos los tags fueron aplicados? [x] Sí

### 7. Pruebas

- **Prueba realizada:** Conexión desde cliente VPN P2S a `10.1.3.4:443` — `curl` devuelve `{"status":"ok"}` con `HTTP/1.1 200 OK`. Conexión desde IP de VPN `172.16.0.2` confirmada.
- **Resultado:** [x] Exitoso
- **Retos encontrados:** Resolución DNS automática para clientes P2S pendiente (workaround: hosts file). Ver ficha App Service reto #5.

### 8. Datos Técnicos para la Calculadora

- **SKU:** N/A
- **Costo aproximado:** ~$0.01/hora por endpoint + $0.01/GB datos procesados
- **Horas activas al mes:** 730 (24/7)
