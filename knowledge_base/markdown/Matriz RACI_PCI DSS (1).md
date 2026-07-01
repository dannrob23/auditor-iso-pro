## Hoja: Información

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Matriz RACI por requerimiento PCI DSS |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
| 1  Control de Versiones |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
| Versión | Realizado por | Fecha | Revisado por | Fecha | Aprobado por | Fecha | Descripción del cambio |
| 1.0 |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
| 1.1 |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
| 1.2 |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |

---

## Hoja: Instructivo

| RACI |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R - Responsible
 Son responsables del trabajo o de tomar la decisión. Puede tener más de una persona responsable de una tarea, pero para que el proceso de toma de decisiones sea efectivo, intente tener una persona responsable de una sola tarea. | A - Accountable
La persona propietaria de la tarea o entregable. Puede que ellos mismos no hagan el trabajo, pero sí es
responsable de asegurarse de que esté finalizado. Para evitar confusiones y la difusión de responsabilidades, es mejor tener una persona responsable por tarea del proyecto. |  |  |  |  |  |  |  |  |  |  |  |  |
| C - Consulted
La persona, rol o grupo que ayudará a completar la tarea. Tendrán comunicación bidireccional con el
personas responsables de la tarea proporcionando aportes y retroalimentación
sobre la finalización de la tarea. | I - Informed
Las personas, roles o grupos que necesitan estar actualizados sobre el progreso de la tarea. No tendrán comunicación bidireccional, pero es fundamental mantenerlos informados ya que se verán afectados por el resultado final de la tarea/proyecto. |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Instrucciones:
1. Ubiquese en cada requerimiento
2. Defina los roles de cada una de sus partes interesadas para cada tarea del requeirmiento seleccionando R, A, C o I en el menú desplegable. Ingrese el cargo de sus roles en cada raci.
4. Una vez completado, preste atención a las personas que asumen la responsabilidad de las tareas y capacitelas. |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## Hoja: 1

| #VALUE! | Matriz RACI por requerimiento PCI DSS |  |  |  |  | Código:  | AN-XX |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | Version: | 1 |
|  |  |  |  |  |  |  |  |
| Requisito/Responsable | Requerimiento | Actividad | R | A | C | I | Entregable/Documento |
| Requisito 1: Instalar y Mantener los Controles de Seguridad de la Red | 1.1 Se definen y comprenden los procesos y mecanismos para instalar y mantener los controles de seguridad de la red. | 1.1.1 Todas las políticas de seguridad y procedimientos operativos que se identifican en el Requisito 1 son: 
•	 Documentados.
•	 Actualizados.
•	 En uso.
•	 Conocidos por todas las partes involucradas.
 |  |  |  |  |  |
|  |  | 1.1.2 Los roles y responsabilidades para realizar las actividades del Requisito 1 están documentados, asignados y comprendidos.  |  |  |  |  |  |
|  | 1.2 Se configuran y mantienen los controles de seguridad de la red (NSC). | 1.2.1 Los estándares de configuración para el conjunto de reglas de los NSC son:
•	 Definidos.
•	 Implementados.
•	 Mantenido. |  |  |  |  |  |
|  |  | 1.2.2 Todos los cambios en las conexiones de red y en las configuraciones de los NSC se aprueban y gestionan de acuerdo con el proceso de control de cambios definido en el Requisito 6.5.1.
Notas de Aplicabilidad
Los cambios en las conexiones de red incluyen la adición, eliminación o modificación de una conexión. 
Los cambios en las configuraciones del NSC incluyen aquellos relacionados con el propio componente, así como los que afectan la forma en que realiza su función de seguridad.
 |  |  |  |  |  |
|  |  | 1.2.3 Se mantiene un diagrama de red precisos que muestra todas las conexiones entre el CDE y otras redes, incluyendo las redes inalámbricas.
Notas de Aplicabilidad
Se puede utilizar un(os) diagrama(s) de red vigente(s) u otra solución técnica o topológica que identifique las conexiones y dispositivos en la red para cumplir con este requisito. |  |  |  |  |  |
|  |  | 1.2.4 Se mantienen diagramas de flujo de datos precisos que cumplen con lo siguiente:  
•	 Muestran todos los flujos de datos de tarjetahabientes a través de sistemas y redes.
•	 Se actualizan según sea necesario ante cambios en el entorno.
Notas de Aplicabilidad
Se puede utilizar un diagrama de flujo de datos u otra solución técnica o topológica que identifique los flujos de datos de tarjetahabientes a través de sistemas y redes para cumplir con este requisito. |  |  |  |  |  |
|  |  | 1.2.5 Todos los servicios, protocolos y puertos permitidos están identificados, aprobados y tienen una necesidad de negocio definida. |  |  |  |  |  |
|  |  | 1.2.6 Las configuraciones de seguridad son definidas e implementadas para todos los servicios, protocolos y puertos que están en uso y que son considerados inseguros, de tal manera que el riesgo es mitigado.  |  |  |  |  |  |
|  |  | 1.2.7 Las configuraciones de los NSC se revisan al menos una vez cada seis meses para confirmar que son relevantes y eficientes.  |  |  |  |  |  |
|  |  | 1.2.8 Los archivos de configuración de los NSC están: 
•	 Asegurados contra el acceso no autorizado. 
•	 Se mantienen consistentes con las configuraciones de red activas. 
Notas de Aplicabilidad
Cualquier archivo o ajuste utilizado para configurar o sincronizar los NSC se considera un “archivo de configuración.” Esto incluye archivos, controles automatizados y basados en el sistema, scripts, configuraciones, infraestructura como código u otros parámetros de los que se hace una copia de seguridad, se archivan o se almacenan de forma remota. |  |  |  |  |  |
|  | 1.3 El acceso a la red hacia y desde el entorno de datos de tarjetahabientes está restringido. | 1.3.1 El tráfico de entrada al CDE está restringido de la siguiente manera: 
•	 Sólo el tráfico que sea necesario, 
•	 Todo el resto del tráfico está específicamente denegado. |  |  |  |  |  |
|  |  | 1.3.2 El tráfico saliente del CDE se restringe de la siguiente manera: 
•	 Sólo al tráfico necesario.
•	 Todo el resto del tráfico está específicamente denegado. |  |  |  |  |  |
|  |  | 1.3.3 Los NSC se implementan entre todas las redes inalámbricas y el CDE; esto es independientemente de que la red inalámbrica sea parte CDE o no, de manera que: 
•	 Todo el tráfico inalámbrico de las redes inalámbricas hacia el CDE es denegado de forma explícita.
•	 Sólo se permite el tráfico inalámbrico al CDE que tenga un propósito de negocio autorizado. |  |  |  |  |  |
|  | 1.4 Se controlan las conexiones de red entre las redes fiables y las que no lo son. | 1.4.1 Los NSC se implementan entre redes confiables y no confiables. |  |  |  |  |  |
|  |  | 1.4.2 El tráfico entrante de redes que no son confiables a redes confiables está restringido a: 
•	 Las comunicaciones con componentes del sistema autorizados para proveer servicios de acceso público, protocolos y puertos.
•	 Respuestas las comunicaciones previamente iniciadas por componentes del sistema en una red confiable, esto para protocolos con dicho comportamiento.
•	 Todo el tráfico restante está denegado.
Notas de Aplicabilidad
La intención de este requisito es abordar las sesiones de comunicación entre redes fiables y no fiables, en lugar de las especificaciones de los protocolos.
Este requisito no limita el uso de UDP u otros protocolos de red no orientados a conexión si el comportamiento estándar del estado de la conexión del protocolo es mantenido y bajo el control del NSC. |  |  |  |  |  |
|  |  | 1.4.3 Se implementan medidas Antispoofing para detectar y bloquear la entrada a la red confiable de direcciones IP origen falsas o suplantadas. |  |  |  |  |  |
|  |  | 1.4.4 Los componentes del sistema que almacenan datos de tarjetahabientes no son accesibles directamente desde redes no confiables.
Notas de Aplicabilidad
Este requisito no se aplica al almacenamiento de datos de tarjetahabientes en memoria volátil, pero sí se aplica cuando la memoria se trata como almacenamiento persistente (por ejemplo, disco RAM). Los datos de tarjetahabientes sólo pueden almacenarse en la memoria volátil durante el tiempo necesario para apoyar el proceso de negocio asociado (por ejemplo, hasta la finalización transacción relacionada con tarjeta de pago). |  |  |  |  |  |
|  |  | 1.4.5 La divulgación de las direcciones IP internas y la información de enrutamiento se limita sólo a las partes autorizadas. |  |  |  |  |  |
|  | 1.5 Se mitigan los riesgos para el CDE desde dispositivos informáticos que pueden conectarse tanto a redes no confiables como al CDE. | 1.5.1 Los controles de seguridad se implementan en cualquier dispositivo informático, incluyendo los dispositivos propiedad de la empresa y de los empleados, que se conectan tanto a redes no confiables (incluida Internet) como al CDE manera siguiente. 
•	 Se definen los parámetros de configuración específicos para impedir que se introduzcan amenazas en la red de la entidad. 
•	 Los controles de seguridad se están ejecutando activamente.
•	 Los usuarios de los dispositivos informáticos no pueden alterar los controles de seguridad a menos que estén específicamente documentados y autorizados por el nivel gerencial, caso por caso, durante un período limitado.
Notas de Aplicabilidad
Estos controles de seguridad pueden desactivarse temporalmente solo si existe una necesidad técnica legítima, según lo autorizado por el nivel gerencial caso por caso. Se requiere de una autorización formal para desactivar estos controles de seguridad para y bajo un propósito específico. También puede ser necesario implementar medidas de seguridad adicionales durante el período durante el cual los controles de seguridad estén desactivados.
Este requisito aplica a los dispositivos informáticos que sean propiedad tanto de la compañía como de los empleados. Los sistemas que no pueden ser administrados por políticas corporativas introducen debilidades y brindan oportunidades para que personas malintencionadas pueden explotarlas y/o aprovecharlas.  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |

---

## Hoja: 2

|  | Matriz RACI por requerimiento PCI DSS |  |  |  |  | Código:  | AN-XX |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | Version: | 1 |
|  |  |  |  |  |  |  |  |
| Requisito/Responsable | Requerimiento | Actividad | R | A | C | I | Entregable/Documento |
| Requisito 2: Aplicar Configuraciones Seguras a Todos los Componentes del Sistema | 2.1 Se definen y comprenden los procesos y mecanismos para aplicar configuraciones seguras a todos los componentes del sistema. | 2.1.1Todas las políticas de seguridad y procedimientos operativos que se identifican en el Requisito 2 están: 
•	 Documentados.
•	 Actualizados.
•	 En uso.
•	 Conocidos por todas las partes involucradas.  |  |  |  |  |  |
|  |  | 2.1.2 Los roles y responsabilidades para realizar las actividades del Requisito 2 están documentados, asignados y comprendidos. 
Nuevo requisito - efectivo inmediatamente
 |  |  |  |  |  |
|  | 2.2 Los componentes del sistema se configuran y administran de forma segura. | 2.2.1 Las estándares de configuración se desarrollan, implementan y mantienen para:
•	 Cubrir todos los componentes del sistema.
•	 Cubrir todas las vulnerabilidades de seguridad conocidas. 
•	 Brindar coherencia con los estándares de hardening del sistema aceptados por el sector o con las recomendaciones de hardening del proveedor. 
•	 Ser actualizadas a medida que se identifican nuevos problemas de vulnerabilidad, como se define en el Requisito 6.3.1.
•	 Ser aplicadas cuando los nuevos sistemas sean configurados y verificadas como establecidas antes o inmediatamente después de que un componente del sistema se conecte a un entorno de producción. |  |  |  |  |  |
|  |  | 2.2.2 Las cuentas predeterminadas del proveedor se gestionan de la siguiente manera:
•	 Si se utilizan las cuentas predeterminadas del proveedor, la contraseña predeterminada se cambia según el Requisito 8.3.6.
•	 Si no se van a utilizar las cuentas predeterminadas del proveedor, la cuenta se elimina o se desactiva.
Notas de Aplicabilidad
Esto se aplica a TODAS las cuentas y contraseñas predeterminadas del proveedor, incluidas, entre otras, las utilizadas por los sistemas operativos, el software que proporciona servicios de seguridad, las cuentas de aplicaciones y sistemas, los terminales de punto de venta (POS), las aplicaciones de pago y los valores predeterminadas del Simple Network Management Protocol (SNMP).
Este requisito también se aplica cuando un componente del sistema no está instalado en el entorno de una entidad, por ejemplo, el software y las aplicaciones que forman parte del CDE y a las que se ingresa a través de un servicio de suscripción en la nube. |  |  |  |  |  |
|  |  | 2.2.3 Las funciones principales que requieren distintos niveles de seguridad se manejan como sigue: 
•	 Solo existe una función principal en un componente del sistema,
O
•	 Las funciones principales con distintos niveles de seguridad que existen en el mismo componente del sistema están aisladas entre sí,
O
•	 Las funciones primarias con distintos niveles de seguridad en el mismo componente del sistema están todas aseguradas al nivel requerido por la función que requiera un nivel mayor de seguridad. |  |  |  |  |  |
|  |  | 2.2.4 Sólo se habilitan los servicios, protocolos, «demonios» y funciones necesarias, y se eliminan o deshabilitan todas las funciones innecesarias.  |  |  |  |  |  |
|  |  | 2.2.5 Si existen servicios, protocolos o «demonios» inseguros: 
•	 La justificación de negocio está documentada.
•	 Se documentan e implementan características de seguridad adicionales que reducen el riesgo de utilizar servicios, protocolos o «demonios» inseguros. |  |  |  |  |  |
|  |  | 2.2.6 Los parámetros de seguridad del sistema están configurados para impedir su uso indebido. |  |  |  |  |  |
|  |  | 2.2.7 Todo el acceso administrativo sin consola está cifrado utilizando criptografía robusta.
Notas de Aplicabilidad
Esto incluye el acceso administrativo a través de interfaces basadas en navegador e interfaces de programación de aplicaciones (API). |  |  |  |  |  |
|  | 2.3 Los entornos inalámbricos se configuran y administran de forma segura. | 2.3.1 Para entornos inalámbricos conectados al CDE o que transmiten datos de tarjetahabientes, todos los valores predeterminados de los proveedores inalámbricos se cambian en la instalación o se confirma que son seguros, incluidos, entre otros:
•	 Claves de cifrado inalámbricas predeterminadas.
•	 Contraseñas o puntos de acceso inalámbricos.
•	 Valores predeterminados de SNMP,
•	 Cualquier otro proveedor inalámbrico predeterminado relacionado con la seguridad.
Notas de Aplicabilidad
Esto incluye, pero no se limita a, las claves de encriptación inalámbrica predeterminadas, las contraseñas de los puntos de acceso inalámbricos, los valores predeterminados de SNMP y cualquier otro valor predeterminado del proveedor inalámbrico relacionado con la seguridad. |  |  |  |  |  |
|  |  | 2.3.2 Para los entornos inalámbricos conectados al CDE o que transmitan datos de tarjetahabientes, las claves cifradas inalámbricas se cambian como sigue: 
•	 Siempre que el personal con conocimiento de la clave deje la empresa o la función para la que era necesario el conocimiento.
•	 Siempre que se sospeche o se sepa que una clave está comprometida. |  |  |  |  |  |

---

## Hoja: 3

|  | Matriz RACI por requerimiento PCI DSS |  |  |  |  | Código:  | AN-XX |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | Version: | 1 |
|  |  |  |  |  |  |  |  |
| Requisito/Responsable | Requerimiento | Actividad | R | A | C | I | Entregable/Documento |
| Requisito 3: Proteger los Datos  de Tarjetahabientes Almacenados | 3.1 Se definen y comprenden los procesos y mecanismos para realizar las actividades del Requisito 3. | 3.1.1 Todas las políticas de seguridad y procedimientos operativos que se identifican en el Requisito 3 son: 
•	Documentados. 
•	Actualizados. 
•	En uso.
•	Conocidos por todas las partes involucradas. |  |  |  |  |  |
|  |  | 3.1.2 Los roles y responsabilidades para realizar las actividades del Requisito 3 están documentados, asignados y comprendidos.
Nuevo requisito - efectivo inmediatamente |  |  |  |  |  |
|  | 3.2 El almacenamiento de los datos de tarjetahabientes se mantiene al mínimo. | 3.2.1 El almacenamiento de datos de tarjetahabientes se mantiene al mínimo mediante la implementación de políticas y procedimientos de retención y eliminación de datos que incluyan al menos lo siguiente:
•	 Cubren todas las ubicaciones donde hay datos de tarjetahabientes.
•	 Cubren todo dato confidencial de autenticación (SAD) almacenado antes de completar la autorización. Este punto es la mejor práctica hasta su fecha de vigencia; consulte las Notas de Aplicabilidad que aparecen a continuación para obtener más detalles.
•	 Limitar la cantidad de datos almacenados y su tiempo de retención a lo requerido por los requisitos legales o reglamentarios y/o de negocios. 
•	 Requisitos de retención específicos para los datos de tarjetahabientes que definen la duración del período de retención e incluyen una justificación de negocio documentada. 
•	 Procesos para el borrado seguro o para hacer que los datos de tarjetahabiente sean irrecuperables cuando ya no se necesitan según la política de retención.
•	 Un proceso para verificar, al menos una vez cada tres meses, que los datos de tarjetahabientes que excedan el período de retención definido se han eliminado de forma segura o se han vuelto irrecuperables. 
Notas de Aplicabilidad
Cuando un TPSP almacena datos de tarjetahabientes (por ejemplo, en un entorno de nube), las entidades son responsables de trabajar con sus proveedores de servicios para comprender cómo el TPSP cumple con este requisito para la entidad. Las consideraciones incluyen garantizar que todas las instancias geográficas de un elemento de datos se eliminen de forma segura.
El punto anterior (para la cobertura de SAD almacenada antes de completar la autorización) es la mejor práctica hasta el 31 de marzo de 2025, después de lo cual se requerirá como parte del Requisito 3.2.1 y se debe considerar en su totalidad durante una evaluación de los PCI DSS. |  |  |  |  |  |
|  | 3.3 Los datos confidenciales de autenticación (SAD) no se almacenan después de la autorización. | 3.3.1 Los SAD no se retienen después de la autorización, incluso si están cifrados. Todos los datos confidenciales de autenticación recibidos se vuelven irrecuperables una vez finalizado el proceso de autorización
Notas de Aplicabilidad
Este requisito no se aplica a los emisores y empresas que apoyan los servicios de emisión (en los que los SAD son requeridos para una necesidad legítima de negocio de emisión) y tienen una justificación de negocio para almacenar los datos confidenciales de autenticación. 
Consulte el Requisito 3.3.3 para conocer los requisitos adicionales específicos para emisores. 
Los datos confidenciales de autenticación incluyen los datos citados en los Requisitos 3.3.1.1 hasta el 3.3.1.3. 
 |  |  |  |  |  |
