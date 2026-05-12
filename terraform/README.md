# Terraform - Fase 1 Foundation

Esta carpeta contiene la infraestructura base de red para el MVP `northwind`.

## Alcance

Incluido en Fase 1:

- Resource Group.
- Hub VNet `10.0.0.0/16`.
- Spoke Operaciones VNet `10.1.0.0/16`.
- Spoke Ventas VNet `10.2.0.0/16`.
- Subnets del Hub.
- Subnets del Spoke Operaciones.
- Subnets del Spoke Ventas.
- Peering Hub -> Spoke Operaciones.
- Peering Spoke Operaciones -> Hub.
- Peering Hub -> Spoke Ventas.
- Peering Spoke Ventas -> Hub.
- Tags comunes.

Excluido de Fase 1:

- VPN Gateway.
- Azure Bastion host.
- App Service.
- SQL Database.
- Storage Account.
- Private Endpoints.
- Private DNS Zones.
- Azure OpenAI / AI Search.

## Uso

1. Copia el archivo de ejemplo:

```bash
cp terraform.tfvars.example terraform.tfvars
```

2. Revisa valores en `terraform.tfvars`.

3. Ejecuta validacion:

```bash
terraform init
terraform fmt -recursive
terraform validate
terraform plan -out=tfplan
```

4. Aplica solo cuando se confirme la creacion de recursos:

```bash
terraform apply tfplan
```

## Autenticacion

Terraform usa el provider `azurerm`. Puedes autenticar con Azure CLI o con variables `ARM_*`.

Variables esperadas si usas service principal:

```bash
export ARM_CLIENT_ID="..."
export ARM_CLIENT_SECRET="..."
export ARM_TENANT_ID="..."
export ARM_SUBSCRIPTION_ID="..."
```

No guardes secretos reales en este repositorio.
