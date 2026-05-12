# Diseno de Red

## Direccionamiento

| Red / Subnet | CIDR | Uso |
| --- | --- | --- |
| Hub VNet | 10.0.0.0/16 | Red central de servicios compartidos |
| snet-management | 10.0.0.0/24 | Administracion y servicios compartidos futuros |
| GatewaySubnet | 10.0.1.0/27 | Reservada para VPN Gateway |
| AzureBastionSubnet | 10.0.2.0/26 | Reservada para Azure Bastion |
| Spoke Operaciones VNet | 10.1.0.0/16 | Recursos del departamento de Operaciones |
| snet-app-ops | 10.1.1.0/24 | Aplicacion privada en fase posterior |
| snet-data-ops | 10.1.2.0/24 | Datos privados en fase posterior |
| snet-private-endpoints-ops | 10.1.3.0/24 | Private Endpoints |
| Spoke Ventas VNet | 10.2.0.0/16 | Recursos del departamento de Ventas |
| snet-app-ventas | 10.2.1.0/24 | Aplicacion privada en fase posterior |
| snet-data-ventas | 10.2.2.0/24 | Datos privados en fase posterior |
| snet-private-endpoints-ventas | 10.2.3.0/24 | Private Endpoints |

## Nombres de Recursos

| Recurso | Nombre |
| --- | --- |
| Resource Group | rg-northwind-mvp-eastus |
| Hub VNet | vnet-hub-northwind-mvp-eastus |
| Spoke Operaciones VNet | vnet-spk-ops-northwind-mvp-eastus |
| Spoke Ventas VNet | vnet-spk-ventas-northwind-mvp-eastus |
| Peering Hub -> Ops | peer-hub-to-ops-mvp |
| Peering Ops -> Hub | peer-ops-to-hub-mvp |
| Peering Hub -> Ventas | peer-hub-to-ventas-mvp |
| Peering Ventas -> Hub | peer-ventas-to-hub-mvp |

## Reglas de Fase 1

- No hay peering directo entre Operaciones y Ventas; ambos se conectan solo con el Hub.
- No se crean gateways, firewalls, private endpoints ni rutas UDR en esta fase.
- Las subnets reservadas respetan los nombres requeridos por Azure:
  - `GatewaySubnet`.
  - `AzureBastionSubnet`.
- No se asignan IPs publicas.
- Los tags se aplican a Resource Group y VNets.

## Subnets para Companeros

| Equipo / Persona | Subnet asignada | Uso posterior |
| --- | --- | --- |
| Network / VPN | GatewaySubnet | VPN Gateway P2S |
| Network / Bastion | AzureBastionSubnet | Bastion |
| App Service | snet-app-ops | Integracion privada de App Service |
| Data / Storage | snet-data-ops | Servicios de datos privados |
| Private Link | snet-private-endpoints-ops | Private Endpoints |
| App Service Ventas | snet-app-ventas | Integracion privada de App Service |
| Data / Storage Ventas | snet-data-ventas | Servicios de datos privados |
| Private Link Ventas | snet-private-endpoints-ventas | Private Endpoints |