|  |  | 3.3.1.1 El contenido completo de cualquier pista no se conserva una vez finalizado el proceso de autorización.
Notas de Aplicabilidad
En el curso normal de los negocios, es posible que sea necesario conservar los siguientes elementos de datos de la pista: 
•	 Nombre del tarjetahabiente.
•	 Número de cuenta principal (PAN).
•	 Fecha de expiración.
•	 Código de servicio.
Para minimizar el riesgo, almacene de forma segura sólo estos elementos de datos según sea necesario para la empresa. |  |  |  |  |  |
|  |  | 3.3.1.2 El código de verificación de la tarjeta no se conserva una vez finalizado el proceso de autorización.
Notas de Aplicabilidad
El código de verificación de la tarjeta es el número de tres o cuatro dígitos impreso en el anverso o el reverso de una tarjeta de pago y que se utiliza para verificar las transacciones no presenciales de la tarjeta. |  |  |  |  |  |
|  |  | 3.3.1.3 El número de identificación personal (PIN) y el bloque del PIN no se conservan al finalizar el proceso de autorización.
Notas de Aplicabilidad
Los bloques PIN se cifran durante el curso natural de los procesos de transacción, pero incluso si una entidad cifra el bloque de PIN nuevamente, todavía no se permite que se almacene después de la finalización del proceso de autorización. |  |  |  |  |  |
|  |  | 3.3.2 Los SAD que se almacenan electrónicamente antes de completar la autorización se cifran mediante criptografía robusta. 
Notas de Aplicabilidad
Las organizaciones que administran los programas de conformidad (por ejemplo, las marcas de pago y adquirentes) determinan si se permite el almacenamiento de los SAD antes de la autorización. Comuníquese con las organizaciones de interés para cualquier criterio adicional.
Este requisito aplica para todo almacenamiento de los SAD, incluso si no hay datos PAN en el entorno.
Consulte el Requisito 3.2.1 para conocer el requisito adicional que aplica si el SAD se almacena antes de completar la autorización.
Este requisito no aplica para los emisores y empresas que apoyan la emisión de servicios cuando existe una justificación comercial legítima de emisión para almacenar los SAD). 
Consulte el Requisito 3.3.3 para conocer los requisitos específicos para emisores. 
Este requisito no reemplaza la forma en que se deben administrar los bloques PIN ni significa que aquellos que hayan sido debidamente cifrados necesiten cifrarse nuevamente. 
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 3.3.3 Requisito adicional para emisores y empresas que apoyan servicios de emisión y que almacenan datos confidenciales de autenticación: Cualquier almacenamiento de datos confidenciales de autenticación está: 
•	 Limitado a lo que se necesita para una necesidad legítima de negocio de emisión y está asegurado.
•	 Cifrado utilizando criptografía robusta. 
Notas de Aplicabilidad
Este requisito se aplica solo para los emisores y empresas que apoyan la emisión de servicios y almacenan datos confidenciales de autenticación. 
Las entidades que emiten tarjetas de pago o que realizan o apoyan servicios de emisión a menudo crearán y controlarán datos confidenciales de autenticación como parte de la función de emisión. Está permitido a las empresas que realizan, facilitan o apoyan servicios de emisión, almacenar datos confidenciales de autenticación SÓLO SI se tiene una necesidad legítima de negocio de almacenar dichos datos. 
Los requisitos PCI DSS están destinados a todas las entidades que almacenan, procesan o transmiten datos de tarjetahabientes, incluidos los emisores. La única excepción para los emisores y procesadores de emisores es que los datos confidenciales de autenticación pueden retenerse si existe una razón legítima para hacerlo. Estos datos deben almacenarse de forma segura y de acuerdo con todas PCI DSS y los requisitos específicos de la marca de pago. 
(continúa en la página siguiente)
El punto anterior (para cifrar los SAD almacenados con criptografía robusta) es la mejor práctica hasta el 31 de marzo de 2025, después de lo cual se requerirá como parte del Requisito 3.3.3 y se debe considerar por completo durante una evaluación PCI DSS. |  |  |  |  |  |
|  | 3.4 El acceso a las pantallas de datos PAN completas y la capacidad de copiar los datos de tarjetahabientes está restringidos. | 3.4.1 Los datos PAN están enmascarados cuando se muestra (el BIN y los últimos cuatro dígitos constituyen el número máximo de dígitos que se muestran), de manera que sólo el personal con una necesidad legítima de negocios pueda ver más que el BIN y los últimos cuatro dígitos de los datos PAN.
Notas de Aplicabilidad
Este requisito no sustituye a otros más estrictos para la visualización de los datos de tarjetahabientes, por ejemplo, los requisitos legales o de las marcas de pago para los recibos de los puntos de venta (POS).
Este requisito se refiere a la protección de los datos PAN cuando se muestran en pantallas, recibos de papel, impresiones, etc., y no debe confundirse con el requisito 3.5.1 para la protección de los datos PAN cuando se almacenan, se procesan o se transmiten. 
 |  |  |  |  |  |
|  |  | 3.4.2 Cuando se utilicen tecnologías de acceso remoto 
los controles técnicos impiden la copia y/o la reubicación de los datos PAN para todo el personal, excepto para aquellos con autorización explícita y documentada y una necesidad legítima de negocio y definida.
Notas de Aplicabilidad
Almacenar o reubicar los datos PAN en discos duros locales, medios electrónicos extraíbles y otros dispositivos de almacenamiento hace que estos dispositivos estén dentro del alcance PCI DSS.
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  | 3.5 El número de cuenta principal (PAN) está protegido donde sea que se almacene. | 3.5.1 Los datos PAN se hace ilegible en cualquier lugar donde se almacene utilizando cualquiera de los siguientes enfoques: 
•	 Hashes unidireccionales basados en criptografía robusta del PAN completo. 
•	 Truncamiento (los hashes no pueden utilizarse para reemplazar el segmento truncado de la PAN).
•	 Índice de tokens.
•	 Criptografía robusta con procesos y procedimientos de gestión de claves asociados. 
•	 Si en un entorno hay versiones truncadas y con hash del mismo PAN, o diferentes formatos de truncamiento del mismo PAN, se establecen controles adicionales de manera que las diferentes versiones no puedan correlacionarse para reconstruir el PAN original.
Notas de Aplicabilidad
Constituye un esfuerzo relativamente trivial para individuos malintencionados el reconstruir los datos del PAN originales si tienen acceso tanto a la versión truncada como a la versión hash de un PAN.
Este requisito se aplica a los datos PAN guardados en almacenamiento primario (bases de datos o archivos planos como hojas de cálculo de archivos de texto), así como en almacenamiento no primario (copias de seguridad, registros de auditoría, registros de excepciones o de resolución de problemas), todos ellos deben estar protegidos. 
Este requisito no excluye el uso de archivos temporales que contengan datos PAN en texto no cifrado mientras se encriptan y desencriptan. |  |  |  |  |  |
|  |  | 3.5.1.1 Los hash utilizados para hacer ilegibles los datos PAN (según el primer punto del requisito 3.5.1) son hashes criptográficos con clave de todos los datos PAN, con procesos y procedimientos de gestión de claves asociados de acuerdo con los Requisitos 3.6 y 3.7.
Notas de Aplicabilidad
Este requisito se aplica a los datos PAN guardados en almacenamiento primario (bases de datos o archivos planos como hojas de cálculo de archivos de texto), así como en almacenamiento no primario (copias de seguridad, registros de auditoría, registros de excepciones o de resolución de problemas), todos ellos deben estar protegidos. 
Este requisito no excluye el uso de archivos temporales que contengan datos PAN en texto no cifrado mientras se encriptan y desencriptan. 
Este requisito se considera una práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 3.5.1.2 Si se utiliza un cifrado a nivel de disco o de partición (en lugar de un cifrado de base de datos a nivel de archivo, columna o campo) para hacer que los datos PAN sea ilegibles, sólo se implementará de la siguiente manera:
•	 En medios electrónicos extraíbles
O
•	 Si se utiliza para medios electrónicos no extraíbles, los datos PAN también se hacen ilegibles mediante otro mecanismo que cumpla con el Requisito 3.5.1. 
Nota: Las implementaciones de cifrado de discos o particiones también deben cumplir todos los demás requisitos de cifrado y gestión de claves PCI DSS. 
Notas de Aplicabilidad
Aunque el cifrado de disco puede seguir estando presente en estos tipos de dispositivos, este no puede ser el único mecanismo utilizado para proteger los datos PAN almacenadas en esos sistemas. Cualquier dato del PAN almacenado también debe volverse ilegible según el Requisito 3.5.1, por ejemplo, mediante el truncamiento o por un mecanismo de cifrado a nivel de datos. El cifrado de disco completo ayuda a proteger los datos en caso de pérdida física de un disco y, por lo tanto, su uso es apropiado sólo para dispositivos de almacenamiento de medios electrónicos extraíbles. 
Los medios que forman parte de la arquitectura de un centro de datos (por ejemplo, unidades intercambiables en caliente, copias de seguridad en cinta) se consideran medios electrónicos no extraíbles a los que se aplica el Requisito 3.5.1.
Las implementaciones de cifrado de discos o particiones también deben cumplir todos los demás requisitos de cifrado y gestión de claves PCI DSS. 
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 3.5.1.3 Si se utiliza el cifrado a nivel del disco o de partición (en lugar del cifrado de la base de datos a nivel de archivo, columna o campo) para hacer que los datos PAN sea ilegibles, sólo se implementará de la siguiente manera: 
•	El acceso lógico se gestiona por separado e independientemente de la autenticación del sistema operativo nativo y de los mecanismos de control de acceso. 
•	Las claves de descifrado no están asociadas a las cuentas de usuarios. 
•	Los factores de autenticación (contraseñas, frases de paso o claves criptográficas) que permiten el acceso a los datos no cifrados se almacenan de forma segura.
Notas de Aplicabilidad
Las implementaciones de cifrado de discos o particiones también deben cumplir todos los demás requisitos de cifrado y gestión de claves PCI DSS. |  |  |  |  |  |
|  | 3.6 Las claves criptográficas utilizadas para proteger los datos almacenados de tarjetahabientes están protegidos. | 3.6.1 Los procedimientos se definen e implementan para proteger las claves cifradas utilizadas para proteger los datos almacenados de tarjetahabientes contra la divulgación y el uso indebido que incluyen: 
•		 El acceso a las claves está restringido al menor número de custodios necesarios. 
•		 Las claves de cifrado de claves son al menos tan seguras como las claves de cifrado de datos que estas protegen. 
•		 Las claves de cifrado de claves se almacenan por separado de las claves de cifrado de datos. 
•		 Las claves se almacenan de forma segura en el menor número posible de formas y ubicaciones.
Notas de Aplicabilidad
Este requisito se aplica a las claves utilizadas para cifrar los datos almacenados de tarjetahabientes y a las claves de cifrado utilizadas para proteger las claves de cifrado de datos.
El requisito para proteger las claves utilizadas para proteger los datos almacenados de tarjetahabientes de la divulgación y el uso indebido se aplica tanto a las claves de cifrado de datos como a las claves de cifrado de claves. Debido a que una clave de cifrado de claves puede otorgar acceso a muchas claves de cifrado de datos, las claves de cifrado de claves requieren fuertes medidas de protección. |  |  |  |  |  |
|  |  | 3.6.1.1 Requisito adicional sólo para proveedores de servicios: Se mantiene una descripción documentada de la arquitectura criptográfica que incluye: 
•	 Detalles de todos los algoritmos, protocolos y claves utilizados para la protección de los datos de tarjetahabientes, incluyendo la fuerza de la clave y la fecha de caducidad.
•	 Evitar el uso de las mismas claves criptográficas en entornos de producción y de prueba. Este punto es la mejor práctica hasta su fecha de vigencia; consulte las Notas de Aplicabilidad que aparecen a continuación para obtener más detalles.
•	 Descripción del uso de claves para cada clave. 
•	 Inventario de los módulos de seguridad de hardware (HSM), sistemas de gestión de claves (KMS) y otros dispositivos criptográficos seguros (SCD) utilizados para la gestión de claves, incluido el tipo y la ubicación de los dispositivos, como se describe en el Requisito 12.3.3.
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad evaluada es un proveedor de servicios.
En las implementaciones de HSM en la nube, la responsabilidad de la arquitectura criptográfica de acuerdo con este Requisito será compartida entre el proveedor de la nube y el cliente de la nube.
El punto anterior (para que en la arquitectura criptográfica se impida el uso de las mismas claves criptográficas en producción y prueba) es una mejor práctica hasta el 31 de marzo de 2025, después de lo cual se requerirá como parte del Requisito 3.6.1.1 y deberá tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 3.6.1.2 Las claves secretas y privadas que se utilizan para cifrar/descifrar los datos de tarjetahabientes se almacenan en uno (o más) de los siguientes formularios en todo momento: 
•	 Cifrado con una clave de cifrado de clave, que sea al menos tan fuerte, como la clave de cifrado de datos y que se almacene por separado de la clave de cifrado de datos. 
•	 Dentro de un dispositivo criptográfico seguro (SCD), como un módulo de seguridad de hardware (HSM) o un dispositivo de punto de interacción aprobado por PTS. 
•	 Como mínimo dos componentes clave de longitud completa
o recursos compartidos de clave, de acuerdo con un método aceptado por la industria. 
Notas de Aplicabilidad
No es necesario que las claves públicas sean almacenadas en uno de estas formas.
Las claves criptográficas almacenadas como parte de un sistema de gestión de claves (KMS) que emplea SCD son aceptables. 
Una clave criptográfica que se divide en dos partes no cumple con este requisito. Las claves secretas o privadas almacenadas como componentes clave o recursos compartidos de claves deben generarse a través de uno de los siguientes métodos: 
•	Utilizando un generador de números aleatorios aprobado y dentro de un SCD, 
O
•	De acuerdo con el estándar ISO 19592 o su equivalente en la industria para la generación de claves secretas compartidas. |  |  |  |  |  |
|  |  | 3.6.1.3 El acceso a los componentes de claves criptográficas de texto no cifrado está restringido al menor número posible de custodios que sean necesarios. |  |  |  |  |  |
|  |  | 3.6.1.4 Las claves criptográficas se almacenan en el menor número posible de ubicaciones.  |  |  |  |  |  |
|  | 3.7 Cuando se usa criptografía para proteger datos almacenados de tarjetahabientes, se definen e implementan procesos y procedimientos de administración de claves que cubren todos los aspectos del ciclo de vida de las claves. | 3.7.1 Las políticas y procedimientos de administración de claves se implementan para incluir la generación de claves criptográficas fuertes utilizadas para proteger los datos almacenados de los tarjetahabientes. |  |  |  |  |  |
|  |  | 3.7.2 Las políticas y los procedimientos de administración de claves son implementados para incluir la distribución segura de las claves criptográficas utilizadas para proteger los datos almacenados de tarjetahabientes. |  |  |  |  |  |
|  |  | 3.7.3 Se implementan políticas y procedimientos de gestión de claves para incluir el almacenamiento seguro de las claves criptográficas utilizadas para proteger los datos de tarjetahabientes almacenado. |  |  |  |  |  |
|  |  | 3.7.4 Se implementan políticas y procedimientos de gestión de claves para los cambios de claves criptográficas de para aquellas claves que han llegado al final de su criptoperíodo, según lo definido por el proveedor de la aplicación asociada o el propietario de la clave, y basado en las mejores prácticas y directrices de la industria, incluyendo lo siguiente:
•	 Un criptoperíodo definido para cada tipo de clave en uso.
•	 Un proceso para el cambio de claves al final del criptoperíodo definido. |  |  |  |  |  |
|  |  | 3.7.5 Los procedimientos de políticas de gestión de claves se implementan para incluir el retiro, sustitución o destrucción de las claves utilizadas para proteger los datos almacenados de tarjetahabientes, según se considere necesario cuando: 
• 	La clave haya llegado al final de su criptoperíodo definido.
• 		La integridad de la clave se haya debilitado, incluso cuando el personal con conocimiento de un componente de la clave en texto no cifrado abandone la empresa, o la función por la que conocía la clave.
• 		Cuando se sospecha o se sabe que las claves están comprometidas. 
Las claves retiradas o reemplazadas no se utilizan para operaciones de cifrado.
Notas de Aplicabilidad
Si es necesario conservar las claves criptográficas retiradas o reemplazas, dichas claves deben archivarse de forma segura (por ejemplo, utilizando una clave de cifrado).  |  |  |  |  |  |
|  |  | 3.7.6 Cuando el personal realiza operaciones manuales de gestión de claves criptográficas en texto no cifrado, se implementan políticas y procedimientos de gestión de claves que incluyen la gestión de estas operaciones utilizando conocimiento dividido y control dual. 
Notas de Aplicabilidad
Este control es aplicable para operaciones manuales de administración de claves o donde la administración de claves no está controlada por el producto de cifrado. 
Una clave criptográfica que simplemente se divide en dos partes no cumple con este requisito. Las claves secretas o privadas almacenadas como componentes clave o recursos compartidos de claves deben generarse a través de uno de los siguientes métodos: 
• 	Utilizando un generador de números aleatorios aprobado y dentro de un dispositivo criptográfico seguro (SCD), como un módulo de seguridad de hardware (HSM) o un dispositivo de punto de interacción aprobado por PTS, 
O
• 	De acuerdo con el estándar ISO 19592 o su equivalente en la industria para la generación de claves secretas compartidas. |  |  |  |  |  |
|  |  | 3.7.7 Se implementan políticas y procedimientos de administración de claves para incluir la prevención de la sustitución no autorizada de claves criptográficas. |  |  |  |  |  |
|  |  | 3.7.8 Las políticas y los procedimientos de administración de claves se implementan para incluir que los custodios de claves criptográficas reconozcan formalmente (por escrito o electrónicamente) que comprenden y aceptan sus responsabilidades como custodios de claves. |  |  |  |  |  |
|  |  | 3.7.9 Requisito adicional sólo para proveedores de servicios: Cuando un proveedor de servicios comparte claves criptográficas con sus clientes para la transmisión o el almacenamiento de datos del tarjetahabiente, se documenta y distribuye a los clientes de los proveedores de servicios orientación sobre la transmisión, el almacenamiento y la actualización segura de dichas claves.
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad que se evalúa es un proveedor de servicios. |  |  |  |  |  |

