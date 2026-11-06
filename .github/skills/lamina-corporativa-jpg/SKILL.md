---
name: lamina-corporativa-jpg
description: Convierte un texto/prompt con el detalle de una lámina en UN gráfico JPG 1920x1080 (Full HD, 16:9, pantalla completa) con un diseño corporativo fijo (paleta, tipografía, espaciado, formas, fondos). Usar cuando se pida generar una imagen/lámina/diagrama de arquitectura, componentes, portada o cierre de un producto de software, o cuando se pida que el JPG mantenga el mismo estilo gráfico que los demás.
---

# Imagen corporativa JPG 1920×1080

Este skill **solo genera imágenes JPG individuales**. No arma la presentación, no numera ni ordena láminas, no crea PDF ni PPT: el usuario junta los JPG por su cuenta. Su objetivo es que **todos los JPG compartan exactamente el mismo diseño gráfico**.

Entrada: un texto con el detalle de lo que debe mostrar la imagen (título, puntos, componentes, relaciones, cifras). Salida: un archivo `.jpg` horizontal 16:9 de 1920×1080 px que ocupa toda la pantalla (sin bordes externos). Estilo serio, sobrio y profesional, sin recargar.

## Flujo

1. Leer el prompt y decidir qué representación comunica mejor el contenido (portada/cierre, lista + cifras, arquitectura en capas, cuadrícula de componentes o SVG libre). Si el texto no cabe con holgura, condensarlo o preguntar si se divide en varias imágenes; no reducir la fuente.
2. Cada lámina vive en su propia carpeta `presentacion/lamina-NN/` (NN con dos dígitos: `lamina-01`, `lamina-02`, …). Si el usuario pide "lamina-03", usar ese número; si no lo indica, usar el siguiente libre. Copiar la plantilla más cercana de [templates/](./templates) a `presentacion/lamina-NN/lamina-NN.html` y mantener el `href` del CSS como `../../.github/skills/lamina-corporativa-jpg/assets/slide.css`.
3. Reemplazar el contenido usando **solo** las clases de [assets/slide.css](./assets/slide.css). No inventar estilos, colores ni fuentes.
4. Renderizar:
   ```powershell
   python .github\skills\lamina-corporativa-jpg\scripts\render.py presentacion\lamina-NN\lamina-NN.html presentacion\lamina-NN\lamina-NN.jpg
   ```
5. Abrir el JPG y verificar: sin texto cortado/desbordado, sin solapes, alineaciones limpias. Corregir y re-renderizar si hace falta.

Requiere Python + Pillow y Microsoft Edge o Chrome instalados. El script garantiza salida exacta 1920×1080, calidad 95.

## Correcciones

Nunca editar el JPG. Para corregir una imagen ya generada: modificar su HTML en `presentacion/lamina-NN/lamina-NN.html` (texto, nodos, orden) y volver a ejecutar el mismo comando de render, que sobrescribe el JPG. Después de corregir, abrir y revisar el resultado. Un cambio de estilo global se hace en `assets/slide.css` y exige re-renderizar las imágenes existentes para que sigan siendo uniformes.

## Plantillas

| Archivo | Uso |
|---|---|
| `01-portada.html` | Imagen de título o cierre (fondo oscuro) |
| `02-contenido.html` | Mensaje + lista de puntos + cifras clave |
| `03-arquitectura-capas.html` | Arquitectura por capas con nodos y flechas |
| `04-componentes.html` | Cuadrícula de componentes/módulos (3×2) |

Para diagramas que no encajan en capas (flujos, secuencias, redes) usar SVG inline con `viewBox="0 0 1728 ..."` (área útil) dentro de `.diagram`, aplicando los mismos tokens.

## Estándar visual (no desviarse)

**Lienzo**: 1920×1080, fondo blanco `#FFFFFF`. Portada/cierre: fondo `#0B1F3A` con barra vertical izquierda `#1F5FBF` de 24 px.

**Paleta** (únicos colores permitidos):
- Navy 900 `#0B1F3A` títulos / fondo oscuro · Navy 700 `#14325C` énfasis, nodos primarios
- Azul 600 `#1F5FBF` único acento fuerte · Azul 100 `#E6EEF9` relleno suave
- Teal 600 `#0F8B8D` acento secundario, uso mínimo · Teal 100 `#E3F3F3`
- Texto `#1B2733` · Texto secundario `#5A6877` · Líneas `#D3DBE5` · Superficie `#F4F6F9`

**Tipografía**: Segoe UI (fallback Helvetica Neue, Arial). Título 56 px semibold · subtítulo 28 · cuerpo 28–30 · texto de tarjeta 24 · etiquetas/leyendas ≥ 20 · portada 96. Nunca menos de 20 px. Eyebrow en mayúsculas con espaciado 0.12em.

**Espaciado**: rejilla de 8 px. Márgenes laterales 96 px (portada 160), superior 72 px, pie a 40 px del borde. Separación entre bloques 32 px. Zona útil: 1728 px de ancho × ~800 px de alto entre cabecera y pie.

**Formas**: esquinas con radio 8 px; bordes de 1–1,5 px (`#D3DBE5` o navy); sin sombras, sin degradados, sin 3D. Conectores de 2 px gris `#5A6877` con punta de flecha. Elementos externos con borde discontinuo.

**Estructura fija de cada lámina de contenido**: eyebrow (sección) → título (mensaje, una idea) → filete azul 96×4 → cuerpo → pie con nombre del producto a la izquierda. Sin número de página (el orden lo define el usuario al juntar los JPG).

## Reglas de sobriedad

- Una idea por lámina; título que exprese la conclusión, no solo el tema.
- Máximo ~6 bloques o ~4 puntos por lámina; texto de nodos en 1–2 líneas.
- Un solo color de acento dominante (azul); teal solo para diferenciar una categoría.
- Mucho espacio en blanco; alinear todo a la rejilla y a los márgenes.
- Sin clip-art, emojis, fotos de stock ni decoraciones. Iconos solo si son simples, lineales y del mismo trazo.
- Incluir leyenda en diagramas que usen más de dos estilos de nodo.
- Mantener nombre del producto y terminología idénticos en todas las imágenes.
- Si el contenido no cabe, proponer dividirlo en dos imágenes en lugar de reducir la fuente.
