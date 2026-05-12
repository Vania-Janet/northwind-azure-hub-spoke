# Northwind Azure Hub-Spoke

Proyecto MVP para una landing zone empresarial en Azure para Northwind Distribucion S.A. de C.V.

La Fase 1 prepara solo la base de red:

- Resource Group.
- Hub VNet.
- Spoke VNet de Operaciones.
- Spoke VNet de Ventas.
- Subnets requeridas para administracion, VPN, Bastion, aplicacion, datos y private endpoints.
- Peering Hub <-> Spokes.
- Tags obligatorios para gobierno y costos.

No se crean todavia VPN Gateway, Bastion, App Service, SQL Database, Storage, Private Endpoints ni servicios de IA.

## Caso de Negocio

Northwind necesita una intranet privada para departamentos internos, sin exponer aplicaciones ni datos a internet. La arquitectura objetivo usa un patron Hub and Spoke: el Hub centraliza conectividad y servicios compartidos, mientras que cada Spoke aloja cargas departamentales aisladas.

Esta primera fase deja lista la red base para que el equipo pueda montar encima los componentes de aplicacion, datos, seguridad, VPN y RAG en fases posteriores.

## Region

La region objetivo del MVP es `eastus`.

## Tags Obligatorios

Todos los recursos de Fase 1 reciben estos tags:

| Tag | Valor |
| --- | --- |
| Project | northwind-mvp |
| Environment | mvp |
| Owner | equipo-cloud-iimas |
| CostCenter | CloudClass |
| Criticality | low |
| Workload | PrivateIntranet |

## Estructura de Fase 1

```text
terraform/
  providers.tf
  variables.tf
  locals.tf
  main.tf
  outputs.tf
  terraform.tfvars.example
  modules/
    01-foundation/
```

## Como Correr Terraform

Desde `northwind-azure-hub-spoke/terraform`:

```bash
terraform init
terraform fmt -recursive
terraform validate
terraform plan -out=tfplan
```

Cuando el plan este revisado y aprobado:

```bash
terraform apply tfplan
```

Importante: no ejecutes `terraform apply` hasta confirmar que quieres crear recursos en Azure.

## Costos de Fase 1

La Fase 1 crea Resource Group, VNets, subnets y peering. Estos recursos no tienen costo fijo mensual mientras estan ociosos. Azure Virtual Network no tiene cargo por crear la VNet, pero el VNet Peering puede cobrar por trafico de entrada y salida entre redes.

Estimacion practica para Fase 1:

- Sin trafico entre Hub y Spokes: aproximadamente `USD 0/mes`.
- Con pruebas ligeras de conectividad: normalmente centavos, dependiendo del volumen de GB transferidos por peering.
- Sin VPN Gateway, Bastion, App Service, SQL, Storage ni IA: no hay cargos horarios relevantes en esta fase.

Puedes dejar esta fase viva durante dias o semanas con costo cercano a cero, siempre que no agregues servicios con cobro horario ni generes trafico significativo entre VNets.