---

## Hoja: 4

|  | Matriz RACI por requerimiento PCI DSS |  |  |  |  | Código:  | AN-XX |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | Version: | 1 |
|  |  |  |  |  |  |  |  |
| Requisito/Responsable | Requerimiento | Actividad | R | A | C | I | Entregable/Documento |
| Requisito 4: Proteja los Datos de Tarjetahabientes con una Criptografía Robusta Durante la Transmisión | 4.1 Se definen y documentan los procesos y mecanismos para realizar las actividades del Requisito 4. | 4.1.1 Todas las políticas de seguridad y procedimientos operativos que se identifican en el Requisito 4 son:
•	 Documentados
•	 Actualizados
•	 En uso
•	 Conocidos por todas las partes involucradas
 |  |  |  |  |  |
|  |  | 4.1.2 Los roles y responsabilidades para realizar las actividades del Requisito 4 están documentados, asignados y comprendidos. 
 |  |  |  |  |  |
|  | 4.2 Los datos PAN está protegidos con criptografía robusta durante la transmisión. | 4.2.1 Se implementan fuertes protocolos de seguridad y criptografía robusta de la siguiente manera para proteger los datos PAN durante la transmisión a través de redes públicas abiertas:
•	 Sólo se aceptan claves y certificados confiables.
•	 Los certificados utilizados para proteger los datos PAN durante la transmisión a través de redes públicas abiertas se confirman como válidos y no están vencidos ni revocados. Este punto es la mejor práctica hasta su fecha de vigencia; consulte las Notas de Aplicabilidad a continuación para obtener más detalles.
•	 El protocolo en uso sólo apoya versiones o configuraciones seguras y no apoya el uso de versiones, algoritmos, tamaños de clave o implementaciones inseguras.
•	 La fuerza del cifrado es apropiada para la metodología de cifrado en uso. 
Notas de Aplicabilidad
Puede haber casos en los que una entidad reciba datos de tarjetahabientes no solicitados a través de un canal de comunicación inseguro que no fue diseñado con el propósito de recibir datos confidenciales. Ante esta situación, la entidad puede optar por incluir el canal en su CDE y asegurarlo de acuerdo con PCI DSS o implementar medidas para impedir que el canal se utilice para datos de tarjetahabientes.
Un certificado auto-firmado también puede ser aceptable si el certificado es emitido por una CA interna dentro de la organización, si el autor del certificado está confirmado y si el certificado está verificado (por ejemplo, mediante hash o firma) y no está caducado. Hay que tomar en cuenta que los certificados auto-firmados en los que en el campo de Denominación Distinguida (DN) bajo "emitido por" y "emitido para" aparece la misma información, no son aceptables.
El punto anterior (para confirmar que los certificados utilizados para proteger los datos PAN durante la transmisión a través de redes públicas abiertas son válidos y no están vencidos ni revocados) es una mejor práctica hasta el 31 de marzo de 2025, después de lo cual se requerirá como parte del Requisito 4.2.1 y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 4.2.1.1 Se mantiene un inventario de las claves y certificados confiables de la entidad utilizados para proteger los datos PAN durante la transmisión.
Notas de Aplicabilidad
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación de PCI DSS.
 |  |  |  |  |  |
|  |  | 4.2.1.2 Las redes inalámbricas que transmiten datos PAN o están conectadas al CDE utilizan las mejores prácticas de la industria para implementar criptografía robusta para autenticación y transmisión.  |  |  |  |  |  |
|  |  | 4.2.2  Los datos PAN están protegidos con criptografía robusta siempre que se envíen a través de tecnologías de mensajería del usuario final.
Notas de Aplicabilidad
Este requisito también se aplica si un cliente u otro tercero solicitan que se le envíen datos PAN a través de tecnologías de mensajería para el usuario final.
Puede haber casos en los que una entidad reciba datos no solicitados de tarjetahabientes a través de un canal de comunicación inseguro que no está destinado a la transmisión de datos confidenciales. Ante esta situación, la entidad puede optar por incluir el canal en su CDE y asegurarlo de acuerdo con PCI DSS o borrar los datos del tarjetahabiente e implementar medidas para impedir que el canal se utilice para datos de tarjetahabientes.
 |  |  |  |  |  |

---

## Hoja: 5

|  | Matriz RACI por requerimiento PCI DSS |  |  |  |  | Código:  | AN-XX |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | Version: | 1 |
|  |  |  |  |  |  |  |  |
| Requisito/Responsable | Requerimiento | Actividad | R | A | C | I | Entregable/Documento |
| Requisito 5: Proteger Todos los Sistemas y Redes de Software Malicioso | 5.1 Se definen y comprenden los procesos y mecanismos para proteger todos los sistema y redes del software malintencionado. | 5.1.1 Todas las políticas de seguridad y procedimientos operativos que se identifican en el Requisito 5 son:
•	 Documentados
•	 Actualizados
•	 En uso
•	 Conocidos por todas las partes involucradas |  |  |  |  |  |
|  |  | 5.1.2 Los roles y responsabilidades para realizar las actividades del Requisito 5 están documentados, asignados y comprendidos. 
 |  |  |  |  |  |
|  | 5.2 El software malintencionado (malware) es evadido, o se detecta y se soluciona. | 5.2.1 Una solución antimalware se aplicará a todos los componentes del sistema, excepto a aquellos componentes del sistema identificados en evaluaciones periódicas según el Requisito 5.2.3 que concluye que los componentes del sistema no están en riesgo de malware. |  |  |  |  |  |
|  |  | 5.2.2 Las soluciones antimalware implementadas:
•	 Detectan todos los tipos conocidos de malware.
•	 Eliminan, bloquean o contienen todos los tipos conocidos de malware.  |  |  |  |  |  |
|  |  | 5.2.3 Todos los componentes del sistema que no se encuentren en riesgo de malware se evalúan periódicamente para incluir lo siguiente: 
•	 Una lista documentada de todos los componentes del sistema que no están en riesgo de malware.
•	 Identificación y evaluación de amenazas de malware en evolución para los componentes del sistema.
•	 Confirmación de si dichos componentes del sistema continúan sin requerir protección antimalware.
 |  |  |  |  |  |
|  |  | 5.2.3.1 La frecuencia de las evaluaciones periódicas de los componentes del sistema identificados como no en riesgo de malware se define en el análisis de riesgo específico de la entidad, el cual se realiza de acuerdo con todos los elementos especificados en el Requisito 12.3.1. 
 |  |  |  |  |  |
|  | 5.3 Los mecanismos y procesos antimalware están activos, mantenidos y monitoreados. | 5.3.1 Las soluciones antimalware se mantienen actualizadas a través de procesos de actualización automáticos. |  |  |  |  |  |
|  |  | 5.3.2  Soluciones antimalware:
•	 Realizan escaneos periódicos y escaneos activos o en tiempo real
O 
•	 Realizan un análisis continuo del comportamiento de los sistemas o procesos. |  |  |  |  |  |
|  |  | 5.3.2.1 Si se realizan escaneos periódicos de malware para cumplir con el requisito 5.3.2, la frecuencia de los escaneos se define en el análisis de riesgos específico de la entidad, que se realiza de acuerdo con todos los elementos especificados en el Requisito 12.3.1. 
Notas de Aplicabilidad
Este requisito aplica para las entidades que realizan escaneos periódicos de malware para cumplir con el Requisito 5.3.2.
 |  |  |  |  |  |
|  |  | 5.3.3 Para los medios electrónicos extraíbles, la solución antimalware: 
• Realiza escaneos automáticos cuando el medio es insertado, conectado o montado lógicamente,
O
• Realiza un análisis continuo del comportamiento de los sistemas o procesos cuando el medio está insertado, conectado o montado lógicamente.
 |  |  |  |  |  |
|  |  | 5.3.4 Los registros de auditoría de la solución antimalware están habilitados y se conservan de acuerdo con el requisito 10.5.1. |  |  |  |  |  |
|  |  | 5.3.5 Los mecanismos antimalware no pueden ser desactivados o alterados por los usuarios, a menos que esté específicamente documentado y autorizado por la administración en cada caso, por un período de tiempo limitado. 
Notas de Aplicabilidad
Las soluciones antimalware sólo pueden desactivarse temporalmente si existe una necesidad técnica legítima, autorizada por la dirección en cada caso. Si es necesario desactivar la protección antimalware para un fin específico, esto debe ser formalmente autorizado. También puede ser necesario implementar medidas de seguridad adicionales para el período durante el cual la protección antimalware no está activa. |  |  |  |  |  |
|  | 5.4 Los mecanismos contra antiphishing protegen a los usuarios contra los ataques de phishing. |  5.4.1 Existen procesos y mecanismos automatizados para detectar y proteger al personal contra ataques de phishing. 
Notas de Aplicabilidad
Este requisito se aplica al mecanismo automatizado. No se pretende que los sistemas y servicios que proporcionan tales mecanismos automatizados (como servidores de correo electrónico) entren en el ámbito PCI DSS.
El enfoque de este requisito es proteger al personal con acceso a los componentes del sistema en el ámbito PCI DSS.
Cumplir con este requisito de controles técnicos y automatizados para detectar y proteger al personal contra el phishing no es igual a lo que establece el Requisito 12.6.3.1 en cuanto al entrenamiento de concienciación sobre seguridad. Cumplir con este requisito tampoco implica que se está cumpliendo con el requisito de proporcionar al personal capacitación en cuanto a concienciación de seguridad, y viceversa.
 |  |  |  |  |  |

---

## Hoja: 6

|  | Matriz RACI por requerimiento PCI DSS |  |  |  |  | Código:  | AN-XX |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | Version: | 1 |
|  |  |  |  |  |  |  |  |
| Requisito/Responsable | Requerimiento | Actividad | R | A | C | I | Entregable/Documento |
| Requisito 6: Desarrollar y Mantener Sistemas y Software Seguros | 6.1 Se definen y comprenden los procesos y mecanismos para desarrollar y mantener sistemas y software seguros. | 6.1.1 Todas las políticas de seguridad y procedimientos operativos que se identifican en el Requisito 6 son:
•	 Documentados.
•	 Actualizados.
•	 En uso.
•	 Conocidos por todas las partes involucradas.  |  |  |  |  |  |
|  |  | 6.1.2 Los roles y responsabilidades para realizar las actividades del Requisito 6 están documentados, asignados y comprendidos. 
 |  |  |  |  |  |
|  | 6.2 El software a medida y personalizado se desarrolla de forma segura. | 6.2.1 El software a medida y personalizado se desarrolla de forma segura, de la siguiente manera:
•	 Basándose en estándares de la industria y/o mejores prácticas para un desarrollo seguro. 
•	 De acuerdo con PCI DSS (por ejemplo, autenticación segura y registro). 
•	 Considerando la incorporación de la información de problemas de seguridad durante cada etapa del ciclo de vida del desarrollo de software. 
Notas de Aplicabilidad
Esto se aplica a todo el software desarrollado por o para la entidad para su propio uso. Esto incluye software tanto a la medida como personalizado. Esto no aplica para el software de terceros. |  |  |  |  |  |
|  |  | 6.2.2 El personal de desarrollo de software que trabaja en software a medida y personalizado recibe capacitación al menos una vez cada 12 meses de la siguiente manera: 
•	 Sobre la seguridad del software relevante para su función laboral y lenguajes de desarrollo.
•	 Incluyendo diseño de software seguro y técnicas de codificación segura.
•	 Incluyendo, si se utilizan herramientas de prueba de seguridad, cómo utilizar las herramientas para detectar vulnerabilidades en el software.
Notas de Aplicabilidad:
Este requisito de revisión del código se aplica a todo el software a medida y personalizado (tanto interno como de cara al público), como parte del ciclo de vida de desarrollo del sistema.
Las aplicaciones web públicas también están sujetas a controles adicionales para abordar las amenazas y vulnerabilidades continuas después de la implementación, como se define en el Requisito 6.4 de los PCI DSS.
Las revisiones de código se pueden realizar mediante procesos manuales o automatizados, o una combinación de ambos. |  |  |  |  |  |
|  |  | 6.2.3 El software a medida y personalizado es revisado antes de ser lanzado a producción o para los clientes, a fin de identificar y corregir posibles vulnerabilidades de codificación, de la siguiente manera:
•	 Las revisiones de código garantizan que el código se desarrolle de acuerdo con las pautas de codificación segura.
•	 Las revisiones de código buscan vulnerabilidades de software tanto existente como emergente.
•	 Las correcciones apropiadas se implementan antes de la publicación. |  |  |  |  |  |
|  |  | 6.2.3.1 Si las revisiones manuales de código son realizadas para software hecho a medida y personalizado antes de ser liberado a producción, los cambios de código son:
•	 Revisados por personas que no sean el autor del código original, y que conozcan las técnicas de revisión de código y las prácticas de codificación segura.
•	 Revisados y aprobados por la dirección antes de su publicación.
Notas de Aplicabilidad
Las revisiones manuales de código pueden ser llevadas a cabo por personal interno con conocimientos o por personal de terceros con conocimientos.
Una persona a la que se le ha concedido formalmente la responsabilidad del control de la publicación y que no es ni el autor original del código ni el revisor del mismo cumple con los criterios de ser administrador. |  |  |  |  |  |
|  |  | 6.2.4 Las técnicas de ingeniería de software u otros métodos están definidos y en uso para el software a medida y personalizado por el personal de desarrollo de software a fin de impedir o mitigar los ataques de software comunes y las vulnerabilidades relacionadas, incluyendo, pero no limitado a lo siguiente:
•	 Ataques de inyección, incluyendo SQL, LDAP, XPath u otros fallos de flujo de tipo comando, parámetro, objeto, defecto o de inyección.
•	 Ataques a datos y estructuras de datos, incluyendo intentos de manipulación de buffers, punteros, datos de entrada o datos compartidos.
•	 Ataques al uso de criptografía, incluyendo intentos de explotar implementaciones criptográficas débiles, inseguras o inapropiadas, algoritmos, suites de cifrado o modos de operación.
•	 Ataques a la lógica del negocio, incluyendo los intentos de abusar o eludir las características y funcionalidades de la aplicación a través de la manipulación de las APIs, los protocolos y canales de comunicación, la funcionalidad del lado del cliente, u otras funciones y recursos del sistema/aplicación. Esto incluye los scripts entre sitios (XSS) y la falsificación de petición entre sitios (CSRF).
• 	 Ataques a los mecanismos de control de acceso, incluidos los intentos de eludir o abusar de los mecanismos de identificación, autenticación o autorización, o los intentos de aprovechar las debilidades en la implementación de dichos mecanismos.
•	 Ataques a través de cualquier vulnerabilidad de "alto riesgo" identificada en el proceso de identificación de vulnerabilidades, tal como se define en el Requisito 6.3.1. 
Notas de Aplicabilidad
Esto se aplica a todo el software desarrollado por o para la entidad para su propio uso. Esto incluye software tanto a la medida como personalizado. Esto no aplica para el software de terceros. |  |  |  |  |  |
|  | 6.3 Las vulnerabilidades de seguridad se identifican y son abordadas. | 6.3.1 Las vulnerabilidades de seguridad se identifican y gestionan de la siguiente manera: 
•	 Las nuevas vulnerabilidades de seguridad se identifican utilizando fuentes reconocidas por la industria de información de vulnerabilidades de seguridad, incluyendo alertas de equipos internacionales y nacionales de respuesta a emergencias informáticas (CERTs).
•	 A las vulnerabilidades se les asigna una clasificación de riesgo basada en las mejores prácticas de la industria y considerando su impacto potencial. 
•	 Las clasificaciones de riesgo identifican, como mínimo, todas las vulnerabilidades consideradas de alto riesgo o críticas para el entorno. 
•	 Se cubren las vulnerabilidades de los programas informáticos a medida y de terceros (por ejemplo, sistemas operativos y bases de datos). 
Notas de Aplicabilidad
Este requisito no se consigue con los escaneos de vulnerabilidades realizados para los requisitos 11.3.1 y 11.3.2, ni es lo mismo. Este requisito se refiere a un proceso para monitorizar activamente las fuentes de la industria en materia de información de vulnerabilidades y para que la entidad determine la clasificación de riesgo que se asociará con cada vulnerabilidad. |  |  |  |  |  |
|  |  | 6.3.2 A fin de facilitar la gestión de vulnerabilidades y parches se mantiene un inventario del software a medida y personalizado y de los componentes del software de terceros incorporados en el software a medida y personalizado.  |  |  |  |  |  |
|  |  | 6.3.3 Todos los componentes del sistema están protegidos contra vulnerabilidades conocidas mediante la instalación de parches/actualizaciones de seguridad aplicables de la siguiente manera: 
• 	 Los parches/actualizaciones críticas o de alta seguridad (identificados de acuerdo con el proceso de clasificación de riesgos del Requisito 6.3.1) se instalan dentro del período de un mes de su emisión. 
• 	 Todos los demás parches/actualizaciones de seguridad aplicables se instalan dentro de un período de tiempo apropiado según lo determine la entidad (por ejemplo, dentro de los tres meses posteriores al lanzamiento).  |  |  |  |  |  |
|  | 6.4 Las aplicaciones web públicas están protegidas contra ataques. | 6.4.1 Para las aplicaciones web de cara al público, las nuevas amenazas y vulnerabilidades se abordan de forma continua y están protegidas contra los ataques conocidos de la siguiente manera:
•	 Revisión de las aplicaciones web de cara al público mediante herramientas o métodos de evaluación de la seguridad de las vulnerabilidades de las aplicaciones, sean manuales o automatizadas, como sigue:
•	 Al menos una vez cada 12 meses y después de cambios significativos.
•	 Por una entidad especializada en seguridad de aplicaciones.
•	 Incluyendo, como mínimo, todos los ataques de software comunes descritos en el Requisito 6.2.4.
•	 Todas las vulnerabilidades se clasifican de acuerdo con el Requisito 6.3.1.
•	 Se corrigen todas las vulnerabilidades.
•	 La aplicación se vuelve a evaluar después de las correcciones
O
•	 Instalación de soluciones técnicas automatizadas que detecten e impidan continuamente los ataques basados en la web de la siguiente manera:
•	 Instaladas frente a las aplicaciones web de cara al público para detectar e impedir los ataques basados en la web.
•	 Funcionando activamente y actualizándose según corresponda.
•	 Generando registros de auditoría. 
•	 Configurados ya sea para bloquear los ataques basados en la web o para generar una alerta que se investigue inmediatamente.
Notas de Aplicabilidad
Esta evaluación no es la misma que los escaneos de vulnerabilidad realizados para los Requisitos 11.3.1 y 11.3.2.
Este requisito será sustituido por el requisito 6.4.2 después del 31 de marzo de 2025, cuando entre en vigor el requisito 6.4.2. |  |  |  |  |  |
|  |  | 6.4.2 Para aplicaciones web de cara al público se implementa una solución técnica automatizada que detecta e impide continuamente ataques basados en la web, con al menos lo siguiente:
•	 Se instala frente a aplicaciones web de cara al público y está configurado para detectar e impedir ataques basados en la web.
•	 Funcionando activamente y actualizándose según corresponda. 
•	 Generando registros de auditoría.
•	 Configurados ya sea para bloquear los ataques basados en la web o para generar una alerta que se investigue inmediatamente. 
Notas de Aplicabilidad
Este nuevo requisito reemplazará al Requisito 6.4.1 una vez que termine su fecha de vigencia. |  |  |  |  |  |
|  |  | 6.4.3 Todos los scripts de las páginas de pago que se cargan y ejecutan en el navegador del consumidor se gestionan de la siguiente manera:
•	 Se implementa un método para confirmar que cada script está autorizado.
•	 Se implementa un método para asegurar la integridad de cada script. 
•	 Se mantiene un inventario de todos los scripts con una justificación por escrito que explique su necesidad. 
Notas de Aplicabilidad
Este requisito se aplica a todos los scripts cargados desde el entorno de la entidad y a los scripts cargados desde terceras y cuartas partes. |  |  |  |  |  |
|  | 6.5 Los cambios en todos los componentes del sistema se gestionan de forma segura. | 6.5.1 Los cambios en todos los componentes del sistema en el entorno de producción se realizan de acuerdo con los procedimientos establecidos que incluyen: 
•	Motivo y descripción del cambio. 
•	Documentación del impacto a la seguridad. 
•	Aprobación documentada del cambio por las partes autorizadas.
•	Pruebas para verificar que el cambio no afecta negativamente la seguridad del sistema.
•	En el caso de los cambios de software a la medida y personalizados, todas las actualizaciones se comprueban para determinar la conformidad con el Requisito 6.2.4 antes de ser instalados para producción. 
•	Procedimientos para hacer frente a los fallos y volver a un estado seguro.  |  |  |  |  |  |
|  |  | 6.5.2 Al completar un cambio significativo, se confirma que todos los requisitos PCI DSS están vigentes en todos los sistemas y redes nuevas o modificadas, y la documentación se actualiza según corresponda.
Notas de Aplicabilidad
Estos cambios significativos también deben capturarse y reflejarse en la actividad de confirmación del alcance PCI DSS anual de la entidad, según el Requisito 12.5.2. |  |  |  |  |  |
|  |  | 6.5.3 Los entornos de preproducción se separan de los entornos de producción y la separación se aplica con controles de acceso. |  |  |  |  |  |
|  |  | 6.5.4 Los roles y las funciones se separan entre los entornos de producción y pre-producción para asignar responsabilidades de manera tal que sólo se desplieguen los cambios revisados y aprobados.
Notas de Aplicabilidad
En entornos con personal limitado donde los individuos desempeñan múltiples roles o funciones, este mismo objetivo puede lograrse con controles de procedimiento adicionales que asignen responsabilidades. Por ejemplo, un desarrollador puede ser también un administrador que utiliza una cuenta de nivel administrador con privilegios especiales en el entorno de desarrollo y, para su función de desarrollador, utiliza una cuenta separada con acceso de nivel de usuario al entorno de producción. |  |  |  |  |  |
|  |  | 6.5.5 Los datos PAN activos no se utilizan en entornos de pre-producción, excepto cuando esos entornos están incluidos en el CDE y protegidos de acuerdo con todos los requisitos PCI DSS aplicables. |  |  |  |  |  |
|  |  | 6.5.6 Los datos de prueba y las cuentas de pruebas se eliminan de los componentes del sistema antes de que el sistema entre en producción. |  |  |  |  |  |

