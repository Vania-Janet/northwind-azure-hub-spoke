variable "project" {
  description = "Nombre corto del proyecto usado para naming y tags."
  type        = string
  default     = "northwind"
}

variable "environment" {
  description = "Ambiente de despliegue."
  type        = string
  default     = "mvp"

  validation {
    condition     = contains(["dev", "staging", "prod", "mvp"], var.environment)
    error_message = "environment debe ser dev, staging, prod o mvp."
  }
}

variable "location" {
  description = "Region Azure para la Fase 1."
  type        = string
  default     = "eastus"
}

variable "owner" {
  description = "Responsable del proyecto o equipo."
  type        = string
  default     = "equipo-cloud-iimas"
}

variable "cost_center" {
  description = "Centro de costo."
  type        = string
  default     = "CloudClass"
}

variable "criticality" {
  description = "Criticidad del workload."
  type        = string
  default     = "low"

  validation {
    condition     = contains(["low", "medium", "high", "critical"], var.criticality)
    error_message = "criticality debe ser low, medium, high o critical."
  }
}

variable "workload" {
  description = "Nombre funcional del workload."
  type        = string
  default     = "PrivateIntranet"
}
