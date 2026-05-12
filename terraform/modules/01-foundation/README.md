# Module 01 - Foundation

Modulo Terraform para la base de infraestructura de Fase 1.

## Recursos

- Resource Group.
- Hub VNet.
- Spoke VNet de Operaciones.
- Spoke VNet de Ventas.
- Subnets del Hub:
  - `snet-management`
  - `GatewaySubnet`
  - `AzureBastionSubnet`
- Subnets del Spoke:
  - `snet-app-ops`
  - `snet-data-ops`
  - `snet-private-endpoints-ops`
- Subnets del Spoke Ventas:
  - `snet-app-ventas`
  - `snet-data-ventas`
  - `snet-private-endpoints-ventas`
- VNet Peering bidireccional.

## Decisiones

- El Hub usa `10.0.0.0/16`.
- El Spoke de Operaciones usa `10.1.0.0/16`.
- El Spoke de Ventas usa `10.2.0.0/16`.
- `GatewaySubnet` y `AzureBastionSubnet` se reservan desde Fase 1, pero no se crean VPN Gateway ni Bastion todavia.
- `snet-app-ops` y `snet-app-ventas` se dejan delegadas a `Microsoft.Web/serverFarms` para facilitar App Service VNet Integration en una fase posterior.
- Los peerings no habilitan gateway transit en Fase 1 porque el VPN Gateway aun no existe.

## Entradas Principales

- `resource_group_name`
- `location`
- `hub_vnet_name`
- `spoke_vnet_name`
- `hub_subnets`
- `spoke_subnets`
- `tags`

## Outputs

- IDs y nombres de Resource Group, VNets y subnets.
- IDs de los peerings.
