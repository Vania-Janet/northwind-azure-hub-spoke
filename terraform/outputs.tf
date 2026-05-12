output "resource_group_name" {
  description = "Nombre del Resource Group de Fase 1."
  value       = module.foundation.resource_group_name
}

output "resource_group_id" {
  description = "ID del Resource Group de Fase 1."
  value       = module.foundation.resource_group_id
}

output "hub_vnet_name" {
  description = "Nombre de la Hub VNet."
  value       = module.foundation.hub_vnet_name
}

output "hub_vnet_id" {
  description = "ID de la Hub VNet."
  value       = module.foundation.hub_vnet_id
}

output "spoke_ops_vnet_name" {
  description = "Nombre de la Spoke VNet de Operaciones."
  value       = module.foundation.spoke_vnet_name
}

output "spoke_ops_vnet_id" {
  description = "ID de la Spoke VNet de Operaciones."
  value       = module.foundation.spoke_vnet_id
}

output "spoke_sales_vnet_name" {
  description = "Nombre de la Spoke VNet de Ventas."
  value       = module.foundation.sales_vnet_name
}

output "spoke_sales_vnet_id" {
  description = "ID de la Spoke VNet de Ventas."
  value       = module.foundation.sales_vnet_id
}

output "hub_subnet_ids" {
  description = "Mapa de IDs de subnets del Hub."
  value       = module.foundation.hub_subnet_ids
}

output "spoke_ops_subnet_ids" {
  description = "Mapa de IDs de subnets del Spoke Operaciones."
  value       = module.foundation.spoke_subnet_ids
}

output "spoke_sales_subnet_ids" {
  description = "Mapa de IDs de subnets del Spoke Ventas."
  value       = module.foundation.sales_subnet_ids
}

output "peering_ids" {
  description = "IDs de los peerings Hub <-> Spoke."
  value       = module.foundation.peering_ids
}
