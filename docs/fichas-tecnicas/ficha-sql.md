# Ficha Técnica — Azure SQL (Persona 3)

- **Responsable:** Luis Enrique Morales Flores
- **Área del proyecto:** App / Base de datos

---

## Recurso 1: Azure SQL Server (servidor lógico)

### 1. Identificación del recurso

- **Servicio de Azure:** Azure SQL Server (servidor lógico)
- **Nombre exacto (nomenclatura):** `sql-northwind-mvp-eastus`
- **Azure Resource ID:** `/subscriptions/26ae16d4-2f67-45f7-9d46-6c02d925cf48/resourceGroups/rg-northwind-mvp-eastus/providers/Microsoft.Sql/servers/sql-northwind-mvp-eastus`
- **Resource Group:** `rg-northwind-mvp-eastus`
- **Ubicación:** Región: `centralus` | Ambiente: `mvp`

  > ⚠️ Nota: El servidor fue creado en Central US porque la suscripción no tenía cuota disponible para Azure SQL en East US en el momento de la creación. El nombre conserva el sufijo `eastus` por convención del equipo. El Private Endpoint (`pe-sql-ops-mvp-eastus`) está en East US, conectando el servidor cross-region.
- **Tipo de recurso Azure:** `microsoft.sql/servers`

  > ⚠️ Nota: El servidor fue creado en Central US porque la suscripción no tenía cuota disponible para Azure SQL en East US. El Private Endpoint (`pe-sql-ops-mvp-eastus`) está en East US, conectando el servidor cross-region.

### 2. Configuración técnica

- **SKU / tier:** N/A (el servidor lógico no tiene SKU propio; pertenece a la base de datos)
- **Para SQL (Modelo de compra):** [x] No Aplica (aplica al recurso Database)
- **Para Storage (Tipo de servicio):** [x] No Aplica
- **Redundancia:** [x] No Aplica
- **Alta disponibilidad:** [x] No
- **Autoapagado configurado:** [x] No Aplica (el serverless de la DB tiene auto-pause)

### 3. Red y seguridad

- **VNet y Subnet asignada:** N/A (el servidor lógico no se integra a VNet directamente)
- **Asignación de IP Privada:** [x] No Aplica (la IP privada es del Private Endpoint)
- **¿Tiene IP pública?** [x] No — acceso público deshabilitado. Acceso únicamente vía Private Endpoint.
- **Aislamiento:** [x] Public network access: Disabled
- **Enlace privado:** [x] Usa Private Endpoint — `pe-sql-ops-mvp-eastus`
- **¿Usa Managed Identity?** [x] No — autenticación SQL (usuario + contraseña)

### 4. Secretos y credenciales

- **¿Usa secretos?** [x] Sí
- **Dónde están guardados:** [x] App Service Configuration (Application Settings) del App Service `app-ops-northwind-mvp-eastus`
- **Variables configuradas:**
  - `AZURE_SQL_SERVER` = FQDN del servidor (`sql-northwind-mvp-eastus.database.windows.net`)
  - `AZURE_SQL_DATABASE` = `sqldb-ops-mvp`
  - `AZURE_SQL_USER` = (usuario SQL administrador)
  - `AZURE_SQL_PASSWORD` = (contraseña SQL)

### 5. Dependencias

- **Este recurso depende de:** Resource Group `rg-northwind-mvp-eastus`
- **Otros recursos dependen de este:** Base de datos `sqldb-ops-mvp`, Private Endpoint `pe-sql-ops-mvp-eastus`
- **Recursos dependientes creados junto con este:** Base de datos `sqldb-ops-mvp`

### 6. Tags aplicados

`Project = northwind-mvp` | `Environment = mvp` | `Owner = equipo-cloud-iimas`
`CostCenter = CloudClass` | `Workload = PrivateIntranet` | `Criticality = low`

¿Todos los tags fueron aplicados? [x] Sí

### 7. Pruebas

- **Prueba realizada:** Conexión desde App Service a través de Private Endpoint. Verificación con endpoint `/health/sql` que prueba conexión, INSERT y SELECT a tabla `chat_history`.
- **Resultado:** [x] Exitoso
- **Retos encontrados y cómo se resolvió:**
  1. **East US no disponible para SQL:** La suscripción no tenía cuota para SQL en East US. Se creó en Central US con Private Endpoint cross-region en East US spoke VNet.
  2. **pyodbc no disponible en Linux App Service:** `pyodbc` requiere el driver ODBC de Microsoft que no está instalado en App Service Linux. Se resolvió cambiando a `pymssql==2.3.1`, que usa el protocolo TDS directamente sin drivers nativos.
  3. **Parámetros pymssql:** `cursor.execute()` de pymssql requiere los parámetros como tupla y usa `%s`/`%d` como placeholders (no `?` como pyodbc). El error `execute() takes at most 2 positional arguments` fue silenciado por `except Exception: pass`. Se corrigió la sintaxis en `database.py`.

### 8. Datos Técnicos para la Calculadora

- **SKU:** N/A (servidor lógico)
- **Costo aproximado:** N/A (ver base de datos)
- **Horas activas al mes:** N/A

---

## Recurso 2: Azure SQL Database

### 1. Identificación del recurso

