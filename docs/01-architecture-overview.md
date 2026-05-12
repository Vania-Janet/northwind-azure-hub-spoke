# Arquitectura General

## Patron Hub and Spoke

La arquitectura usa un patron Hub and Spoke. El Hub concentra servicios compartidos de conectividad, seguridad, resolucion privada y administracion. Cada Spoke aloja cargas departamentales aisladas.

En la base actual se implementan dos Spokes departamentales: Operaciones y Ventas.

```text
Hub VNet 10.0.0.0/16
  |
  | VNet Peering
  |
Spoke Operaciones VNet 10.1.0.0/16
  |
  | Spoke aislado adicional
  |
Spoke Ventas VNet 10.2.0.0/16
```

## Hub

El Hub reserva subnets para:

| Subnet | CIDR | Uso |
| --- | --- | --- |
| snet-management | 10.0.0.0/24 | Administracion, Key Vault y monitoreo en fases posteriores |
| GatewaySubnet | 10.0.1.0/27 | VPN Gateway en fase posterior |
| AzureBastionSubnet | 10.0.2.0/26 | Azure Bastion en fase posterior |

En esta fase no se crea VPN Gateway ni Bastion. Solo se reservan las subnets requeridas por Azure para evitar redisenos posteriores.

## Spoke Operaciones

El Spoke de Operaciones reserva subnets para:

| Subnet | CIDR | Uso |
| --- | --- | --- |
| snet-app-ops | 10.1.1.0/24 | App Service VNet Integration en fase posterior |
| snet-data-ops | 10.1.2.0/24 | Cargas de datos privadas en fase posterior |
| snet-private-endpoints-ops | 10.1.3.0/24 | Private Endpoints de SQL, Storage y otros servicios |

El Spoke de Ventas reserva subnets equivalentes:

| Subnet | CIDR | Uso |
| --- | --- | --- |
| snet-app-ventas | 10.2.1.0/24 | App Service VNet Integration en fase posterior |
| snet-data-ventas | 10.2.2.0/24 | Cargas de datos privadas en fase posterior |
| snet-private-endpoints-ventas | 10.2.3.0/24 | Private Endpoints de SQL, Storage y otros servicios |

`snet-app-ops` y `snet-app-ventas` quedan delegadas a `Microsoft.Web/serverFarms` para preparar App Service sin crear todavia el servicio.

## Peering

Se crean dos peerings:

- Hub -> Spoke Operaciones.
- Spoke Operaciones -> Hub.
- Hub -> Spoke Ventas.
- Spoke Ventas -> Hub.

El gateway transit queda deshabilitado en Fase 1 porque el VPN Gateway aun no existe. Se habilitara en una fase posterior cuando se cree el gateway en el Hub.

## Seguridad

La Fase 1 no expone aplicaciones, bases de datos ni almacenamiento. Tampoco crea IPs publicas. La red queda preparada para que las siguientes fases agreguen controles privados de acceso.
