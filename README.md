 
Sobre los servicios:
Estos siempre han de recibir 4 parametros, los cuatro primeros y por este orden:
    - id_App: Obligatorio, neceistamos saber que aplicación es la que está intentando acceder
    - user: si es una web que no tiene usuarios definidos o autenticados, indicar "NOMBRE_DE_LA_WEB"
    - ret_code: En principio debe llegar con cero o vacio, en el se retorna el código de error que la BBDD retorna
    - ret_txt: Texto que retorna la BBDD, en principio para el usuario.
    
Siempre retorna los valores "ret_*", que siempre actuan de la siguiente manera, dependiendo de RET_CODE:
    - ret_code = 0: El programa a terminado Ok
        - ret_txt: Texto que retorna la BBDD, en principio para el usuario. No suele hacer falta o es un simple OK
        - request: 2xx

    - ret_code > 0: El programa a terminado Ok, pero quiere indicar alguna particularidad, que se debe indicar en la documentación
        - ret_txt: Texto que retorna la BBDD, en principio para el usuario. No suele hacer falta o es un simple OK
        - Ejemplo: en un login:
            - Si es 0: Login correcto, entrar en el programa
            - Si es 1: Login correcto, pero contraseña va a caducar. Preguntar el usuario si quiere cambiar ya la contrasela porque le va a caducar
            - Si es 2: La contraseña ha caducado, debe cambiarla
            - Si es 3: Tiene que cambiar la contraseña por otros motivos.
        - request: 2xx

    - ret_code < 0:
        - ret_code = -99: Error del sistema. 
            - request: 5xx

        - ret_code entre -98 y -1: Lo mismo que en positivo pero serían errores de sistema. Lo normal es -1 y que ret_txt tenga el mensaje para el usuario. 
            - request: 4xx


Independientemente de esto, que es para control interno y manejo de mensajes, 

---------------------------
1xx - Informativos: Estos códigos indican que la solicitud fue recibida y el servidor está procesándola. Generalmente, no requieren acción por parte del usuario.

100 - Continue: El cliente debe continuar con la solicitud.
101 - Switching Protocols: El servidor acepta cambiar el protocolo.
102 - Processing: (WebDAV) El servidor está procesando la solicitud.

---------------------------
2xx - Éxito: Indican que la solicitud fue recibida, comprendida y aceptada correctamente.

200 - OK: La solicitud fue exitosa.
201 - Created: El recurso fue creado satisfactoriamente.
202 - Accepted: La solicitud fue aceptada para procesamiento, pero no completada.
204 - No Content: Respuesta exitosa sin contenido en el cuerpo.
206 - Partial Content: Respuesta parcial, generalmente para descargas.

---------------------------
3xx - Redirecciones: Indican que se requiere acción adicional para completar la solicitud, generalmente relacionada con redireccionamientos.

301 - Moved Permanently: La URL del recurso ha cambiado permanentemente.
302 - Found: Redirección temporal a otra URL.
303 - See Other: Redirección a una URL para obtener la respuesta.
304 - Not Modified: El recurso no ha cambiado desde la última solicitud (usado con caché).
307 - Temporary Redirect: Redirección temporal, igual que 302 pero más estricto.
308 - Permanent Redirect: Redirección permanente, igual que 301 pero más moderno.

---------------------------
4xx - Errores del cliente: Indican que el cliente hizo algo mal, como una solicitud inválida o acceso no autorizado.

400 - Bad Request: La solicitud tiene un error en la sintaxis.
401 - Unauthorized: Se requiere autenticación.
403 - Forbidden: El servidor entendió la solicitud, pero la rechaza.
404 - Not Found: El recurso solicitado no existe.
405 - Method Not Allowed: El método HTTP no es permitido para este recurso.
409 - Conflict: Conflicto en la solicitud, como una edición concurrente de recursos.
410 - Gone: El recurso ya no está disponible y no volverá a estarlo.


5xx - Errores del servidor: Indican que el servidor falló al procesar una solicitud válida.

500 - Internal Server Error: Error general en el servidor.
501 - Not Implemented: El servidor no soporta la funcionalidad requerida.
502 - Bad Gateway: El servidor recibió una respuesta inválida de otro servidor.
503 - Service Unavailable: El servidor está sobrecargado o en mantenimiento.
504 - Gateway Timeout: El servidor no recibió respuesta a tiempo de otro servidor.
505 - HTTP Version Not Supported: La versión de HTTP no es compatible.


-----------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------

SEGURIDAD

1. Autenticación con JWT: Para que solo usuarios autorizados puedan acceder a tus APIs, tanto desde la web como desde servidores externos.
2. CORS: Para permitir solo llamadas desde dominios confiables (tu web).
3. Rate Limiting: Para prevenir abusos y ataques de fuerza bruta.
4. HTTPS: Obligatorio en producción para proteger la comunicación entre clientes y tu API.
5. Validación de entrada con Pydantic: Para garantizar que las solicitudes sean válidas y evitar inyecciones.

Tambien deberíamos crear un middleware personalizado y ver como mejoramos los logs




Sincronización: Se queda embuclado en tablas grandes



FastAPI
http://127.0.0.1:8000/mallorquina/mll_fichas_tecnicas?id_App=63&user=Prueba&ret_code=0&ret_txt="OK"&origen_path=fichas_tecnicas.xlsx&output_path=salida.html