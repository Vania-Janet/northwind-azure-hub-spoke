/* 
  Este archivo normaliza -> en minusculas y sin espacios la variable East US 
  Genera la nomenclatura -> plantilla base con las variables de project, env & location
  Dicccionario de nombres -> estandarización para resource g, hub & spokes 
  Diccionario de tags -> Gobernanza agrupando metadatos.  Al desplegar un recurso solo pasas tags = local.common_tags
*/

locals {
  normalized_location = lower(replace(var.location, " ", ""))
  name_suffix         = "${lower(var.project)}-${lower(var.environment)}-${local.normalized_location}"
  project_tag         = "${lower(var.project)}-${lower(var.environment)}"

  names = {
    resource_group    = "rg-${local.name_suffix}"
    hub_vnet          = "vnet-hub-${local.name_suffix}"
    spoke_ops_vnet    = "vnet-spk-ops-${local.name_suffix}"
    spoke_sales_vnet  = "vnet-spk-ventas-${local.name_suffix}"
    hub_to_ops_peer   = "peer-hub-to-ops-${lower(var.environment)}"
    ops_to_hub_peer   = "peer-ops-to-hub-${lower(var.environment)}"
    hub_to_sales_peer = "peer-hub-to-ventas-${lower(var.environment)}"
    sales_to_hub_peer = "peer-ventas-to-hub-${lower(var.environment)}"
  }

  common_tags = {
    Project     = local.project_tag
    Environment = var.environment
    Owner       = var.owner
    CostCenter  = var.cost_center
    Criticality = var.criticality
    Workload    = var.workload
  }
}
