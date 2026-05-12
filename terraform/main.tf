/*
  En resource_group_name, hub_vnet_name & spoke_vnet_name usamos los valores de locals.tf
  Aquí se define la Configuración de Red
  El subnetting: 1. en el hub reserva espacios para bastion y gateway y
  2. en el spoke por capas para app, data y el private endpoint
*/

module "foundation" {
  source = "./modules/01-foundation"

  location            = var.location
  resource_group_name = local.names.resource_group

  hub_vnet_name     = local.names.hub_vnet
  hub_address_space = ["10.0.0.0/16"]
  hub_to_spoke_peer = local.names.hub_to_ops_peer

  spoke_vnet_name     = local.names.spoke_ops_vnet
  spoke_address_space = ["10.1.0.0/16"]
  spoke_to_hub_peer   = local.names.ops_to_hub_peer

  sales_vnet_name     = local.names.spoke_sales_vnet
  sales_address_space = ["10.2.0.0/16"]
  hub_to_sales_peer   = local.names.hub_to_sales_peer
  sales_to_hub_peer   = local.names.sales_to_hub_peer

  hub_subnets = {
    snet-management    = "10.0.0.0/24"
    GatewaySubnet      = "10.0.1.0/27"
    AzureBastionSubnet = "10.0.2.0/26"
  }

  spoke_subnets = {
    snet-app-ops               = "10.1.1.0/24"
    snet-data-ops              = "10.1.2.0/24"
    snet-private-endpoints-ops = "10.1.3.0/24"
  }

  sales_subnets = {
    snet-app-ventas               = "10.2.1.0/24"
    snet-data-ventas              = "10.2.2.0/24"
    snet-private-endpoints-ventas = "10.2.3.0/24"
  }

  app_subnet_name       = "snet-app-ops"
  sales_app_subnet_name = "snet-app-ventas"

  tags = local.common_tags
}