- **Servicio de Azure:** Azure SQL Database
- **Nombre exacto (nomenclatura):** `sqldb-ops-mvp`
- **Azure Resource ID:** `/subscriptions/26ae16d4-2f67-45f7-9d46-6c02d925cf48/resourceGroups/rg-northwind-mvp-eastus/providers/Microsoft.Sql/servers/sql-northwind-mvp-eastus/databases/sqldb-ops-mvp`
- **Resource Group:** `rg-northwind-mvp-eastus`
- **Ubicación:** Región: `centralus` (mismo servidor lógico) | Ambiente: `mvp`
- **Tipo de recurso Azure:** `microsoft.sql/servers/databases`

### 2. Configuración técnica

- **SKU / tier:** General Purpose — Serverless Gen5, 2 vCores
- **Para SQL (Modelo de compra):** [x] vCore (modelo serverless)
- **Almacenamiento máximo:** 32 GB (mínimo configurado)
- **Auto-pause:** [x] Sí — se pausa tras 1 hora de inactividad (reduce costo)
- **Redundancia:** Locally Redundant (LRS)
- **Alta disponibilidad:** [x] No (MVP)
- **Autoapagado configurado:** [x] Sí — auto-pause serverless

### 3. Red y seguridad

- **VNet y Subnet asignada:** N/A (la conectividad privada es vía Private Endpoint del servidor lógico)
- **Asignación de IP Privada:** [x] No Aplica
- **¿Tiene IP pública?** [x] No (heredado del servidor lógico con acceso público deshabilitado)
- **Aislamiento:** [x] Acceso solo vía Private Endpoint
- **Enlace privado:** [x] Usa Private Endpoint del servidor lógico
- **¿Usa Managed Identity?** [x] No

### 4. Secretos y credenciales

- **¿Usa secretos?** [x] No (las credenciales están en el servidor lógico)

### 5. Dependencias

- **Este recurso depende de:** Servidor lógico `sql-northwind-mvp-eastus`
- **Otros recursos dependen de este:** App Service `app-ops-northwind-mvp-eastus` (tabla `chat_history` para historial de conversaciones)
- **Recursos creados junto con este:** Ninguno

### 6. Tags aplicados

`Project = northwind-mvp` | `Environment = mvp` | `Owner = equipo-cloud-iimas`
`CostCenter = CloudClass` | `Workload = PrivateIntranet` | `Criticality = low`

¿Todos los tags fueron aplicados? [x] Sí

### 7. Pruebas

- **Prueba realizada:** Verificación de persistencia de historial de chat: mensajes enviados desde la UI persisten al cerrar y reabrir el browser. Endpoint `/health/sql` confirma INSERT y SELECT exitosos en tabla `chat_history`.
- **Resultado:** [x] Exitoso
- **Retos encontrados y cómo se resolvió:** Ver retos del Recurso 1 (servidor lógico).

### 8. Datos Técnicos para la Calculadora

- **SKU:** General Purpose — Serverless Gen5, 2 vCores
- **Precio:** Pay-per-use (por vCore-segundo cuando activa). ~$0.000145/vCore-segundo. Con auto-pause, costo mínimo.
- **Horas activas al mes:** Variable (serverless con auto-pause; estimado bajo para MVP)
- **Almacenamiento:** 32 GB (~$0.115/GB/mes)

---

## Recurso 3: Private Endpoint — SQL Server

### 1. Identificación del recurso

- **Servicio de Azure:** Private Endpoint
- **Nombre exacto (nomenclatura):** `pe-sql-ops-mvp-eastus`
- **Resource Group:** `rg-northwind-mvp-eastus`
- **Ubicación:** Spoke Ops | Región: `eastus` | Ambiente: `mvp`
- **Tipo de recurso Azure:** `microsoft.network/privateendpoints`
- **Recurso destino:** SQL Server `sql-northwind-mvp-eastus` (sub-resource: `sqlServer`)

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
- **Enlace privado:** [x] Usa Private DNS Zone — `privatelink.database.windows.net`
  - Registro A: `sql-northwind-mvp-eastus` → IP privada del endpoint
  - DNS Zone vinculada a: `vnet-hub-northwind-mvp-eastus` y `vnet-spk-ops-northwind-mvp-eastus`

  > ⚠️ Nota: El Private Endpoint está en East US pero apunta a un servidor SQL en Central US (cross-region). Azure soporta esta configuración.

### 4. Secretos y credenciales

- **¿Usa secretos?** [x] No

### 5. Dependencias

- **Este recurso depende de:** SQL Server `sql-northwind-mvp-eastus`, subnet `snet-private-endpoints-ops`
- **Otros recursos dependen de este:** App Service `app-ops-northwind-mvp-eastus` (conecta a SQL vía VNet Integration → Private Endpoint)
- **Recursos creados junto con este:** NIC, registro A en `privatelink.database.windows.net`

### 6. Tags aplicados

`Project = northwind-mvp` | `Environment = mvp` | `Owner = equipo-cloud-iimas`
`CostCenter = CloudClass` | `Workload = PrivateIntranet` | `Criticality = low`

¿Todos los tags fueron aplicados? [x] Sí

### 7. Pruebas

- **Prueba realizada:** App Service conecta exitosamente al SQL a través del Private Endpoint. Verificado con `/health/sql` (INSERT + SELECT exitoso desde la red privada).
- **Resultado:** [x] Exitoso
- **Retos encontrados:** Cross-region private endpoint (SQL en Central US, PE en East US) — Azure soporta nativamente esta configuración sin configuración adicional.

### 8. Datos Técnicos para la Calculadora

- **SKU:** N/A
- **Costo aproximado:** ~$0.01/hora por endpoint + $0.01/GB datos procesados
- **Horas activas al mes:** 730 (24/7)
