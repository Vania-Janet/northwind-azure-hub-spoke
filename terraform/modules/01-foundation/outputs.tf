/*
  Este modulo expone los nombres y IDs básicos
  La utilidad de los outputs es sacar esa información al exterior 
*/

output "resource_group_name" {
  description = "Nombre del Resource Group."
  value       = azurerm_resource_group.this.name
}

output "resource_group_id" {
  description = "ID del Resource Group."
  value       = azurerm_resource_group.this.id
}

output "hub_vnet_name" {
  description = "Nombre de la Hub VNet."
  value       = azurerm_virtual_network.hub.name
}

output "hub_vnet_id" {
  description = "ID de la Hub VNet."
  value       = azurerm_virtual_network.hub.id
}

output "spoke_vnet_name" {
  description = "Nombre de la Spoke VNet de Operaciones."
  value       = azurerm_virtual_network.spoke_ops.name
}

output "spoke_vnet_id" {
  description = "ID de la Spoke VNet de Operaciones."
  value       = azurerm_virtual_network.spoke_ops.id
}

output "sales_vnet_name" {
  description = "Nombre de la Spoke VNet de Ventas."
  value       = azurerm_virtual_network.spoke_sales.name
}

output "sales_vnet_id" {
  description = "ID de la Spoke VNet de Ventas."
  value       = azurerm_virtual_network.spoke_sales.id
}

output "hub_subnet_ids" {
  description = "Mapa de IDs de subnets del Hub."
  value       = { for name, subnet in azurerm_subnet.hub : name => subnet.id }
}

output "spoke_subnet_ids" {
  description = "Mapa de IDs de subnets del Spoke Operaciones."
  value       = { for name, subnet in azurerm_subnet.spoke_ops : name => subnet.id }
}

output "sales_subnet_ids" {
  description = "Mapa de IDs de subnets del Spoke Ventas."
  value       = { for name, subnet in azurerm_subnet.spoke_sales : name => subnet.id }
}

output "peering_ids" {
  description = "IDs de los peerings creados."
  value = {
    hub_to_spoke = azurerm_virtual_network_peering.hub_to_spoke.id
    spoke_to_hub = azurerm_virtual_network_peering.spoke_to_hub.id
    hub_to_sales = azurerm_virtual_network_peering.hub_to_sales.id
    sales_to_hub = azurerm_virtual_network_peering.sales_to_hub.id
  }
}
