# Caso de Negocio

## Cliente

Northwind Distribucion S.A. de C.V.

## Problema

Northwind requiere una intranet corporativa privada para que sus departamentos puedan consultar aplicaciones internas y documentos operativos sin exponer informacion sensible a internet.

Los departamentos iniciales del MVP son:

- Operaciones.
- Ventas, planeado para una fase posterior.

## Objetivo del MVP

Construir una base segura en Azure con arquitectura Hub and Spoke. La primera fase deja lista la red para montar despues VPN, Bastion, aplicaciones privadas, bases de datos, almacenamiento privado y agentes de IA por departamento.

## Valor Esperado

- Aislamiento de cargas por departamento.
- Control centralizado desde el Hub.
- Preparacion para acceso privado mediante VPN Point-to-Site.
- Estandar de naming y tags desde el inicio.
- Base reutilizable para las fases de aplicacion, datos e IA.

## Alcance de Fase 1

Fase 1 no entrega la intranet completa. Solo crea la fundacion:

- Resource Group.
- Hub VNet.
- Spoke VNet de Operaciones.
- Subnets.
- Peering bidireccional.
- Tags.

No se crean servicios con costo horario como VPN Gateway, Bastion, App Service, SQL, Storage o IA.