---

## Hoja: 7

|  | Matriz RACI por requerimiento PCI DSS |  |  |  |  | Código:  | AN-XX |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | Version: | 1 |
|  |  |  |  |  |  |  |  |
| Requisito/Responsable | Requerimiento | Actividad | R | A | C | I | Entregable/Documento |
| Requisito 7: Restringir el Acceso a los Componentes del Sistema y a los Datos de Tarjetahabientes Según la Necesidad de Conocimiento de la Empresa | 7.1 Se definen y comprenden los procesos y mecanismos para restringir el acceso a los componentes del sistema ya los datos de tarjetahabientes según la necesidad de negocio. | 7.1.1 Todas las políticas de seguridad y procedimientos operativos que se identifican en el Requisito 7 son:
•	Documentados, 
•	Actualizados
•	 En uso 
•	Conocidos por todas las partes involucradas.  |  |  |  |  |  |
|  |  | 7.1.2 Los roles y responsabilidades para realizar las actividades del Requisito 7 están documentados, asignados y son comprendidos.  |  |  |  |  |  |
|  | 7. 2 El acceso a los componentes y datos del sistema se define y asigna adecuadamente. | 7.2.1 Se define un modelo de control de acceso que incluye la autorización de acceso como sigue:
•	 Acceso apropiado según el tipo de negocios de la entidad y las necesidades de acceso. 
•	 Acceso a los componentes del sistema y a los recursos de datos basados en la clasificación y las funciones del trabajo de los usuarios. 
•	 Los privilegios mínimos requeridos (por ejemplo, usuario, administrador) para realizar una función laboral. |  |  |  |  |  |
|  |  | 7.2.2 El acceso se asigna a los usuarios, incluidos los privilegiados, en función de: 
•	 La clasificación y función del trabajo.
•	 Los privilegios mínimos necesarios para realizar las responsabilidades del trabajo. |  |  |  |  |  |
|  |  | 7.2.3 Los privilegios requeridos son aprobados por el personal autorizado. |  |  |  |  |  |
|  |  | 7.2.4 Todas las cuentas de usuario y los privilegios de acceso relacionados, incluyendo las cuentas de terceros/proveedores, se revisan de la siguiente manera:
•	 Al menos una vez cada seis meses
•	 Para asegurarse de que las cuentas de usuario y el acceso sigan siendo apropiados según la función del trabajo. 
•	 Se aborda cualquier acceso inadecuado.
•	 La gerencia reconoce que el acceso sigue siendo apropiado. 
Notas de Aplicabilidad
Este requisito se aplica a todas las cuentas de usuario y privilegios de acceso relacionados, incluyendo las que utiliza el personal y terceros/proveedores, y las cuentas utilizadas para acceder a servicios de terceros en la nube. 
Consulte los Requisitos 7.2.5 y 7.2.5.1 y 8.6.1 a 8.6.3 para conocer los controles de aplicaciones y cuentas del sistema. |  |  |  |  |  |
|  |  | 7.2.5 Todas las aplicaciones y cuentas del sistema y los privilegios de acceso relacionados se asignan y administran de la siguiente manera:
•	 Basado en los privilegios mínimos necesarios para la operatividad del sistema o aplicación.
•	 El acceso está limitado a los sistemas, aplicaciones o procesos que específicamente requieren su uso.   |  |  |  |  |  |
|  |  | 7.2.5.1 Todo el acceso de aplicaciones y cuentas del sistema y los privilegios de acceso relacionados se revisan de la siguiente manera:
•	 Periódicamente, (a una frecuencia definida en el análisis de riesgos específico de la entidad, el cual se desarrolla de acuerdo a todos los elementos especificados en el Requisito 12.3.1).
•	 El acceso a la aplicación/sistema sigue siendo apropiado para la función que se está realizando. 
•	 Se aborda cualquier acceso inadecuado.
•	 La gerencia reconoce que el acceso sigue siendo apropiado. |  |  |  |  |  |
|  |  | 7.2.6 Todo acceso por parte de los usuarios a las bases de datos de tarjetahabientes está restringido de la siguiente manera:
•	 A través de aplicaciones u otros métodos programáticos, con acceso y acciones permitidas basadas en las funciones y privilegios mínimos del usuario.
•	 Solo los administradores autorizados pueden acceder directamente o consultar las bases de datos de CHD almacenados.
Notas de Aplicabilidad
Este requisito se aplica a los controles para el acceso de los usuarios a las bases de datos almacenados de tarjetahabientes. 
Consulte los Requisitos 7.2.5 y 7.2.5.1 y 8.6.1 a 8.6.3 para conocer los controles de aplicaciones y cuentas del sistema. |  |  |  |  |  |
|  | 7.3 El acceso a los componentes y datos del sistema se gestiona a través de un sistema de control de acceso. | 7.3.1 Existen sistemas de control de acceso que restringen el acceso según la necesidad del usuario y cubre todos los componentes del sistema. |  |  |  |  |  |
|  |  | 7.3.2 Los sistemas de control de acceso están configurados para aplicar los permisos asignados a individuos, aplicaciones, y sistemas basados en la clasificación y función del trabajo. |  |  |  |  |  |
|  |  | 7.3.3 El sistema de control de acceso está configurado para "denegar todo" predeterminadamente. |  |  |  |  |  |

---

## Hoja: 8

|  | Matriz RACI por requerimiento PCI DSS |  |  |  |  | Código:  | AN-XX |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | Version: | 1 |
|  |  |  |  |  |  |  |  |
| Requisito/
Responsable | Requerimiento | Actividad | R | A | C | I | Entregable/Documento |
| Requisito 8: Identificar a los Usuarios y Autenticar el Acceso a los Componentes del Sistema | 8.1 Se definen y comprenden los procesos y mecanismos para realizar las actividades del Requisito 8. | 8.1.1 Todas las políticas de seguridad y procedimientos operativos que se identifican en el Requisito 8 están:
•	 Documentados.
•	 Actualizados.
•	 En uso.
•	 Conocidos por todas las partes involucradas. |  |  |  |  |  |
|  |  | 8.1.2 Los roles y responsabilidades para realizar las actividades del Requisito 8 están documentados, asignados y son comprendidos. |  |  |  |  |  |
|  | 8.2 La identificación de usuarios y las cuentas relacionadas para usuarios y administradores se gestionan estrictamente durante el ciclo de vida de una cuenta. | 8.2.1 A todos los usuarios se les asigna un ID único antes de permitirles el acceso a los componentes del sistema o a los datos de tarjetahabientes.
Notas de Aplicabilidad
Este requisito no está destinado a aplicarse a las cuentas de usuario de los terminales de punto de venta que sólo tienen acceso a un número de tarjeta simultáneamente para procesar una única transacción (como los IDs utilizados por los cajeros en los terminales de punto de venta). |  |  |  |  |  |
|  |  | 8.2.2 Las cuentas grupales, compartidas o genéricas, u otras credenciales de autenticación compartidas sólo se usan cuando es necesario, de manera excepcional, y se administran de la siguiente manera:
•	 Se impide el uso de la cuenta a menos que se requiera por una circunstancia excepcional.
•	 Su uso está limitado al tiempo necesario para la circunstancia excepcional.
•	 La justificación de negocio para su uso está documentada.
•	 El uso está explícitamente aprobado por la dirección. 
•	 La identidad del usuario individual se confirma antes de que se conceda el acceso a una cuenta.
•	 Cada acción realizada es atribuible a un usuario individual. 
Notas de Aplicabilidad
Este requisito no está destinado a aplicarse a las cuentas de usuario de los terminales de punto de venta que sólo tienen acceso a un número de tarjeta simultáneamente para procesar una única transacción (como los IDs utilizados por los cajeros en los terminales de punto de venta). |  |  |  |  |  |
|  |  | 8.2.3 Requisito adicional sólo para proveedores de servicios: Los proveedores de servicios con acceso remoto a las instalaciones del cliente deben utilizar factores de autenticación únicos para las instalaciones de cada cliente.
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad que se evalúa es un proveedor de servicios.
Este requisito no se aplica a los proveedores de servicios que acceden a sus propios entornos de servicios compartidos, donde se alojan múltiples entornos de clientes.
Si los empleados del proveedor de servicios utilizan factores de autenticación compartidos para acceder de forma remota a las instalaciones del cliente, estos factores deben ser únicos para cada cliente y deben administrarse de acuerdo con el Requisito 8.2.2. |  |  |  |  |  |
|  |  | 8.2.4 La creación, eliminación y modificación de IDs de usuario, factores de autenticación y otros objetos de identificación se gestiona de la siguiente manera:
•	 Autorizado con la aprobación correspondiente.
•	 Implementado solo con los privilegios especificados en la aprobación documentada.
Notas de Aplicabilidad
Este requisito se aplica a todas las cuentas de usuario, incluyendo los empleados, contratistas, consultores, trabajadores temporales y proveedores externos. |  |  |  |  |  |
|  |  | 8.2.5 El acceso para los usuarios que cesan se revoca inmediatamente |  |  |  |  |  |
|  |  | 8.2.6 Las cuentas de usuario inactivas se eliminan o inhabilitan dentro de los 90 días de inactividad.  |  |  |  |  |  |
|  |  | 8.2.7 Las cuentas utilizadas por terceros para acceder, apoyar o mantener componentes del sistema a través de acceso remoto se administran de la siguiente manera:
•	 Son habilitadas solamente durante el período de tiempo necesario y son deshabilitadas cuando no están en uso.
•	 El uso es monitoreado para detectar actividad inesperada. |  |  |  |  |  |
|  |  | 8.2.8 Si una sesión de usuario ha estado inactiva durante más de 15 minutos, se requiere que el usuario vuelva a autenticarse para reactivar el terminal o la sesión.
Notas de Aplicabilidad
Este requisito no está destinado a aplicarse a las cuentas de usuario de los terminales de punto de venta que sólo tienen acceso a un número de tarjeta simultáneamente para procesar una única transacción (como los IDs utilizados por los cajeros en los terminales de punto de venta).
Este requisito no pretende impedir que se realicen actividades legítimas mientras la consola/PC está desatendida.  |  |  |  |  |  |
|  | 8.3 Se establece y gestiona una autenticación robusta para usuarios y administradores. | 8.3.1 Todo acceso por parte de los usuarios y administradores a componentes del sistema se autentifica utilizando al menos uno de los siguientes factores de autenticación:
•	Algo que uno sabe, como una contraseña o frase de paso.
•	Algo que uno tiene, como un dispositivo token o una tarjeta inteligente.
•	Algo que uno es, como un elemento biométrico.
Notas de Aplicabilidad
Este requisito no está destinado a aplicarse a las cuentas de usuario de los terminales de punto de venta que sólo tienen acceso a un número de tarjeta simultáneamente para procesar una única transacción (como los IDs utilizados por los cajeros en los terminales de punto de venta).
Este requisito no sustituye a los requisitos de autenticación de múltiples factores (MFA), sino que se aplica a los sistemas incluidos en el ámbito de aplicación que no están sujetos a los requisitos de los MFA.
El certificado digital es una opción válida para "algo que se tiene" si es único para un usuario concreto. |  |  |  |  |  |
|  |  | 8.3.2 Se utiliza criptografía robusta para que todos los factores de autenticación sean ilegibles durante la transmisión y el almacenamiento en todos los componentes del sistema.  |  |  |  |  |  |
|  |  | 8.3.3 La identidad del usuario se verifica antes de modificar cualquier factor de autenticación. |  |  |  |  |  |
|  |  | 8.3.4 Los intentos de autenticación inválidos se limitan mediante: 
•	 El bloqueo del ID de usuario después de no más de 10 intentos.
•	 El establecimiento de la duración del bloqueo a un mínimo de 30 minutos o hasta que se confirme la identidad del usuario. 
Notas de Aplicabilidad
Este requisito no está destinado a aplicarse a las cuentas de usuario de los terminales de punto de venta que sólo tienen acceso a un número de tarjeta simultáneamente para procesar una única transacción (como los IDs utilizados por los cajeros en los terminales de punto de venta). |  |  |  |  |  |
|  |  | 8.3.5 Si las contraseñas/frases de paso se utilizan como factores de autenticación para cumplir con el requisito 8.3.1, estas se establecen y restablecen para cada usuario tal y como sigue: 
•	 Se establece un valor único para la primera vez que se utilizan y al restablecerse.
•	 Existe la obligatoriedad de cambiarlos inmediatamente después del primer uso. |  |  |  |  |  |
|  |  | 8.3.6 Si las contraseñas/frases de paso se utilizan como factores de autenticación para cumplir el requisito 8.3.1, estas deberán cumplir el siguiente nivel mínimo de complejidad: 
•	 Una longitud mínima de 12 caracteres (o SI el sistema no admite 12 caracteres, una longitud mínima de ocho caracteres).
•	 Contener tanto caracteres numéricos como alfabéticos.
Notas de Aplicabilidad
Este requisito no se aplica a: 
•	 Cuentas de usuario de los terminales de punto de venta que sólo tienen acceso a un número de tarjeta simultáneamente para procesar una única transacción (como los IDs utilizados por los cajeros en los terminales de punto de venta).
•	 Cuentas de aplicaciones o sistemas, que se rigen por los requisitos de la sección 8.6. |  |  |  |  |  |
|  |  | 8.3.7 Las personas no pueden enviar una nueva contraseña / frase de paso que sea igual a cualquiera de las últimas cuatro contraseñas / frases de paso utilizadas.
Notas de Aplicabilidad
Este requisito no está destinado a aplicarse a las cuentas de usuario de los terminales de punto de venta que sólo tienen acceso a un número de tarjeta simultáneamente para procesar una única transacción (como los IDs utilizados por los cajeros en los terminales de punto de venta). |  |  |  |  |  |
|  |  | 8.3.8 Las políticas y los procedimientos de autenticación están documentados y son comunicados a todos los usuarios, incluyendo: 
•	 Orientación sobre la selección de factores de autenticación robustos.
•	Orientación sobre cómo los usuarios deben proteger sus factores de autenticación.
•	Instrucciones para no reutilizar contraseñas/frases de paso utilizadas anteriormente.
•	Instrucciones para cambiar contraseñas/frases de paso si existe alguna sospecha o conocimiento de que la contraseña/frase de paso se ha visto comprometida y cómo reportar el incidente. |  |  |  |  |  |
|  |  | 8.3.9 Si las contraseñas/frases de paso se utilizan como el único factor de autenticación para el acceso del usuario (es decir, en cualquier implementación de autenticación de factor único), entonces:
•	 Las contraseñas/frases de paso se cambian al menos una vez cada 90 días, 
O
•	 La postura de seguridad de las cuentas se analiza dinámicamente y el acceso a los recursos en tiempo real se determina automáticamente de acuerdo a dicha postura de seguridad. 
Notas de Aplicabilidad
Este requisito se aplica a los componentes del sistema dentro del alcance que no están en el CDE ya que esos componentes no están sujetos a los requisitos de los MFA.
Este requisito no está destinado a aplicarse a las cuentas de usuario de los terminales de punto de venta que sólo tienen acceso a un número de tarjeta simultáneamente para procesar una única transacción (como los IDs utilizados por los cajeros en los terminales de punto de venta).
Este requisito no se aplica a las cuentas de clientes de proveedores de servicios, pero se aplica a las cuentas del personal del proveedor de servicios. |  |  |  |  |  |
|  |  | 8.3.10 Requisito adicional sólo para proveedores de servicios: Si las contraseñas / frases de paso contraseña se utilizan como el único factor de autenticación para el acceso del usuario del cliente a los datos de tarjetahabiente (es decir, en cualquier implementación de autenticación de factor único), entonces se brinda orientación a los usuarios del cliente, que incluye:
•	Orientación para que los clientes cambien sus contraseñas/frases de paso periódicamente.
•	Orientación sobre cuándo y bajo qué circunstancias se cambian lascontraseñas/frases de paso.
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad que se evalúa es un proveedor de servicios.
Este requisito no se aplica a las cuentas de usuarios consumidores que acceden a la información de su propia tarjeta de pago.
Este requisito para los proveedores de servicios será reemplazado por el Requisito 8.3.10.1 una vez que el 8.3.10.1 entre en vigor. |  |  |  |  |  |
|  |  | 8.3.10.1 Requisito adicional sólo para proveedores de servicios: Si las contraseñas/frases de paso se utilizan como el único factor de autenticación para el acceso del usuario del cliente (es decir, en cualquier implementación de autenticación de factor único), entonces:
•	 Las contraseñas/frases de paso se cambian al menos una vez cada 90 días, 
O
•	 La postura de seguridad de las cuentas se analiza dinámicamente y el acceso a los recursos en tiempo real se determina automáticamente de acuerdo a dicha postura de seguridad.
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad que se evalúa es un proveedor de servicios.
Este requisito no se aplica a las cuentas de usuarios consumidores que acceden a la información de su propia tarjeta de pago. |  |  |  |  |  |
|  |  | 8.3.11 Cuando se utilizan factores de autenticación como tokens de seguridad físicos o lógicos, tarjetas inteligentes o certificados: 
•	 Los factores se asignan a un usuario individual y no se comparten entre varios usuarios. 
•	 Los controles físicos y/o lógicos garantizan que sólo el usuario previsto pueda utilizar ese factor para acceder. |  |  |  |  |  |
|  | 8.4 Se implementa la autenticación múltiples factores (MFA) para proteger el ingreso al CDE. | 8.4.1 Los MFA se implementan para todos los accesos al CDE sin consola, para el personal con acceso administrativo. 
Notas de Aplicabilidad
El requisito de MFA para el acceso administrativo sin consola se aplica a todo el personal con privilegios elevados o aumentados que accede al CDE a través de una conexión sin consola, es decir, a través de un acceso lógico que se produce a través de una interfaz de red en lugar de una conexión directa y física. 
Los MFA se consideran una práctica recomendada para el acceso administrativo sin consola, a los componentes del sistema en cuestión que no forman parte del CDE. |  |  |  |  |  |
|  |  | 8.4.2  Los MFA se implementan para todos los accesos al CDE.
Notas de Aplicabilidad
Este requisito no se aplica a: 
•	 Aplicación o cuentas del sistema que desempeñan funciones automatizadas.
•	 Cuentas de usuario de los terminales de punto de venta que sólo tienen acceso a un número de tarjeta simultáneamente para procesar una única transacción (como los IDs utilizados por los cajeros en los terminales de punto de venta).
Se requieren los MFA para ambos tipos de ingresos especificados en los Requisitos 8.4.2 y 8.4.3. Por lo tanto, la aplicación de los MFA a un tipo de acceso no reemplaza la necesidad de aplicar otra instancia de MFA al otro tipo de acceso. Si una persona se conecta primero a la red de la entidad a través de un acceso remoto, y luego inicia una conexión al CDE desde dentro de la red; según este requisito, la persona se autenticaría usando los MFA dos veces, una cuando se conecta a través de acceso remoto a la red de la entidad, y luego cuando se conecta a través de un acceso administrativo sin consola desde la red de la entidad al CDE.
(continúa en la página siguiente)
Los requisitos de los MFA se aplican a todos los tipos de componentes del sistema, incluyendo la nube, los sistemas alojados y las aplicaciones locales, los dispositivos de seguridad de red, las estaciones de trabajo, los servidores y los puntos finales, e incluye el acceso directo a las redes o sistemas de una entidad, así como el acceso basado en web a una aplicación o función. 
Los MFA para acceso remoto al CDE se pueden implementar a nivel de red o sistema/aplicación; no es necesario que se apliquen en ambos niveles. Por ejemplo, si se usan MFA cuando un usuario se conecta a la red del CDE, no es necesario que se usen cuando el usuario inicia sesión en cada sistema o aplicación dentro del CDE. |  |  |  |  |  |
|  |  | 8.4.3  Los MFA se implementan para todos los accesos a redes remotas que se originan fuera de la red de la entidad y que podrían ingresar o impactar el CDE de la siguiente manera:
•	 Todo acceso remoto por parte de todo el personal, tanto usuarios como administradores, originados fuera de la red de la entidad.
•	 Todo acceso remoto por terceros y proveedores.
Notas de Aplicabilidad
El requisito de los MFA para el acceso remoto que se origina desde fuera de la red de la entidad se aplica a todas las cuentas de usuario que pueden ingresar a la red de forma remota, donde ese acceso remoto conduce o podría conducir a un acceso al CDE.
Si el acceso remoto se realiza a una parte de la red de la entidad que está correctamente segmentada del CDE, de manera que los usuarios remotos no puedan ingresar al CDE o afectarlo, no se requiere MFA para el acceso remoto a esa parte de la red. Sin embargo, se requieren los MFA para cualquier acceso remoto a redes con acceso al CDE y se recomienda para todos los accesos remotos a las redes de la entidad.
Los requisitos de los MFA se aplican a todos los tipos de componentes del sistema, incluyendo la nube, los sistemas alojados y las aplicaciones locales, los dispositivos de seguridad de red, las estaciones de trabajo, los servidores y los puntos finales, e incluye el acceso directo a las redes o sistemas de una entidad, así como el acceso basado en web a una aplicación o función. |  |  |  |  |  |
|  | 8.5 Los sistemas de autenticación de múltiples factores (MFA) están configurados para evitar su uso indebido. | 8.5.1 Los sistemas MFA se implementan de la siguiente manera:
•	El sistema MFA no es susceptible a ataques de repetición.
•	Los sistemas MFA no pueden ser omitidos por ningún usuario, incluyendo los usuarios administrativos, a menos que esté específicamente documentado y autorizado por la administración de manera excepcional durante un período de tiempo limitado. 
•	Se utilizan al menos dos tipos diferentes de factores de autenticación.
•	Se requiere el éxito de todos los factores de autenticación antes de que se otorgue el acceso. |  |  |  |  |  |
|  | 8.6 El uso de cuentas de aplicaciones y sistemas y factores de autenticación asociados se gestiona estrictamente. | 8.6.1 Si las cuentas utilizadas por los sistemas o aplicaciones pueden ser utilizadas para el inicio de sesión interactivo, se gestionan de la siguiente manera: 
•	 Se impide el uso interactivo a menos que se requiera por una circunstancia excepcional.
•	 El uso está limitado al tiempo necesario para la circunstancia excepcional.
•	 La justificación de negocio para su uso interactivo está documentada.
•	 El uso interactivo está explícitamente aprobado por la dirección. 
•	 La identidad del usuario individual se confirma antes de que se conceda el acceso a una cuenta.
•	 Cada acción realizada es atribuible a un usuario individual.  |  |  |  |  |  |
|  |  | 8.6.2 Las contraseñas/frases de paso para cualquier aplicación y cuentas de sistema que puedan ser utilizadas para el inicio de sesión interactivo no están codificadas en scripts, archivos de configuración/propiedades, o código fuente a la medida y personalizado. Las contraseñas/frases de acceso almacenadas deben estar cifradas de acuerdo con el Requisito 8.3.2 PCI DSS.
Notas de Aplicabilidad
Las contraseñas/frases de ingreso almacenadas deben estar cifradas de acuerdo con el Requisito 8.3.2 de PCI DSS. |  |  |  |  |  |
|  |  | 8.6.3 Las contraseñas/frases de paso para cualquier cuenta de aplicación y de sistema están protegidas contra el uso indebido de la siguiente manera: 
•	 Las cuentas de sistema y de aplicación se cambian periódicamente, (a una frecuencia definida en el análisis de riesgos específico de la entidad, el cual se desarrolla de acuerdo con todos los elementos especificados en el Requisito 12.3.1) y ante la sospecha o la confirmación de que estén comprometidas.
•	 Las contraseñas/frases de acceso se construyen con la complejidad necesaria y apropiada para la frecuencia con la que la entidad cambia las contraseñas/frases de acceso. |  |  |  |  |  |

