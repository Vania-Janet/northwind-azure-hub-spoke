# Ficha Técnica — Azure Blob Storage (Persona 3)

- **Responsable:** Luis Enrique Morales Flores
- **Área del proyecto:** App / Almacenamiento departamental

---

## Recurso 1: Storage Account

### 1. Identificación del recurso

- **Servicio de Azure:** Azure Storage Account (Blob Storage)
- **Nombre exacto (nomenclatura):** `stnorthwindmvp`
- **Azure Resource ID:** `/subscriptions/26ae16d4-2f67-45f7-9d46-6c02d925cf48/resourceGroups/rg-northwind-mvp-eastus/providers/Microsoft.Storage/storageAccounts/stnorthwindmvp`
- **Resource Group:** `rg-northwind-mvp-eastus`
- **Ubicación:** Región: `eastus` | Ambiente: `mvp`
- **Tipo de recurso Azure:** `microsoft.storage/storageaccounts`

### 2. Configuración técnica

- **SKU / tier:** Standard (General Purpose v2)
- **Para Storage (Tipo de servicio):** [x] Blob Storage
- **Redundancia:** Locally Redundant Storage (LRS)
- **Alta disponibilidad:** [x] No (MVP)
- **Autoapagado configurado:** [x] No Aplica
- **Containers configurados:**
  - `documentos-ops` — documentos internos del departamento de Operaciones
  - `documentos-ventas` — documentos internos del departamento de Ventas

  > **Decisión de diseño:** Se usa un único Storage Account con dos containers en lugar de dos cuentas separadas. En la arquitectura objetivo cada spoke tendría su propia cuenta de almacenamiento con su propio Private Endpoint en su VNet; en el MVP se consolidan en el spoke Ops por simplicidad, manteniendo la separación lógica a nivel de container. La aislación de acceso se garantiza en la aplicación: cada usuario solo puede listar y leer el container correspondiente a su departamento.

### 3. Red y seguridad

- **VNet y Subnet asignada:** N/A (el Storage Account no se integra a VNet directamente)
- **Asignación de IP Privada:** [x] No Aplica (la IP privada es del Private Endpoint)
- **¿Tiene IP pública?** [x] No — Public network access: Disabled. Acceso únicamente vía Private Endpoint.
- **Aislamiento:** [x] Public network access: Disabled
- **Enlace privado:** [x] Usa Private Endpoint — `pe-st-mvp`
- **¿Usa Managed Identity?** [x] No — autenticación mediante Access Key (connection string)

### 4. Secretos y credenciales

- **¿Usa secretos?** [x] Sí
- **Dónde están guardados:** [x] App Service Configuration (Application Settings) del App Service `app-ops-northwind-mvp-eastus`
- **Variables configuradas:**
  - `AZURE_STORAGE_CONN` = connection string completo (Access Key 1) del storage account

  > **Nota:** El portal denegó la asignación del rol `Storage Blob Data Contributor` (`Add role assignment` aparecía deshabilitado) porque el usuario no tiene el rol Owner en la suscripción, solo Contributor. Se optó por Access Key como método de autenticación, que no requiere asignación RBAC. En un entorno de producción se usaría Managed Identity.

### 5. Dependencias

- **Este recurso depende de:** Resource Group `rg-northwind-mvp-eastus`
- **Otros recursos dependen de este:** App Service `app-ops-northwind-mvp-eastus` (botón "Ver archivos" lista y muestra contenido de blobs por departamento)
- **Recursos dependientes creados junto con este:** Private Endpoint `pe-st-mvp`, NIC del endpoint, registro A en `privatelink.blob.core.windows.net`

### 6. Tags aplicados

`Project = northwind-mvp` | `Environment = mvp` | `Owner = equipo-cloud-iimas`
`CostCenter = CloudClass` | `Workload = PrivateIntranet` | `Criticality = low`

¿Todos los tags fueron aplicados? [x] Sí

### 7. Pruebas

- **Prueba realizada:** Desde la app desplegada en App Service, el endpoint `/api/files` lista correctamente los blobs del container correspondiente al departamento del usuario. El endpoint `/api/files/<filename>` descarga y muestra el contenido de archivos de texto. Acceso bloqueado desde internet (acceso público deshabilitado); solo funciona a través de la VNet Integration del App Service vía el Private Endpoint.
- **Resultado:** [x] Exitoso
- **Retos encontrados y cómo se resolvió:**
  1. **RBAC no disponible para upload desde portal:** El usuario tiene rol Contributor, no Owner, por lo que `Add role assignment` estaba deshabilitado. No fue posible asignarse el rol `Storage Blob Data Contributor`. Se resolvió habilitando temporalmente el acceso público para subir archivos de prueba y luego deshabilitándolo. La autenticación de la app usa Access Key, que no requiere RBAC.
  2. **Archivos subidos con 0 bytes:** La primera subida desde el portal generó blobs vacíos, probablemente por interferencia de la conectividad VPN durante la operación. Se resolvió re-subiendo los archivos con acceso público habilitado temporalmente y sin VPN activa.
  3. **Demo dept incorrecto en el modal:** El query param `?dept=ventas` se incluía en la carga inicial de la página, pero la llamada API `fetch('/api/files')` del modal no lo heredaba. Se resolvió persistiendo el usuario de demo en la sesión Flask (`session["demo_user"]`) al momento del primer acceso con el param, de modo que todas las llamadas API subsiguientes resuelven el departamento correcto desde sesión.

