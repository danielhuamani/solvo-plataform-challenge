# Decisiones

- Crear una app por cada modelo o entidad de negocio, esto va permitir para mas adelante si crece poder migrar cada entidad a un microservicio.
- En las notificaciones se crea un proceso asíncrono porque aveces puede tardar el proceso de envío de email, un sms, etc, y esto puede demorar en la respuesta al cliente
- identificar que cada plataforma es idenpendiente para cada usuario

# Plataforma configuración

- Se creo un endpoint para configurar las notificaciones por plataforma, esto permite que cada usuario pueda configurar sus notificaciones por plataforma.
- Se crea un modelo para almacenar las configuraciones de cada plataforma.

# Notifications

## Sistema de notificaciones

### Decisión
Se diseñó el sistema de notificaciones para que sea **extensible** y fácil de mantener a medida que el producto crezca.

### Enfoque
- Se adopta un enfoque **asíncrono** usando **Celery** para ejecutar el envío de notificaciones fuera del request HTTP.
- Se definió una capa de **canales** en `channels.py` (por ejemplo: log, email, sms) que encapsula la lógica de entrega.
- Se definieron **tareas** en `tasks.py` que ejecutan cada canal de manera independiente.

### Beneficios
- **Escalabilidad**: agregar un nuevo canal implica crear una nueva implementación en `channels.py` y encolar ejecutar su tarea correspondiente.
- **Bajo acoplamiento**: la capa de servicios dispara notificaciones sin conocer detalles internos de cada canal.
- **Evolución futura**: si más adelante se migra el envío de notificaciones a un microservicio, el cambio es más sencillo porque la lógica ya está desacoplada y centralizada.

# Si tuviera 1 millon de usuario

- ** Migración notificación **: Se podría migrar el sistema de notificaciones a un microservicio dedicado que maneje la cola de mensajes y el envío, lo que permitiría escalar horizontalmente y manejar la carga de trabajo de manera más eficiente.
- Agregaria rate limit para las incripciones de device para evitar spam