---

## Hoja: 9

|  | Matriz RACI por requerimiento PCI DSS |  |  |  |  | Código:  | AN-XX |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | Version: | 1 |
|  |  |  |  |  |  |  |  |
| Requisito/Responsable | Requerimiento | Actividad | R | A | C | I | Entregable/Documento |
| Requisito 9: Restringir el Acceso Físico a los Datos de Tarjetahabientes | 9.1 Se definen y comprenden los procesos y mecanismos para realizar las actividades del Requisito 9. | 9.1.1 Todas las políticas de seguridad y procedimientos operativos que se identifican en el Requisito 9 están:
•	 Documentados. 
•	 Actualizados. 
•	 En uso.
•	 Conocidos por todas las partes involucradas. |  |  |  |  |  |
|  |  | 9.1.2 Los roles y responsabilidades para realizar las actividades del Requisito 9 están documentados, asignados y comprendidos.
Nuevo requisito - efectivo inmediatamente |  |  |  |  |  |
|  | 9.2 Los controles de acceso físico gestionan la entrada en el entorno de datos de tarjetahabientes. | 9.2.1 Existen controles de entrada a las instalaciones apropiados para restringir el acceso físico a los sistemas en el CDE. |  |  |  |  |  |
|  |  | 9.2.1.1 El ingreso físico individual a las áreas sensibles dentro del CDE se monitoriza con cámaras de video vigilancia o mecanismos de control de acceso físico (o ambos) como sigue:
•	 Los puntos de entrada y salida hacia/desde las áreas sensibles dentro del CDE son monitorizados. 
•	 Los dispositivos o mecanismos de monitorización están protegidos contra la manipulación o la desactivación.
•	 Los datos recogidos se revisan y se correlacionan con otras entradas.
•	 Los datos recogidos se almacenan durante al menos tres meses, a menos que la ley lo restrinja. |  |  |  |  |  |
|  |  | 9.2.2 Se implementan controles físicos y/o lógicos para restringir el uso de tomas (o puertos) de red de acceso público dentro de la instalación. |  |  |  |  |  |
|  |  | 9.2.3 El ingreso físico a los puntos de acceso inalámbricos, puertas de enlace (gateways), hardware de redes y de comunicaciones y líneas de telecomunicaciones dentro de la instalación está restringido. |  |  |  |  |  |
|  |  | 9.2.4 El acceso a las consolas en áreas sensibles está restringido mediante bloqueo cuando no están en uso. |  |  |  |  |  |
|  | 9.3 El acceso físico al entorno de datos de tarjetahabientes para el personal y los visitantes está autorizado y gestionado. | 9.3.1 Se implementan procedimientos para autorizar y administrar el acceso físico del personal al CDE, que incluyen:
•	  Identificación de personal.
•	 Gestionar cambios en los requisitos de ingreso físico de una persona.
•	  Revocación o rescisión de la identificación del personal.
•	  Limitar el acceso al proceso o sistema de identificación al personal autorizado. |  |  |  |  |  |
|  |  | 9.3.1.1 El acceso físico a áreas sensitivas dentro del CDE para el personal se controla de la siguiente manera:
•	 El acceso está autorizado y se basa en la función del trabajo individual.
•	 El acceso se revoca inmediatamente después de la terminación.
•	 Todos los mecanismos de acceso físico, como llaves, tarjetas de acceso, etc., se devuelven o desactivan al finalizar. |  |  |  |  |  |
|  |  | 9.3.2 Se implementan procedimientos para autorizar y administrar el acceso de visitantes al CDE, que incluyen:
•	 Los visitantes son autorizados antes de ingresar.
•	 Los visitantes están acompañados en todo momento.
•	 Los visitantes están claramente identificados y reciben un gafete u otra identificación con fecha de caducidad.
•	 Los gafetes de visitante u otra identificación distinguen visiblemente a los visitantes del personal. |  |  |  |  |  |
|  |  | 9.3.3 Los gafetes de visitante o la identificación se devuelven o desactivan antes de que los visitantes abandonen las instalaciones, o en su fecha de caducidad. |  |  |  |  |  |
|  |  | 9.3.4 Se utiliza un registro de visitantes para mantener un registro físico de las actividades de los visitantes dentro de la instalación y dentro de las áreas sensibles, que incluye: 
•	 El nombre del visitante y la organización representada.
•	 La fecha y hora de la visita.
•	 El nombre del personal que autoriza el acceso físico. 
•	 Conservar el registro al menos durante al menos tres meses, a menos que la ley lo restrinja. |  |  |  |  |  |
|  | 9.4 Los medios con datos de tarjetahabientes se almacenan, acceden, distribuyen y destruyen de forma segura. | 9.4.1 Todos los medios que contienen datos de tarjetahabientes están protegidos físicamente.  |  |  |  |  |  |
|  |  | 9.4.1.1 Las copias de seguridad sin conexión con los datos de tarjetahabientes se almacenan en una ubicación segura.  |  |  |  |  |  |
|  |  | 9.4.1.2 La protección de las ubicaciones de las copias de seguridad fuera de línea que contienen los datos de tarjetahabientes, se revisa al menos una vez cada 12 meses. |  |  |  |  |  |
|  |  | 9.4.2 Todos los datos de tarjetahabientes se clasifican de acuerdo con la confidencialidad de esos datos. |  |  |  |  |  |
|  |  | 9.4.3 Los apoyos con datos de tarjetahabientes enviados fuera de las instalaciones se protegen de la siguiente manera:
• Los datos enviados fuera de las instalaciones se registran.
• Los datos se envían por mensajería segura u otro método de entrega que pueda ser rastreado con precisión.
• Los registros de seguimiento fuera de las instalaciones incluyen detalles sobre la ubicación de los datos. |  |  |  |  |  |
|  |  | 9.4.4 La gerencia aprueba todos los movimientos de apoyos con datos de tarjetahabientes que se trasladan fuera de las instalaciones (incluso cuando son distribuidos a particulares).
Notas de Aplicabilidad
Las personas que aprueban los movimientos de los apoyos deben tener el nivel adecuado de autoridad de gestión para conceder esta aprobación. Sin embargo, no se requiere específicamente que dichas personas tengan el título de "gerente". |  |  |  |  |  |
|  |  | 9.4.5 Se mantienen registros de inventario de todos los apoyos electrónicos con datos de tarjetahabientes.  |  |  |  |  |  |
|  |  | 9.4.5.1 Los inventarios de apoyos electrónicos con datos de tarjetahabientes se realizan al menos una vez cada 12 meses.  |  |  |  |  |  |
|  |  | 9.4.6 Los materiales impresos con datos de tarjetahabientes se destruyen cuando ya no se necesitan por razones de negocios o legales, de la siguiente manera:
•	 Los materiales se trituran transversalmente, se incineran o se pulverizan de forma que los datos de tarjetahabientes no puedan reconstruirse. 
•	 Los materiales se guardan en contenedores de almacenamiento seguro antes de su destrucción. 
Notas de Aplicabilidad
Estos requisitos relativos a la destrucción de medios de almacenamiento cuando éstos ya no son necesarios por motivos de negocio o legales son independientes y distintos del Requisito 3.2.1 PCI DSS, que se refiere a la eliminación segura de los datos de los tarjetahabientes cuando ya no son necesarios de acuerdo con las políticas de retención de datos de tarjetahabientes de la entidad. |  |  |  |  |  |
|  |  | 9.4.7 Los medios de almacenamiento electrónicos con datos de tarjetahabientes se destruyen cuando ya no se necesitan por razones de negocio o legales mediante una de las siguientes opciones: 
•	 El medio de almacenamiento electrónico se destruye.
•	 Los datos de tarjetahabientes se vuelven irrecuperables, de modo que no pueden reconstruirse. 
Notas de Aplicabilidad
Estos requisitos relativos a la destrucción de medios de almacenamiento cuando éstos ya no son necesarios por motivos de negocio o legales son independientes y distintos del Requisito 3.2.1 PCI DSS, que se refiere a la eliminación segura de los datos de los tarjetahabientes cuando ya no son necesarios de acuerdo con las políticas de retención de datos de tarjetahabientes de la entidad. |  |  |  |  |  |
|  | 9.5 Los dispositivos de Punto de Interacción (POI) están protegidos contra manipulaciones y sustituciones no autorizadas. | 9.5.1 Los dispositivos POI que capturan los datos de las tarjetas de pago a través de la interacción física directa con el factor de forma de la tarjeta de pago están protegidos contra la manipulación y la sustitución no autorizada, incluyendo lo siguiente:
•	 Mantener una lista de dispositivos de POI. 
•	 Inspeccionar periódicamente los dispositivos POI en busca de manipulaciones o sustituciones no autorizadas. 
•	 Formar al personal para que esté atento a los comportamientos sospechosos y denuncie las manipulaciones o sustituciones no autorizadas de los dispositivos.
Notas de Aplicabilidad
Estos requisitos se aplican a los dispositivos de POI desplegados que se utilizan en transacciones con tarjeta física (es decir, un factor de forma de tarjeta de pago como una tarjeta que se pasa, se toca o se introduce). Este requisito no está destinado a aplicarse a los componentes manuales de introducción de claves PAN, como los teclados de ordenador.
Este requisito es recomendado, pero no exigible, para los componentes manuales de introducción de claves PAN, como los teclados de ordenador. 
Este requisito no se aplica a los dispositivos comerciales listos para usar (COTS) (por ejemplo, teléfonos inteligentes o tabletas), que son dispositivos móviles propiedad de comerciantes, diseñados para su distribución en el mercado masivo. |  |  |  |  |  |
|  |  | 9.5.1.1 Se mantiene una lista actualizada de los dispositivos POI, que incluye:
•	 Marca y modelo del dispositivo. 
•	 Ubicación del dispositivo. 
•	 Número de serie del dispositivo u otros métodos de identificación única. |  |  |  |  |  |
|  |  | 9.5.1.2 Las superficies de los dispositivos POI se inspeccionan periódicamente para detectar manipulaciones y sustituciones no autorizadas.  |  |  |  |  |  |
|  |  | 9.5.1.2.1 La frecuencia de las inspecciones a los dispositivos POI y el tipo de inspección que se realice se define en el análisis de riesgos específico de la entidad, que se realiza de acuerdo con todos los elementos especificados en el Requisito 12.3.1.
Notas de Aplicabilidad
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 9.5.1.3 Se proporciona capacitación para que el personal en entornos POI esté al tanto de los intentos de manipulación o reemplazo de dispositivos POI, lo que incluye: manipulación o reemplazo de dispositivos POI, lo que incluye:
•	 Verificar la identidad de cualquier tercero que afirme ser personal de reparación o mantenimiento, antes de otorgarles acceso para modificar o solucionar problemas en los dispositivos.
•	 Procedimientos para garantizar que los dispositivos no se instalen, reemplacen o devuelvan sin verificación. 
•	 Ser consciente de comportamientos sospechosos alrededor de los dispositivos.
•	 Informar sobre comportamientos sospechosos e indicaciones de manipulación o sustitución de dispositivos al personal apropiado. |  |  |  |  |  |

