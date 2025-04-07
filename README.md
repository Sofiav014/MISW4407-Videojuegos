# Enunciado - Ejercicio Entregable Semana 2

Cree un programa que agregue al que entregó en el primer ejercicio el siguiente comportamiento:

- El usuario controla por medio de la entrada de teclado (específicamente las flechas direccionales del teclado) el movimiento de un rectángulo. Con las flechas lo puede mover arriba-abajo e izquierda-derecha un número de pixeles nP por segundo.

- El personaje no puede salir de la pantalla.

- El usuario puede disparar balas con el botón izquierdo del ratón (i.e. cuadrados pequeños de otro color), las cuales salen en la dirección definida desde el personaje hasta la posición del ratón. Las balas salen siempre desde la mitad del personaje a una velocidad nV.

- Si la bala toca otro rectángulo, tanto la bala como el otro rectángulo desaparecen.

- Si la bala llega a alguno de los bordes del juego sin tocar otro rectángulo, desaparece.

- Hay un límite de balas de jugador que pueden existir en el mundo al mismo tiempo, definido por el archivo de configuración del nivel.

- La información de configuración de la bala (tamaño, color, velocidad) junto con la información de movimiento del jugador (nP) se encuentra en el archivo de configuración, además de la información que venía del ejercicio anterior.

## Detalles de configuración 

Va a existir algunos cambios en la configuración, respecto a la configuración anterior. También aparecen nuevos elementos para configurar. 

### Nivel

El nivel posee una modificación adicional para controlar aspectos nuevos del ejercicio:

- Un lugar de origen del jugador que determina donde comienza.

- Un número máximo de balas permitidas en ese nivel.

### Jugador

El jugador va a tener su propia configuración con las siguientes características:

- Un tamaño

- Un color

- Una velocidad de entrada, que determina la velocidad del movimiento con el teclado

### Bala

La bala es disparada desde el centro del rectángulo jugador con el clic izquierdo del ratón. Las propiedades de la bala son:

- Un tamaño

- Un color

- Una velocidad de disparo constante

## Detalles de  implementación

Este ejercicio es una extensión del trabajo desarrollado hasta éste módulo en la semana 1. Para éste nivel tenga en cuenta lo siguiente:

- Se recomienda crear un componente CInputCommand que controla los aspectos del input en el juego.

- Los componentes de tipo etiqueta recomendados, que representan e identifican tipos de entidades en los diferentes sistemas, son CTagPlayer, CTagBullet y CTagEnemy. 

- Los sistemas recomendados para este ejercicio son:

    - Un sistema que controle el input del jugador e invoca las acciones siguiendo el patrón Command.

        - Las acciones del jugador son: PLAYER_LEFT, PLAYER_RIGHT, PLAYER_UP, PLAYER_DOWN y PLAYER_FIRE

        - Recuerde que el sistema de Input debe seguir el patrón Command descrito en el curso

    - Un sistema que controle los límites del jugador

    - Un sistema que controle los limites de las balas y los elimina si se salen de la pantalla

    - Un sistema de colisiones entre el jugador y los enemigos

    - Un sistema de colisiones entre los enemigos y las balas

- Los archivos json han sido modificados, así como existen nuevos archivos de configuración que deben ser tenidos en cuenta.

## Archivos de configuración

Varios ejemplos de archivos de configuración (los cuales serán utilizados para probar en la evaluación) se pueden descargar desde aquí: 

(SEMANA DOS - EJERCICIO - RECURSOS PARA VERIFICACIÓN)
https://misw-4407-desarrollo-de-videojuegos.github.io/web-cohorte-2025-12/

Se espera que, como mínimo, estos archivos de configuración de ejemplo funcionen. Se ofrecen varios para probar diversas situaciones. Solamente deben copiar y pegar reemplazando el contenido de los archivos de configuración.

- Los archivos de configuración que se deben implementar son los siguientes:

    - window.json: Contiene información del título de la ventana, tamaño, fondo y framerate.

    - enemies.json: Contiene información de cada tipo de enemigo existente en el juego.

    - level_01.json: Contiene información del "nivel", en particular a que tiempo

        - Se ha modificado este archivo y contiene información de posición de inicio del jugador y el límite de balas del nivel.

    - player.json: Contiene información del rectángulo del jugador

    - bullet.json: Contiene información de la bala que dispara el jugador

Para los archivos de configuración, es necesario saber cargar archivos de tipo json en Python.