### 8. Datos Técnicos para la Calculadora

- **SKU:** Standard LRS
- **Costo de almacenamiento:** ~$0.018/GB/mes
- **Operaciones:** ~$0.004 por 10,000 operaciones de escritura; ~$0.0004 por 10,000 de lectura
- **Horas activas al mes:** 730 (24/7 — el storage no tiene auto-pause)
- **Volumen estimado:** < 1 GB (documentos internos de texto, MVP)

---

## Recurso 2: Private Endpoint — Blob Storage

### 1. Identificación del recurso

- **Servicio de Azure:** Private Endpoint
- **Nombre exacto (nomenclatura):** `pe-st-mvp`
- **Resource Group:** `rg-northwind-mvp-eastus`
- **Ubicación:** Spoke Ops | Región: `eastus` | Ambiente: `mvp`
- **Tipo de recurso Azure:** `microsoft.network/privateendpoints`
- **Recurso destino:** Storage Account `stnorthwindmvp` (sub-resource: `blob`)

### 2. Configuración técnica

- **SKU / tier:** N/A
- **IP privada asignada:** Dinámica (DHCP) — en subnet `snet-private-endpoints-ops`
- **Subnet:** `snet-private-endpoints-ops` en `vnet-spk-ops-northwind-mvp-eastus`
- **Alta disponibilidad:** [x] No Aplica
- **Autoapagado:** [x] No Aplica

### 3. Red y seguridad

- **VNet y Subnet:** `vnet-spk-ops-northwind-mvp-eastus` / `snet-private-endpoints-ops`
- **Asignación de IP Privada:** [x] Dinámica (DHCP)
- **¿Tiene IP pública?** [x] No
- **Enlace privado:** [x] Usa Private DNS Zone — `privatelink.blob.core.windows.net`
  - Registro A: `stnorthwindmvp` → IP privada del endpoint
  - DNS Zone vinculada a: `vnet-hub-northwind-mvp-eastus` y `vnet-spk-ops-northwind-mvp-eastus`

  > **Nota arquitectónica:** Este Private Endpoint está en el spoke Ops y sirve a los containers de ambos departamentos (Ops y Ventas). En producción, el container de Ventas tendría su propio Storage Account con Private Endpoint en `snet-private-endpoints-ventas` dentro del spoke Ventas. El diseño de red (`02-network-design.md`) ya contempla esa subnet reservada.

### 4. Secretos y credenciales

- **¿Usa secretos?** [x] No

### 5. Dependencias

- **Este recurso depende de:** Storage Account `stnorthwindmvp`, subnet `snet-private-endpoints-ops`
- **Otros recursos dependen de este:** App Service `app-ops-northwind-mvp-eastus` (conecta al storage vía VNet Integration → Private Endpoint)
- **Recursos creados junto con este:** NIC, registro A en `privatelink.blob.core.windows.net`

### 6. Tags aplicados

`Project = northwind-mvp` | `Environment = mvp` | `Owner = equipo-cloud-iimas`
`CostCenter = CloudClass` | `Workload = PrivateIntranet` | `Criticality = low`

¿Todos los tags fueron aplicados? [x] Sí

### 7. Pruebas

- **Prueba realizada:** El App Service accede al blob storage exclusivamente a través de la VNet Integration + Private Endpoint. La resolución DNS del hostname `stnorthwindmvp.blob.core.windows.net` desde dentro del App Service apunta a la IP privada del endpoint (verificado por el funcionamiento del endpoint `/api/files` en producción).
- **Resultado:** [x] Exitoso
- **Retos encontrados:** La Private DNS Zone `privatelink.blob.core.windows.net` fue creada automáticamente al crear el Private Endpoint con integración DNS habilitada. Se vinculó correctamente al Hub VNet para resolución desde clientes VPN.

### 8. Datos Técnicos para la Calculadora

- **SKU:** N/A
- **Costo aproximado:** ~$0.01/hora por endpoint + $0.01/GB datos procesados
- **Horas activas al mes:** 730 (24/7)