---

## Hoja: 10

|  | Matriz RACI por requerimiento PCI DSS |  |  |  |  | Código:  | AN-XX |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | Version: | 1 |
|  |  |  |  |  |  |  |  |
| Requisito/Responsable | Requerimiento | Actividad | R | A | C | I | Entregable/Documento |
| Requisito 10: Registre y Controle Todo el Acceso a los Componentes del Sistema y a los Datos de Tarjetahabientes | 10.1 Se definen y comprenden los procesos y mecanismos para realizar las actividades del Requisito 10. | 10.1.1 Todas las políticas de seguridad y procedimientos operativos que se identifican en el Requisito 10 está: 
•	 Documentados.
•	 Actualizados.
•	 En uso.
•	 Conocidos por todas las partes involucradas.
 |  |  |  |  |  |
|  |  | 10.1.2 Los roles y responsabilidades para realizar las actividades del Requisito 10 están documentados, asignados y comprendidos.
Nuevo requisito - efectivo inmediatamente
 |  |  |  |  |  |
|  | 10.2 Los registros de auditoría se implementan para apoyar la detección de anomalías y actividades sospechosas, y el análisis forense de eventos. | 10.2.1 Los registros de auditoría están habilitados y activos para todos los componentes del sistema y los datos de tarjetahabientes. |  |  |  |  |  |
|  |  | 10.2.1.1 Los registros de auditoría capturan todo el acceso de los usuarios individuales a los datos de tarjetahabientes. |  |  |  |  |  |
|  |  | 10.2.1.2 Los registros de auditoría almacenan todas las acciones realizadas por cualquier individuo con acceso administrativo, incluyendo cualquier uso interactivo de la aplicación o cuentas del sistema. |  |  |  |  |  |
|  |  | 10.2.1.3 Los registros de auditoría capturan todo el acceso a los mismos. |  |  |  |  |  |
|  |  | 10.2.1.4 Los registros de auditoría capturan todos los intentos de acceso lógico inválidos. |  |  |  |  |  |
|  |  | 10.2.1.5 Los registros de auditoría capturan todos los cambios en la identificación y credenciales de autenticación, lo que incluye, entre otros:
•	 Creación de nuevas cuentas.
•	 Elevación de privilegios.
•	 Todos los cambios, adiciones o eliminaciones de cuentas con acceso administrativo. |  |  |  |  |  |
|  |  | 10.2.1.6 Los registros de auditoría capturan lo siguiente: 
•	 Toda inicialización de nuevos registros de auditoría y 
•	 Todo inicio, la detención o la pausa de los registros de auditoría existentes. |  |  |  |  |  |
|  |  | 10.2.1.7 Los registros de auditoría capturan toda la creación y eliminación de objetos a nivel del sistema. |  |  |  |  |  |
|  |  | 10.2.2 Los registros de auditoría guardan los siguientes detalles para cada evento auditable:
•	 Identificación del usuario.
•	 Tipo de evento.
•	 Fecha y hora.
•	 Indicación de Exitoso o Fallido.
•	 Origen del evento.
•	 Identidad o nombre de los datos, componentes del sistema, recursos o servicios afectados (por ejemplo, nombre y protocolo). |  |  |  |  |  |
|  | 10.3 Los registros de auditoría están protegidos contra la destrucción y las modificaciones no autorizadas. | 10.3.1 El acceso de lectura a los archivos de registros de auditoría está limitado a aquellos con una necesidad relacionada con sus funciones. |  |  |  |  |  |
|  |  | 10.3.2 Los archivos de registros de auditoría están protegidos para evitar modificaciones por parte de terceros. |  |  |  |  |  |
|  |  | 10.3.3 Los archivos de registros de auditoría, incluidos los de tecnologías externas, se respaldan de inmediato en un servidor de registro interno seguro, central o sobre otro medio que sea difícil de modificar. |  |  |  |  |  |
|  |  | 10.3.4 Los mecanismos de detección de cambios o supervisión de la integridad de los archivos se utilizan en registros de auditoría para garantizar que los datos de registros existentes no se puedan modificar sin generar alertas. |  |  |  |  |  |
|  | 10.4 Los registros de auditoría se revisan para identificar anomalías o actividades sospechosas. | 10.4.1 Los siguientes registros de auditoría se revisan al menos una vez al día:
•	 Todos los eventos de seguridad. 
•	 Registros de todos los componentes del sistema que almacenan, procesan o transmiten CHD y/o SAD.
•	 Registros de todos los componentes críticos del sistema.
•	 Registros de todos los servidores y componentes del sistema que realizan funciones de seguridad (por ejemplo, controles de seguridad de red, sistemas de detección de intrusiones/sistemas de prevención de intrusiones (IDS / IPS), servidores de autenticación). |  |  |  |  |  |
|  |  | 10.4.1.1 Se utilizan mecanismos automatizados para realizar revisiones de los registros de auditoría.
Notas de Aplicabilidad
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 10.4.2 Los registros de todos los demás componentes del sistema (aquellos no especificados en el Requisito 10.4.1) se revisan periódicamente.
Notas de Aplicabilidad
Este requisito es aplicable a todos los demás componentes del sistema dentro del alcance no incluidos en el Requisito 10.4.1. |  |  |  |  |  |
|  |  | 10.4.2.1 La frecuencia de las evaluaciones periódicas de los componentes del sistema identificados (No definidos en el Requisito 10.4.1) se define en el análisis de riesgo específico de la entidad, el cual se realiza de acuerdo con todos los elementos especificados en el Requisito 12.3.1.
Notas de Aplicabilidad
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 10.4.3 Se abordan las excepciones y anomalías identificadas durante el proceso de revisión. |  |  |  |  |  |
|  | 10.5 Se conserva el historial del registro de auditoría y está disponible para su análisis. | 10.5.1 Conserve el historial de los registros de auditoría durante 12 meses como mínimo, teniendo al menos los tres últimos meses inmediatamente disponibles para su análisis. |  |  |  |  |  |
|  | 10.6 Los mecanismos de sincronización de la hora apoyan una configuración de hora coherente en todos los sistemas. | 10.6.1 Los relojes del sistema y la hora están sincronizados usando tecnología de sincronización de tiempo. 
Notas de Aplicabilidad
Mantener actualizada la tecnología de sincronización horaria incluye la gestión de las vulnerabilidades y la aplicación de parches como lo establecen los Requisitos 6.3.1 y 6.3.3 PCI DSS. |  |  |  |  |  |
|  |  | 10.6.2 Los sistemas están configurados con la hora correcta y consistente como sigue:
•	 Uno o más servidores de tiempo designados están en uso.
•	 Solo los servidores de hora central designados reciben la hora de fuentes externas.
•	 La hora recibida de fuentes externas se basa en la Hora Atómica Internacional u Hora Universal Coordinada (UTC).
•	 Los servidores de tiempo designados aceptan actualizaciones de tiempo solo de fuentes externas específicas aceptadas por la industria.
•	 Cuando hay más de un servidor de tiempo designado, los servidores de tiempo se emparejan entre sí para mantener la hora exacta.
•	 Los sistemas internos reciben información de la hora solo de los servidores de hora central designados. |  |  |  |  |  |
|  |  | 10.6.3 La configuración de sincronización de la hora y los datos están protegidos de la siguiente manera: 
•	 El acceso a los datos de tiempo está restringido solo al personal con una necesidad de negocio.
•	 Cualquier cambio en la configuración de tiempo en sistemas críticos se registra, monitorea y verifica. |  |  |  |  |  |
|  | 10.7 Las fallas de los sistemas de control de seguridad críticos se detectan, informan y atienden con prontitud. | 10.7.1 Requisito adicional sólo para proveedores de servicios: Las fallas de los sistemas de control de seguridad críticos se detectan, alertan y abordan de inmediato, incluyendo entre otras, las fallas de los siguientes sistemas de control de seguridad críticos:
•	 Controles de seguridad de la red 
•	 IDS/IPS 
•	 FIM 
•	 Soluciones antimalware 
•	 Controles de acceso físico 
•	 Controles de Ingreso lógico 
•	 Mecanismos de registro de auditoría 
•	 Controles de segmentación (si se utilizan) 
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad que se evalúa es un proveedor de servicios.
Este requisito será sustituido por el requisito 10.7.2 a partir del 31 de marzo de 2025. |  |  |  |  |  |
|  |  | 10.7.2 Las fallas de los sistemas de control de seguridad críticos se detectan, alertan y abordan de inmediato, incluidas, entre otras, las fallas de los siguientes sistemas de control de seguridad críticos:
•	 Controles de seguridad de la red.
•	 IDS/IPS.
•	 Cambiar los mecanismos de detección.
•	 Soluciones antimalware.
•	 Controles de acceso físico.
•	 Controles de Ingreso lógico.
•	 Mecanismos de registro de auditoría.
•	 Controles de segmentación (si se utilizan).
•	 Mecanismos de revisión del registro de auditoría.
•	 Herramientas de prueba de seguridad automatizadas (si se utilizan).
Notas de Aplicabilidad
Este requisito se aplica a todas las entidades, incluidos los proveedores de servicios, y sustituirá al requisito 10.7.1 a partir del 31 de marzo de 2025. Incluye dos sistemas de control de seguridad críticos adicionales que no aparecen en el Requisito 10.7.1. 
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 10.7.3 Las fallas de cualquier sistema de control de seguridad crítico se responden con prontitud, incluidas, entre otras, las siguientes: 
•	 Restaurando las funciones de seguridad. 
•	 Identificando y documentando la duración (fecha y hora de principio a fin) de la falla de seguridad. 
•	 Identificando y documentando las causas de la falla y documentando el remedio requerido. 
•	 Identificando y abordando cualquier problema de seguridad que surgió durante la falla. 
•	 Determinar si se requieren más acciones como resultado de la falla de seguridad. 
•	 Implementar controles para evitar que se repita la causa de la falla. 
•	 Reanudación del monitoreo de los controles de seguridad.
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad evaluada es un proveedor de servicios hasta el 31 de marzo de 2025, fecha a partir de la cual este requisito se aplicará a todas las entidades.
Este es un requisito actual de la versión 3.2.1 que aplica solo a los proveedores de servicios. Sin embargo, este requisito es una práctica recomendada para todas las demás entidades hasta el 31 de marzo de 2025, después de lo cual será obligatoria y debe considerarse en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |

---

## Hoja: 11

|  | Matriz RACI por requerimiento PCI DSS |  |  |  |  | Código:  | AN-XX |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | Version: | 1 |
|  |  |  |  |  |  |  |  |
| Requisito/Responsable | Requerimiento | Actividad | R | A | C | I | Entregable/Documento |
| Requisito 11: Poner a Prueba Regularmente la Seguridad de los Sistemas y de las Redes | 11.1 Se definen y comprenden los procesos y mecanismos para realizar las actividades del Requisito 11. | 11.1.1 Todas las políticas de seguridad y procedimientos operativos que se identifican en el Requisito 11 son: 
•	 Documentados. 
•	 Actualizados.
•	 En uso.
•	 Conocidos por todas las partes involucradas. |  |  |  |  |  |
|  |  | 11.1.2 Los roles y responsabilidades para realizar las actividades del Requisito 11 son documentados, asignados y comprendidos.
Nuevo requisito - efectivo inmediatamente |  |  |  |  |  |
|  | 11.2 Se identifican y controlan los puntos de acceso inalámbricos y se abordan los puntos de acceso inalámbricos no autorizados. | 11.2.1 Los puntos de acceso inalámbricos autorizados y no autorizados se gestionan de la siguiente manera:
•	 Se comprueba la existencia de puntos de acceso inalámbricos (Wi-Fi) para, 
•	 Detectar e identificar todos los puntos de acceso inalámbricos autorizados y no autorizados, 
•	 Que la verificación, detección e identificación ocurre al menos cada tres meses. 
•	 Si se utiliza la supervisión automatizada, se notifica al personal mediante la generación de alertas.
Notas de Aplicabilidad
Este requisito aplica incluso cuando existe una política que prohíbe el uso de la tecnología inalámbrica, ya que los atacantes no leen ni siguen la política de la empresa.
Los métodos utilizados para cumplir este requisito deben ser suficientes para detectar e identificar tanto los dispositivos autorizados como los no autorizados, incluidos los dispositivos no autorizados conectados a dispositivos que sí están autorizados. |  |  |  |  |  |
|  |  | 11.2 2 Se mantiene un inventario de los puntos de acceso inalámbricos autorizados, incluyendo una justificación de negocio documentada. |  |  |  |  |  |
|  | 11.3 Las vulnerabilidades externas e internas se identifican, se priorizan y se abordan periódicamente. | 11.3.1 Los escaneos de vulnerabilidad interna se realizan de la siguiente manera: 
•	 Al menos una vez cada tres meses.
•	 Se resuelven las vulnerabilidades críticas y de alto riesgo (según las clasificaciones de riesgo de vulnerabilidad de la entidad definidas en el Requisito 6.3.1).
•	 Se realizan re-escaneos que confirman que se han resuelto todas las vulnerabilidades críticas y de alto riesgo (como se indicó anteriormente).
•	 La herramienta de escaneo se mantiene actualizada con la información más reciente sobre vulnerabilidades.
•	 Los escaneos son realizados por personal calificado con la independencia organizacional del probador.
Notas de Aplicabilidad
No es necesario utilizar un QSA o un ASV para realizar escaneos de vulnerabilidad interna.
Los escaneos de vulnerabilidad interna pueden ser realizados por personal interno calificado que sea razonablemente independiente de los componentes del sistema que se analizan (por ejemplo, un administrador de red no debería ser responsable de analizar la red), o una entidad puede optar por una empresa especializada en escaneos de vulnerabilidad. |  |  |  |  |  |
|  |  | 11.3.1.1 Todas las demás vulnerabilidades aplicables (aquellas que no se clasifican como de alto riesgo o críticas (según las clasificaciones de riesgo de vulnerabilidad de la entidad definidas en el Requisito 6.3.1) se gestionan de la siguiente manera: 
•	 Abordado en función del riesgo definido en el análisis de riesgo específico de la entidad, que se realiza de acuerdo con todos los elementos especificados en el Requisito 12.3.1.
•	 Los re-escaneos se realizan según sea necesario.
Notas de Aplicabilidad
El plazo para abordar las vulnerabilidades de menor riesgo está sujeto a los resultados de un análisis de riesgo según el Requisito 12.3.1 que incluye (mínimamente) la identificación de los activos que se protegen, las amenazas y la probabilidad y / o el impacto de una amenaza que se realiza.
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 11.3.1.2 Los escaneos de vulnerabilidad interna se realizan mediante escaneos autenticados como sigue:
•	 Los sistemas que no pueden aceptar credenciales para los escaneos autentificados están documentados.
•	 Se utilizan suficientes privilegios para aquellos sistemas que aceptan credenciales para escanear. 
•	 Si las cuentas utilizadas para el escaneo autenticado se pueden utilizar para el inicio de sesión interactivo, estas se gestionan de acuerdo con el Requisito 8.2.2. 
Notas de Aplicabilidad
Las herramientas de escaneo autenticadas pueden estar basadas en host o en red. 
Los privilegios "suficientes" son los necesarios para ingresar a los recursos del sistema, de modo que se pueda realizar un análisis exhaustivo que detecte vulnerabilidades conocidas. 
Este requisito no se aplica a los componentes del sistema que no pueden aceptar credenciales para escanear. Algunos ejemplos de sistemas que pueden no aceptar credenciales para escanear incluyen algunos dispositivos de red y seguridad, servidores y contenedores.
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 11.3.1.3 Los escaneos de vulnerabilidad interna se realizan después de cualquier cambio significativo como sigue:
•	 Se resuelven las vulnerabilidades críticas y de alto riesgo (según las clasificaciones de riesgo de vulnerabilidad de la entidad definidas en el Requisito 6.3.1).
•	 Los re-escaneos se realizan según sea necesario.
•	 Los escaneos son realizados por personal cualificado con la independencia organizacional del probador (no se requiere que sea un QSA o ASV). 
Notas de Aplicabilidad
No se requiere el escaneo de vulnerabilidad interna autenticado según el Requisito 11.3.1.2 para los análisis realizados después de cambios significativos. |  |  |  |  |  |
|  |  | 11.3.2  Los escaneos de vulnerabilidad externa se realizan de la siguiente manera:
•	 Al menos una vez cada tres meses.
•	 Por parte de un Proveedor de Escaneo Aprobado por PCI SSC (ASV). 
•	 Las vulnerabilidades se resuelven y se cumple con los requisitos de la Guía del Programa ASV.
•	 Se realizan nuevos escaneos según sea necesario para confirmar que las vulnerabilidades se han resuelto de acuerdo con los requisitos de la Guía del Programa ASV escaneos aprobados.
Notas de Aplicabilidad
Para la conformidad inicial PCI DSS no es necesario que se completen cuatro escaneos aprobados en un plazo de 12 meses si el evaluador verifica que: 1) el resultado del escaneo más reciente fue un escaneo satisfactorio, 2) la entidad ha documentado políticas y procedimientos que requieren escaneos al menos una vez cada tres meses, y 3) las vulnerabilidades observadas en los resultados del escaneo se han corregido como se muestra en un re-escaneo. 
(continúa en la página siguiente)
Sin embargo, durante los años siguientes después de la evaluación inicial de PCI DSS, deben haberse realizado escaneos aprobados al menos cada tres meses.
Las herramientas de escaneo de ASV pueden escanear una amplia gama de tipos y topologías de redes. Cualquier detalle sobre el entorno de destino (por ejemplo, distribuidores de carga, proveedores externos, ISP, configuraciones específicas, protocolos en uso, interferencia de escaneo) debe resolverse entre el ASV y el cliente de escaneo.
Consulte la Guía del Programa ASV publicada en el sitio web de PCI SSC para conocer las responsabilidades del cliente de escaneo, la preparación del escaneo, etc.  |  |  |  |  |  |
|  |  | 11.3.2.1 Los escaneos de vulnerabilidad externa se realizan después de cualquier cambio significativo de la siguiente manera:
•	 Se resuelven las vulnerabilidades calificadas con 4.0 o más por CVSS.
•	 Los re-escaneos se realizan según sea necesario.
•	 Los escaneos son realizados por personal cualificado con la independencia organizacional del probador (no se requiere que sea un QSA o ASV).  |  |  |  |  |  |
|  | 11.4 Las pruebas de penetración externas e internas se realizan con regularidad y se corrigen las vulnerabilidades explotables y las debilidades de seguridad. | 11.4.1 La entidad define, documenta e implementa una metodología de prueba de penetración, que incluye: 
•	 Enfoques de pruebas de penetración aceptados por la industria.
•	 Cobertura para todo el perímetro de CDE y sus sistemas críticos. 
•	 Pruebas tanto dentro como fuera de la red. 
•	 Pruebas para validar cualquier control de segmentación y reducción del alcance. 
•	 Pruebas de penetración a nivel de la aplicación para identificar, como mínimo, las vulnerabilidades enumeradas en el Requisito 6.2.4. 
•	 Las pruebas de penetración a nivel de red que abarcan todos los componentes que apoyan las funciones de red y los sistemas operativos. 
•	 Revisión y consideración de amenazas y vulnerabilidades experimentadas en los últimos 12 meses. 
•	 Enfoque documentado para evaluar y abordar el riesgo que plantean las vulnerabilidades explotables y las debilidades de seguridad encontradas durante las pruebas de penetración. 
•	 Retención de los resultados de las pruebas de penetración y los resultados de las actividades de remediación durante al menos 12 meses.
Notas de Aplicabilidad
Realizar pruebas desde el interior de la red (o "pruebas de penetración interna") significa pruebas tanto desde el interior del CDE como hacia el CDE desde redes internas confiables y no confiables. 
Realizar pruebas desde fuera de la red (o pruebas de penetración "externas") significa probar el perímetro externo expuesto de las redes confiables, y de los sistemas críticos conectados o accesibles a las infraestructuras de redes públicas.
 |  |  |  |  |  |
|  |  | 11.4.2 Se realizan pruebas de penetración interna:
•	 Según la metodología definida por la entidad 
•	 Al menos una vez cada 12 meses 
•	 Después de cualquier actualización o cambio significativo de infraestructura o aplicación
•	 Por un recurso interno calificado o un tercero externo calificado
•	 El evaluador cuenta con independencia organizacional (no se requiere que sea un QSA o ASV). |  |  |  |  |  |
|  |  | 11.4.3 Se realizan pruebas de penetración externa: 
•	 Según la metodología definida por la entidad 
•	 Al menos una vez cada 12 meses 
•	 Después de cualquier actualización o cambio significativo de infraestructura o aplicación
•	 Por un recurso interno calificado o un tercero externo calificado
•	 El evaluador cuenta con independencia organizacional (no se requiere que sea un QSA o ASV). |  |  |  |  |  |
|  |  | 11.4.4 Las vulnerabilidades explotables y las debilidades de seguridad encontradas durante las pruebas de penetración se corrigen de la siguiente manera:
•	 De acuerdo con la evaluación de la entidad, del riesgo que representa el problema de seguridad según se define en el Requisito 6.3.1.
•	 La prueba de penetración se repite para verificar las correcciones. |  |  |  |  |  |
|  |  | 11.4.5 Si la segmentación se utiliza para aislar el CDE de otras redes, las pruebas de penetración se realizan en los controles de segmentación de la siguiente manera:
•	 Al menos una vez cada 12 meses y después de cualquier cambio en los controles/métodos de segmentación 
•	 Cubriendo todos los controles/métodos de segmentación en uso.
•	 De acuerdo con la metodología de prueba de penetración definida por la entidad.
•	 Confirmar que los controles/métodos de segmentación son operativos y eficientes, y aislar al CDE de todos los sistemas fuera del ámbito.
•	 Confirmar la efectividad de cualquier uso de aislamiento para separar sistemas con diferentes niveles de seguridad (ver Requisito 2.2.3).
•	 Realizado por un recurso interno calificado o un tercero externo calificado.
•	 El evaluador cuenta con independencia organizacional (no se requiere que sea un QSA o ASV).

 |  |  |  |  |  |
|  |  | 11.4.6 Requisito adicional sólo para proveedores de servicios: Si la segmentación se utiliza para aislar el CDE de otras redes, las pruebas de penetración se realizan en los controles de segmentación de la siguiente manera: 
•	 Al menos una vez cada seis meses y después de cualquier cambio en los controles/métodos de segmentación. 
•	 Cubriendo todos los controles/métodos de segmentación en uso.
•	 De acuerdo con la metodología de prueba de penetración definida por la entidad.
•	 Confirmar que los controles/métodos de segmentación son operativos y eficientes, y aislar al CDE de todos los sistemas fuera del ámbito.
•	 Confirmar la efectividad de cualquier uso de aislamiento para separar sistemas con diferentes niveles de seguridad (ver Requisito 2.2.3).
•	 Realizado por un recurso interno calificado o un tercero externo calificado.
•	 El evaluador cuenta con independencia organizacional (no se requiere que sea un QSA o ASV).
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad que se evalúa es un proveedor de servicios. |  |  |  |  |  |
|  |  | 11.4.7 Requisito adicional sólo para proveedores de servicios alojados/en la nube de terceros: Los proveedores de servicios alojados/en la nube de terceros apoyan a sus clientes para las pruebas de penetración externas según los Requisitos 11.4.3 y 11.4.4.
Notas de Aplicabilidad
Para cumplir con este requisito, los proveedores de servicios alojados/en la nube de terceros pueden: 
•	Proporcionar evidencia a sus clientes para demostrar que se han realizado pruebas de penetración de acuerdo con los Requisitos 11.4.3 y 11.4.4 en la infraestructura suscrita por los clientes, o 
•	Brindar acceso rápido a cada uno de sus clientes para que puedan realizar sus propias pruebas de penetración.
La evidencia proporcionada a los clientes puede incluir resultados de pruebas de penetración redactados, pero debe incluir información suficiente para demostrar que todos los elementos de los Requisitos 11.4.3 y 11.4.4 se han cumplido en nombre del cliente. 
Este requisito se aplica solo cuando la entidad que se evalúa es un proveedor de servicios que gestiona entornos en la nube/host de terceros.
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  | 11.5 Las intrusiones de red y los cambios inesperados de archivos se detectan y se responden. | 11.5.1 Las técnicas de detección y/o prevención de intrusiones se utilizan para detectar y/o impedir intrusiones en la red de la siguiente manera: 
•	 Todo el tráfico se supervisa en el perímetro del CDE. 
•	 Todo el tráfico se supervisa en los puntos críticos del CDE. 
•	 Se envía una alerta al personal indicando las sospechas de situaciones comprometidas. 
•	 Todos los motores de detección y prevención de intrusiones, las líneas de base y las firmas se mantienen actualizadas. |  |  |  |  |  |
|  |  | 11.5.1.1 Requisito adicional sólo para proveedores de servicios: Las técnicas de detección-intrusión y/o intrusión-prevención detectan, alertan/impiden y abordan los canales de comunicación de malware encubierto.
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad que se evalúa es un proveedor de servicios.
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 11.5.2 Un mecanismo de detección de cambios (por ejemplo, herramientas de monitoreo de integridad de archivos) se despliega como sigue:
•	 Para alertar al personal sobre modificaciones no autorizadas (incluyendo cambios, adiciones y eliminaciones) de archivos críticos 
•	 Para realizar comparaciones de archivos críticos al menos una vez por semana.
Notas de Aplicabilidad
A efectos de detección de cambios, los archivos críticos suelen ser aquellos que no cambian regularmente, pero cuya modificación podría indicar poner en riesgo el sistema o comprometerlo. Los mecanismos de detección de cambios, como los productos de monitoreo de la integridad de los archivos, suelen venir pre-configurados con archivos críticos para el sistema operativo correspondiente. Otros archivos críticos, como los de las aplicaciones personalizadas, deben ser evaluados y definidos por la entidad (es decir, el comerciante o proveedor de servicios). |  |  |  |  |  |
|  | 11.6 Se detectan los cambios no autorizados en las páginas de pago se detectan y se responden. | 11.6.1 El mecanismo de detección de cambios y manipulaciones se despliega de la siguiente manera:
•	 Para enviar alertas al personal sobre modificaciones no autorizadas (incluyendo indicadores de situaciones comprometidas, cambios, adiciones y supresiones) en los encabezados HTTP y en el contenido de las páginas de pago tal y como las recibe el navegador del consumidor.
•	 El mecanismo está configurado para evaluar el encabezamiento HTTP y la página de pago recibidas. 
•	 Las funciones del mecanismo se realizan de la siguiente manera:
- Al menos una vez cada siete días 
O
- Periódicamente, (a una frecuencia definida en el análisis de riesgos específico de la entidad, el cual se desarrolla de acuerdo a todos los elementos especificados en el Requisito 12.3.1). 
Notas de Aplicabilidad
La intención de este requisito no es que una entidad necesite instalar software en los sistemas o navegadores de sus consumidores, sino que la entidad utilice técnicas como las descritas en los Ejemplos anteriores para detectar e impedir actividades inesperadas de scripts.
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |

---

## Hoja: 12

|  | Matriz RACI por requerimiento PCI DSS |  |  |  |  | Código:  | AN-XX |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | Version: | 1 |
|  |  |  |  |  |  |  |  |
| Requisito/Responsable | Requerimiento | Actividad | R | A | C | I | Entregable/Documento |
| Requisito 12: Respaldar la Seguridad de la Información con Políticas y Programas Organizacionales | 12.1 Una política integral de seguridad de la información que rija y proporcione orientación para la protección de los activos de información de la entidad es actualizada y bien conocida. | 12.1.1 Una política general de seguridad informática es: 
•	 Establecida.
•	 Publicada.
•	 Mantenida.
•	 Difundida a todo el personal relevante, así como a los proveedores y socios comerciales relevantes. |  |  |  |  |  |
|  |  | 12.1.2 La política de seguridad de la información es:
•	 Revisada al menos una vez cada 12 meses.
•	 Actualizada según sea necesario para reflejar los cambios en los objetivos de negocios o en los riesgos para el entorno.
 |  |  |  |  |  |
|  |  | 12.1.3 La política de seguridad define claramente los roles y responsabilidades de seguridad de la información para todo el personal, y todo el personal conoce y reconoce sus responsabilidades en materia de seguridad de la información. |  |  |  |  |  |
|  |  | 12.1.4 La responsabilidad de la seguridad de la información se asigna formalmente a un director de seguridad de la información o a otro miembro de la dirección ejecutiva con conocimientos de seguridad de la información.  |  |  |  |  |  |
|  | 12.2 Se definen e implementan políticas de uso aceptable para tecnologías de usuario final. | 12.2.1 Se documentan e implementan políticas de uso aceptable para tecnologías orientadas al usuario final, que incluyen:
•	 Aprobación explícita por las partes autorizadas.
•	 Usos aceptables de la tecnología.
•	 Lista de productos aprobados por el comerciante para uso de los empleados, incluidos hardware y software.
Notas de Aplicabilidad
Ejemplos de tecnologías orientadas al usuario final para las que se espera sean aplicadas políticas de uso aceptable son, entre otras, tecnologías inalámbricas y de acceso remoto, computadoras portátiles, tabletas, teléfonos móviles y medios electrónicos extraíbles, uso del correo electrónico y uso de Internet. |  |  |  |  |  |
|  | 12.3 Los riesgos para el entorno de datos de tarjetahabientes se identifican, evalúan y gestionan formalmente. | 12.3.1 Cada requisito PCI DSS que proporciona flexibilidad sobre la frecuencia con la que se realizan (por ejemplo, los requisitos que deben realizarse periódicamente) están apoyados por un análisis de riesgo específico que está documentado e incluye: 
•	 Identificación de los activos a proteger. 
•	 Identificación de las amenazas contra las que protege el requisito.
•	 Identificación de factores que contribuyen a la probabilidad y/o impacto de que se materialice una amenaza. 
•	 Análisis resultante que determine e incluya la justificación de la frecuencia con la que se debe realizar el requisito para minimizar la probabilidad de que se materialice la amenaza.
•	 Revisión de cada análisis de riesgo específico al menos una vez cada 12 meses para determinar si los resultados siguen siendo válidos o si se necesita un análisis de riesgo actualizado.
•	 Realización de análisis de riesgos actualizados cuando sea necesario, según lo determinado por la revisión anual. 
Notas de Aplicabilidad
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 12.3.2 Se realiza un análisis de riesgos específico para cada Requisito PCI DSS que la entidad cumple con el Enfoque personalizado, para que incluya:
•	 Evidencia documentada que detalla cada elemento se especifica en el Anexo B: Directrices e instrucciones para el Uso del Enfoque Personalizado (incluyendo, como mínimo, una matriz de controles y un análisis de riesgos).
•	 Aprobación de las evidencias documentadas por parte de la alta dirección.
•	 La realización del análisis de riesgos específico al menos una vez cada 12 meses.
Nuevo requisito - efectivo inmediatamente
Notas de Aplicabilidad
Esto sólo se aplica a las entidades que utilizan un Enfoque Personalizado.
 |  |  |  |  |  |
|  |  | 12.3.3 Los conjuntos de cifrado criptográfico y los protocolos en uso se documentan y revisan al menos una vez cada 12 meses, incluyendo al menos lo siguiente:
•	 Un inventario actualizado de todos los protocolos y conjuntos de cifrado criptográfico en uso, incluyendo su propósito y dónde se utilizan.
•	 Monitoreo activo de las tendencias de la industria con respecto a la viabilidad continua de todos los protocolos y conjuntos de cifrado criptográfico en uso.
•	 Una estrategia documentada para responder a los cambios anticipados en las vulnerabilidades criptográficas.
Notas de Aplicabilidad
El requisito se aplica a todos los conjuntos y protocolos criptográficos utilizados para cumplir con los requisitos PCI DSS.
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 12.3.4 Las tecnologías de hardware y software en uso se revisan al menos una vez cada 12 meses, incluyendo al menos lo siguiente:
•	 Análisis de que las tecnologías continúan recibiendo correcciones de seguridad por parte de los proveedores con prontitud.
•	 Análisis de que las tecnologías continúan apoyando (y no imposibilitan) la conformidad PCI DSS de la entidad.
•	 Documentación de cualquier anuncio o tendencia de la industria relacionada con una tecnología, como cuando un proveedor ha anunciado planes para el "fin de la vida útil" de una tecnología.
•	 Documentación de un plan, aprobado por la alta gerencia, para remediar tecnologías obsoletas, incluidas aquellas para las que los proveedores han anunciado planes de "fin de vida útil".
Notas de Aplicabilidad
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  | 12.4 Gestión del cumplimiento con PCI DSS. | 12.4.1 Requisito adicional sólo para proveedores de servicios: La responsabilidad es establecida por la gerencia ejecutiva para la protección de datos de tarjetahabientes y un programa de conformidad PCI DSS que incluye: 
•	 Responsabilidad general para mantener la conformidad PCI DSS.
•	 Definición de un estatuto para un programa de conformidad PCI DSS y un reporte a la dirección ejecutiva.
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad que se evalúa es un proveedor de servicios.
La dirección ejecutiva puede incluir puestos de nivel C, junta directiva o equivalente. Los títulos específicos dependerán de la estructura organizacional particular.
La responsabilidad del programa de conformidad de PCI DSS se puede asignar a roles individuales y/o a unidades comerciales dentro de la organización. |  |  |  |  |  |
|  |  | 12.4.2 Requisito adicional sólo para proveedores de servicios: Las revisiones se realizan al menos una vez cada tres meses para confirmar que el personal está realizando sus tareas de acuerdo con todas las políticas de seguridad y los procedimientos operativos. Las revisiones son realizadas por personal distinto al responsable de realizar la tarea en cuestión e incluyen, entre otras, las siguientes tareas: 
• 	Revisiones de registros diarios. 
• 	Revisiones de configuración para controles de seguridad de la red. 
• 	 Aplicación de estándares de configuración a nuevos sistemas. 
• 	 Respuesta a las alertas de seguridad. 
•  	Procesos de gestión del cambio.
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad evaluada es un proveedor de servicios. |  |  |  |  |  |
|  |  | 12.4.2.1 Requisito adicional sólo para proveedores de servicios: Las revisiones realizadas de acuerdo con el Requisito 12.4.2 se documentan para incluir: 
•	 Resultados de las revisiones. 
•	 Acciones de remediación documentadas tomadas para cualquier tarea que no se haya realizado en el Requisito 12.4.2.
•	 Revisión y aprobación de los resultados por parte del personal al que se le haya asignado la responsabilidad del programa de conformidad PCI DSS.
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad que se evalúa es un proveedor de servicios. |  |  |  |  |  |
|  | 12.5 Documentación y validación del alcance PCI DSS. | 12.5.1 Se mantiene y actualiza un inventario de los componentes del sistema que están dentro del alcance PCI DSS, incluyendo una descripción de su función/uso. |  |  |  |  |  |
|  |  | 12.5.2  El alcance PCI DSS es documentado y confirmado por la entidad al menos una vez cada 12 meses y ante cambios significativos en el entorno dentro del alcance. Como mínimo, la validación del alcance incluye:
•	 Identificar todos los flujos de datos para las diversas etapas de pago (por ejemplo, autorización, captura de la liquidación, devoluciones y reembolsos) y canales de aceptación (por ejemplo, tarjeta física, tarjeta virtual y comercio electrónico).
•	 Actualizar todos los diagramas de flujo de datos según el Requisito 1.2.4.
•	 Identificar todas las ubicaciones donde se almacenan, procesan y transmiten datos de tarjetahabientes, incluidos, entre otros: 1) cualquier ubicación fuera del CDE definida actualmente, 2) aplicaciones que procesan CHD, 3) transmisiones entre sistemas y redes, y 4) copias de seguridad de archivos.
•	 Identificar todos los componentes del sistema en el CDE, conectados al CDE o que podrían afectar la seguridad del CDE.
•	 Identificar todos los controles de segmentación en uso y los entornos desde los que se segmenta el CDE, incluida la justificación de los entornos que están fuera del alcance.
•	 Identificar todas las conexiones de entidades de terceros con acceso al CDE.
•	 Confirmar que todos los flujos de datos identificados, datos de tarjetahabientes, componentes del sistema, controles de segmentación y conexiones de terceros con acceso al CDE están incluidos en el alcance.
Nuevo requisito - efectivo inmediatamente
Notas de Aplicabilidad
Se espera que esta confirmación anual del alcance PCI DSS sea una actividad realizada por la entidad que se está evaluando, y no es la misma, ni pretende ser reemplazada por, la confirmación del alcance realizada por el evaluador de la entidad durante la evaluación anual. |  |  |  |  |  |
|  |  | 12.5.2.1 Requisito adicional sólo para proveedores de servicios: El alcance PCI DSS es documentado y confirmado por la entidad al menos una vez cada seis meses y después de cambios significativos en el entorno dentro del alcance. Como mínimo, la validación del alcance incluye todos los elementos especificados en el Requisito 12.5.2.
Notas de Aplicabilidad
 Este requisito se aplica solo cuando la entidad que se evalúa es un proveedor de servicios.
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, fecha a partir de la cual será obligatorio y deberá tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 12.5.3 Requisito adicional sólo para proveedores de servicios: Los cambios significativos en la estructura organizativa dan como resultado una revisión documentada (interna) del impacto en el alcance PCI DSS y la aplicabilidad de los controles; los resultados se comunican a la dirección ejecutiva.
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad que se evalúa es un proveedor de servicios.
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  | 12.6 La educación en concienciación sobre la seguridad es una actividad continua | 12.6.1 Se implementa un programa formal de concientización sobre seguridad para que todo el personal conozca la política y los procedimientos de seguridad de la información a de la entidad, y el rol del personal en la protección de los datos de tarjetahabientes. |  |  |  |  |  |
|  |  | 12.6.2 El programa de concientización sobre seguridad es: 
•	 Revisado al menos una vez cada 12 meses, y 
•	 Actualizado según sea necesario para abordar cualquier nueva amenaza y vulnerabilidad que pueda impactar la seguridad del CDE de la entidad, o la información proporcionada al personal sobre sus funciones en lo concerniente a la protección de los datos de tarjetahabientes.
Notas de Aplicabilidad
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 12.6.3 El personal recibe capacitación sobre seguridad de la siguiente manera: 
•	 Al momento de la contratación y al menos una vez cada 12 meses.
•	 Se utilizan múltiples métodos de comunicación.
•	 El personal reconoce al menos una vez cada 12 meses que ha leído y comprendido las políticas y los procedimientos de seguridad de la información.  |  |  |  |  |  |
|  |  | 12.6.3.1 El entrenamiento de concientización de seguridad incluye la concientización ante amenazas y vulnerabilidades que podrían impactar la seguridad del CDE, incluyendo, pero no limitado a:
•	 Phishing y ataques relacionados. 
•	 Ingeniería social.
Notas de Aplicabilidad
Véase el requisito 5.4.1 para obtener orientación sobre la diferencia entre los controles técnicos y automatizados para detectar y proteger a los usuarios de los ataques de phishing y este requisito, para proporcionar a los usuarios capacitación en concientización sobre seguridad en materia de suplantación de identidad e ingeniería social. Se trata de dos requisitos distintos y separados, y uno de ellos no se cumple aplicando los controles exigidos por el otro.
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 12.6.3.2 La capacitación en concientización sobre seguridad incluye la concientización sobre el uso aceptable de las tecnologías de usuario final de acuerdo con el requisito 12.2.1.
Notas de Aplicabilidad
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  | 12.7 El personal es evaluado para reducir los riesgos de amenazas internas. | 12.7.1 El personal potencial que tendrá acceso al CDE es investigado, en el marco de las limitaciones que establecen las leyes locales, antes de su contratación, a fin de minimizar el riesgo de ataques provenientes de fuentes internas. 
Notas de Aplicabilidad
Para el personal potencial que vaya a ser contratado para puestos como los de cajeros en tiendas, que sólo tienen acceso a un número de tarjeta a la vez cuando facilitan una transacción, este requisito es sólo una recomendación. |  |  |  |  |  |
|  | 12.8 Gestión del riesgo de los activos de información asociados a las relaciones con proveedores de servicios externos (TPSP). | 12.8.1 Se mantiene una lista de todos los proveedores de servicios de terceros (TPSP) con los que se comparten datos de tarjetahabientes o que podrían afectar a la seguridad de los datos de tarjetahabientes, incluyendo una descripción para cada uno de los servicios prestados.
Notas de Aplicabilidad
El uso de un TPSP que cumpla con PCI DSS no hace que una entidad esté en conformidad con PCI DSS, ni elimina la responsabilidad de la entidad por su propia conformidad PCI DSS. |  |  |  |  |  |
|  |  | 12.8.2 Se mantienen acuerdos escritos con los TPSP de la siguiente manera: 
•	 Se mantienen acuerdos escritos con todos los TPSP con los que se comparten datos de tarjetahabientes o que podrían afectar la seguridad del CDE.
•	 Los acuerdos escritos incluyen el reconocimiento por parte de los TPSP de que son responsables por la seguridad de los datos de tarjetahabientes que los TPSP poseen o almacenan, procesan o transmiten en nombre de la entidad, o en la medida en que puedan afectar a la seguridad del CDE de la entidad. 
Notas de Aplicabilidad
La redacción exacta de un reconocimiento dependerá del acuerdo entre las dos partes, los detalles del servicio que se presta y las responsabilidades asignadas a cada parte. El reconocimiento no tiene que incluir la redacción exacta prevista en este requisito.
La prueba de que un TPSP cumple con los requisitos PCI DSS (por ejemplo, un Certificado de Conformidad PCI DSS (AOC) o una declaración en el sitio web de la empresa) no es lo mismo que el acuerdo escrito especificado en este requisito.  |  |  |  |  |  |
|  |  | 12.8.3 Se implementa un proceso establecido para contratar a los TPSP, incluyendo la debida diligencia antes de la contratación. |  |  |  |  |  |
|  |  | 12.8.4 Se implementa un programa para monitorear el estado de conformidad PCI DSS de los TPSP al menos una vez cada 12 meses. 
Notas de Aplicabilidad
Cuando una entidad tiene un acuerdo con un TPSP para cumplir con los requisitos PCI DSS en nombre de la entidad (por ejemplo, a través de un servicio de firewall), la entidad debe trabajar con el TPSP para asegurarse de que se cumplan los requisitos PCI DSS aplicables. Si el TPSP no cumple con los requisitos PCI DSS aplicables, entonces, esos requisitos también están “no en cumplimiento” para la entidad. |  |  |  |  |  |
|  |  | 12.8.5 Se mantiene información sobre qué requisitos PCI DSS gestiona cada TPSP, cuáles gestiona la entidad y cualquiera que se comparta entre el TPSP y la entidad. |  |  |  |  |  |
|  | 12.9 Los proveedores de servicios externos (TPSP) apoyan la conformidad PCI DSS de sus clientes. | 12.9.1 Requisito adicional sólo para proveedores de servicios: Los TPSP reconocen por escrito a los clientes que son responsables por la seguridad de los datos de tarjetahabientes que el TPSP posee o almacena, procesa o transmite en nombre del cliente, o en la medida en que puedan afectar la seguridad del CDE del cliente. 
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad que se evalúa es un proveedor de servicios.
La redacción exacta de un reconocimiento dependerá del acuerdo entre las dos partes, los detalles del servicio que se presta y las responsabilidades asignadas a cada parte. El reconocimiento no tiene que incluir la redacción exacta prevista en este requisito. |  |  |  |  |  |
|  |  | 12.9.2 Requisito adicional sólo para proveedores de servicios: Los TPSP apoyan las solicitudes de información de sus clientes para cumplir con los Requisitos 12.8.4 y 12.8.5 proporcionando lo siguiente a pedido del cliente:
•	 Información del estado de conformidad PCI DSS para cualquier servicio que el TPSP realice en nombre de los clientes (Requisito 12.8.4).
•	 Información sobre qué requisitos PCI DSS son responsabilidad del TPSP y cuáles son responsabilidad del cliente, incluyendo las responsabilidades compartidas (Requisito 12.8.5). 
Nuevo requisito - efectivo inmediatamente
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad que se evalúa es un proveedor de servicios. |  |  |  |  |  |
|  | 12.10 Respuesta inmediata a incidentes de seguridad sospechosos y confirmados que podrían afectar al CDE. | 12.10.1 Existe un plan de respuesta a incidentes y está listo para activarse en caso de sospecha o confirmación de un incidente de seguridad. El plan incluye, pero no se limita a: 
•	 Funciones, responsabilidades y estrategias de comunicación y contacto en caso de sospecha o confirmación de un incidente de seguridad, incluyendo la notificación de marcas de pago y adquirentes, como mínimo.
•	 Procedimientos de respuesta a incidentes con actividades específicas de contención y mitigación para diferentes tipos de incidentes.
•	 Procedimientos de recuperación y continuidad del negocio.
•	 Procesos de apoyo de datos.
•	 Análisis de requisitos legales para reportar situaciones comprometidas.
•	 Cobertura y respuestas de todos los componentes críticos del sistema.
•	 Referencia o inclusión de procedimientos de respuesta a incidentes de las marcas de pago.  |  |  |  |  |  |
|  |  | 12.10.2 Al menos una vez cada 12 meses, el plan de respuesta a incidentes de seguridad es: 
•	 Revisado y el contenido se actualiza según sea necesario.
•	 Probado, incluyendo todos los elementos enumerados en el Requisito 12.10.1. |  |  |  |  |  |
|  |  | 12.10.3 Se designa personal específico para estar disponible las 24 horas del día, los 7 días de la semana a fin de responder a incidentes de seguridad sospechosos o confirmados. |  |  |  |  |  |
|  |  | 12.10.4 El personal responsable de responder a incidentes de seguridad sospechados y confirmados recibe capacitación adecuada y periódica sobre sus responsabilidades en la respuesta a incidentes. |  |  |  |  |  |
|  |  | 12.10.4.1 La frecuencia de la capacitación periódica del personal de respuesta a incidentes es definida según el análisis de riesgos específico de la entidad, que se realiza de acuerdo con todos los elementos especificados en el requisito 12.3.1.
Notas de Aplicabilidad
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  |  | 12.10.5 El plan de respuesta a incidentes de seguridad incluye el monitoreo y la respuesta a las alertas de los sistemas de monitoreo de seguridad, incluyendo, pero no limitado a: 
•	 Sistemas de detección y prevención de intrusiones. 
•	 Controles de seguridad de la red.
•	 Mecanismos de detección de cambios en archivos críticos.
•	 El mecanismo de detección de cambios y manipulaciones en las páginas de pago. Este punto es la mejor práctica hasta su fecha de vigencia; consulte las Notas de Aplicabilidad que aparecen a continuación para obtener más detalles. 
•	 Detección de puntos de acceso inalámbricos no autorizados.
Notas de Aplicabilidad
El punto anterior (para supervisar y responder a las alertas de un mecanismo de detección de cambios y manipulaciones para las páginas de pago) es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual se exigirá como parte del Requisito 12.10.5 y deberá tenerse plenamente en cuenta durante una evaluación PCI DSS.
 |  |  |  |  |  |
|  |  | 12.10.6 El plan de respuesta a incidentes de seguridad se modifica y evoluciona de acuerdo con las lecciones aprendidas y para incorporar los desarrollos de la industria. |  |  |  |  |  |
|  |  | 12.10.7 Existen procedimientos de respuesta a incidentes que se iniciarán cuando se detecten datos de PAN almacenados en un lugar inesperado, e incluyen:
•	 Determinar qué hacer si se descubren datos de PAN fuera del CDE, incluyendo su recuperación, eliminación segura y/o migración al CDE actualmente definido, según corresponda.
•	 Identificar si los datos confidenciales de autenticación se almacenan con datos de PAN. 
•	 Determinar de dónde proceden los datos de tarjetahabientes y cómo han llegaron donde no se esperaba.
•	 Remediar fugas de datos o brechas en el proceso que llevaron a que los datos del tarjetahabientes llegaran a una ubicación inesperada. 
Notas de Aplicabilidad
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |

---

## Hoja: A1 - 2

|  | Matriz RACI por requerimiento PCI DSS |  |  |  |  | Código:  | AN-XX |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | Version: | 1 |
|  |  |  |  |  |  |  |  |
| Requisito/Responsable | Requerimiento | Actividad | R | A | C | I | Entregable/Documento |
| Anexo A1: Requisitos Adicionales de PCI DSS para Proveedores de Alojamiento Compartido | A1.1 Los proveedores de servicios multi-usuario protegen y segregan todos los entornos y datos de los clientes. | A1.1.1 La separación lógica se implementa de la siguiente manera:
•	 El proveedor no puede ingresar a los entornos de sus clientes sin autorización.
•	 Los clientes no pueden ingresar al entorno del proveedor sin autorización.
Notas de Aplicabilidad
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS.
 |  |  |  |  |  |
|  |  | A1.1.2 Los controles se implementan de modo que cada cliente solo tenga permiso para ingresar a sus propios datos de tarjetahabientes y CDE. |  |  |  |  |  |
|  |  | A1.1.3 Los controles se implementan de modo que cada cliente solo pueda ingresar a los recursos que se le han asignados. |  |  |  |  |  |
|  |  | A1.1.4 La eficiencia de los controles de separación lógica utilizados para separar los entornos de los clientes se confirma al menos una vez cada seis meses mediante pruebas de penetración. 
Notas de Aplicabilidad
La prueba de separación adecuada entre los clientes en un entorno de proveedor de servicios multiusuario se suma a las pruebas de penetración especificadas en el Requisito 11.4.6.
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
|  | A1.2 Los proveedores de servicios multiusuario facilitan el registro y la respuesta a incidentes para todos los clientes. | A1.2.1 La función de registro de auditoría está habilitada para el entorno de cada cliente de conformidad con el Requisito 10 PCI DSS, que incluye lo siguiente:
•	 Los registros están habilitados para aplicaciones comunes de terceros.
•	 Los registros están activos de forma predeterminada.
•	 Los registros están disponibles para revisión solo por parte del cliente propietario.
•	 Las ubicaciones de los registros se comunican claramente al cliente propietario.
•	 Los datos de registro y la disponibilidad son consistentes con el Requisito 10 de los PCI DSS |  |  |  |  |  |
|  |  | A1.2.2 Se implementan procesos o mecanismos para apoyar y/o facilitar investigaciones forenses rápidas en caso de un incidente de seguridad sospechado o confirmado para cualquier cliente. |  |  |  |  |  |
|  |  | A1.2.3 Se implementan procesos o mecanismos para reportar y abordar vulnerabilidades e incidentes de seguridad presuntos o confirmados, incluyendo lo siguiente:
•	 Los clientes pueden informar de forma segura los incidentes de seguridad y las vulnerabilidades al proveedor. 
•	 El proveedor aborda y repara los incidentes de seguridad y las vulnerabilidades sospechadas o confirmadas de acuerdo con el Requisito 6.3.1.
Notas de Aplicabilidad
Este requisito es la mejor práctica recomendada hasta el 31 de marzo de 2025, después de lo cual será obligatorio y debe tenerse en cuenta en su totalidad durante una evaluación PCI DSS. |  |  |  |  |  |
| Anexo A2: Requisitos Adicionales de PCI DSS para Entidades que Utilizan SSL/Primeras Versiones de TLS para Conexiones de Terminal POS POI Presencial con Tarjetas

Nota: No se puede utilizar SSL/Primeras Versiones de TLS como control de seguridad, excepto por los terminales POS POI que son verificados como  no susceptibles a exploits conocidos y los puntos de terminación a los que se conectan, como se define en este Anexo. |  | A2.1.1 Cuando los terminales POS POI en el comercio o en la ubicación de aceptación de pagos usan SSL y/o primeras versiones de, la entidad confirma que los dispositivos no son susceptibles a ninguna vulnerabilidad conocida para esos protocolos.
Notas de Aplicabilidad
Este requisito está destinado a aplicarse a la entidad con el terminal POS POI, como un comerciante. Este requisito no está destinado a los proveedores de servicios que sirven como punto de terminación o conexión a esos terminales POS POI. Los requisitos A2.1.2 y A2.1.3 se aplican a los proveedores de servicios POS POI.
La asignación para terminales POS POI que actualmente no son susceptibles a vulnerabilidades se basa en los riesgos actualmente conocidos. Si se introducen nuevas vulnerabilidades a las que los terminales POS POI son susceptibles, estas deberán actualizarse inmediatamente. |  |  |  |  |  |
|  |  | A2.1.2  Requisito adicional sólo para proveedores de servicios: Todos los proveedores de servicios con puntos de conexión existentes POS POI que utilizan SSL y/o primeras versiones de TLS como se define en A2.1 cuentan con un Plan de Migración y Mitigación de Riesgos que incluye:
•	 Descripción del uso, incluidos los datos que se transmiten, los tipos y la cantidad de sistemas que usan y/o apoyan SSL/primeras versiones de TLS y el tipo de entorno. 
•	 Resultados de la evaluación de riesgos y controles de reducción de riesgos implementados.
•	 Descripción de procesos para monitorear nuevas vulnerabilidades relacionadas con SSL/primeras versiones de TLS.
•	 Descripción de los procesos de control de cambios que se implementan para garantizar que los SSL/primeras versiones de TLS no se implementen en nuevos entornos.
•	 Descripción general del plan del proyecto de migración para reemplazar los SSL/primeras versiones de TLS en una fecha futura.
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad evaluada es un proveedor de servicios. |  |  |  |  |  |
|  |  | A2.1.3 Requisito adicional sólo para proveedores de servicios: Todos los proveedores de servicios brindan una oferta de servicios segura.
Notas de Aplicabilidad
Este requisito se aplica solo cuando la entidad evaluada es un proveedor de servicios. |  |  |  |  |  |