# 🛡️ SUBOTAI - Sistema de Verificación de Respuestas IA

Sistema de verificación inteligente que compara respuestas directas de LLMs con respuestas verificadas mediante una base de conocimiento interna.

**[🇬🇧 English Version](README_EN.md)** | **🇪🇸 Versión en Español**

---

## 💼 ¿Por qué SUBOTAI?

Una vez implementado en un entorno empresarial, SUBOTAI se convierte en una herramienta estratégica que:

- **Minimiza errores operativos**: Al validar respuestas contra procedimientos internos documentados
- **Estandariza procesos**: Garantiza que el personal consulte y siga protocolos establecidos
- **Optimiza el flujo de trabajo**: Resuelve dudas del equipo de forma instantánea con información verificada
- **Habilita mejora continua**: Analiza patrones de consultas para identificar áreas de optimización y formación

El sistema evoluciona con tu organización: cada pregunta del personal se convierte en datos valiosos para mejorar la productividad y detectar necesidades de capacitación.

---

## 🎯 ¿Qué hace SUBOTAI?

SUBOTAI actúa como un **Sistema inteligente** que combina:
- **Tu base de conocimiento privada** (documentos de referencia)
- **Respuestas de LLMs externos** (OpenAI, DeepSeek)

El resultado es una respuesta verificada con **indicadores mediante colores**:
- **Negro**: Información de tu base de conocimiento
- **🔵 Azul**: Información del LLM que no contradice tu base
- **🔴 Rojo**: Información que contradice tu base o no tiene equivalente para comparar

---

## ✨ Características Principales

### 📊 Interfaz Comparativa
- **Chat Izquierdo**: Respuesta directa del LLM sin filtros
- **Chat Derecho**: Respuesta verificada con indicadores de confianza
- Visualización lado a lado para comparar respuestas

### 📁 Sistema de Documentos
- **Documentos del servidor**: Base de conocimiento predefinida
- **Carga de documentos del usuario**: Sube tus propios archivos `.txt` y `.md`
- Almacenamiento temporal en el navegador (localStorage)
- **🧪 Testing**: Incluye documentos con datos falsos para verificar la detección de contradicciones

### 🌍 Soporte Multilingüe
- Selecciona el idioma de tus documentos internos (20 idiomas disponibles)
- El sistema traduce mentalmente para procesar correctamente
- **⚠️ Nota**: La eficacia depende de las capacidades de traducción del LLM. ChatGPT tiene mucho mejor rendimiento multiidioma que DeepSeek. Se recomienda usar los 2-3 idiomas más comunes (inglés, español, francés) para mejores resultados.

### 🔌 Multi-Proveedor
- **OpenAI** (GPT-3.5, GPT-4)
- **DeepSeek** (DeepSeek-Chat)
- Fácil cambio entre proveedores

---

## 🚀 Instalación Rápida

### Requisitos Previos
- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)
- **Navegador moderno** con soporte para localStorage (Chrome, Firefox, Edge, Safari)

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/SUBOTAI.git
cd SUBOTAI
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar el servidor
```bash
python main.py
```

### 4. Abrir en el navegador
```
http://localhost:8000/app
```

---

## 📖 Uso

### Paso 1: Conectar tu API Key
1. Selecciona tu proveedor (OpenAI o DeepSeek)
2. Introduce tu API Key
3. Clic en **"Conectar"**
4. Espera la validación (botón se pondrá verde)

### Paso 2: (Opcional) Configurar idioma de documentos
1. Haz clic en la bandera 🇪🇸 junto a "Internal DB"
2. Selecciona el idioma de tus documentos internos
3. **Recomendación**: Usa OpenAI para documentos en idiomas distintos al inglés/español, ya que DeepSeek tiene capacidades limitadas de traducción

### Paso 3: (Opcional) Cargar tus documentos
1. Haz clic en **"📖 Internal DB"**
2. Selecciona archivos `.txt` o `.md`
3. Clic en **"✅ Cargar documentos"**
4. Los documentos se guardarán temporalmente en tu navegador

### Paso 4: Hacer preguntas
1. Escribe tu pregunta en el input inferior
2. Presiona **Enter** o clic en **"Enviar"**
3. Observa las dos respuestas:
   - **Izquierda**: Respuesta cruda del LLM
   - **Derecha**: Respuesta verificada con colores

---

## 🎨 Sistema de Colores

La respuesta verificada usa colores para indicar el nivel de verificación:

| Color | Significado | Ejemplo |
|-------|-------------|---------|
| **Negro** | Información de tu base de conocimiento | *"La velocidad de la luz es 299,792 km/s según tu documento ciencia.txt"* |
| **🔵 Azul** | Información del LLM que no contradice tu base | *"Esto significa que la luz puede dar 7.5 vueltas a la Tierra en un segundo"* |
| **🔴 Rojo** | Información que contradice tu base o no tiene equivalente para comparar | *"La velocidad de la luz varía según el medio"* |

---

## 📁 Estructura de Documentos

### Documentos del Servidor
Los documentos predefinidos se almacenan en:
```
SUBOTAI/src/rag/documents/
├── ciencia.txt       # Hechos científicos verificados
└── [tus archivos]    # Añade más archivos aquí
```

**🧪 Nota para Testing**: La base de datos incluye intencionalmente dos documentos con datos completamente falsos. Esto permite verificar de manera rápida y obvia cómo el sistema detecta y marca información contradictoria con el color rojo.

### Documentos del Usuario
- Se cargan desde la interfaz web
- Se guardan en `localStorage` del navegador
- **⚠️ Son temporales**: se borran al cerrar el navegador

**💡 Decisión de Diseño**: Se ha optado por almacenamiento temporal por tres razones fundamentales:
1. **Facilidad de pruebas**: Cualquier usuario puede probar el sistema sin necesidad de configurar cuentas o servicios externos
2. **Privacidad total**: Los documentos nunca salen del navegador del usuario, garantizando confidencialidad absoluta
3. **Simplicidad operativa**: No requiere gestión de bases de datos, autenticación ni infraestructura de almacenamiento

---

## 🔧 Configuración

### Variables de Entorno (Opcional)
Crea un archivo `.env`:
```bash
# Puerto del servidor (por defecto: 8000)
PORT=8000

# Nivel de logging
LOG_LEVEL=INFO
```

### Añadir Documentos al Servidor
Simplemente copia tus archivos `.txt` a:
```bash
SUBOTAI/src/rag/documents/tu_documento.txt
```

El sistema los cargará automáticamente al iniciar.

---

## 🌐 API REST

### Endpoints Principales

#### `/api/query` - Respuesta Verificada
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_API_KEY" \
  -H "X-Provider: openai" \
  -H "X-Documents-Language: es" \
  -d '{
    "query": "¿Cuál es la velocidad de la luz?",
    "user_documents": []
  }'
```

**Respuesta:**
```json
{
  "response": "La velocidad de la luz es 299,792 km/s...",
  "metadata": {
    "rag_used": true,
    "mode": "rag"
  }
}
```

#### `/api/query-raw` - Respuesta Directa
```bash
curl -X POST http://localhost:8000/api/query-raw \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_API_KEY" \
  -H "X-Provider: openai" \
  -d '{
    "query": "¿Cuál es la velocidad de la luz?"
  }'
```

#### `/api/validate-key` - Validar API Key
```bash
curl -X POST http://localhost:8000/api/validate-key \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "sk-...",
    "provider": "openai"
  }'
```

**Respuesta:**
```json
{
  "valid": true
}
```

---

## 📊 Arquitectura

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │
       ↓
┌──────────────────┐
│  Frontend (HTML) │
│  - Chat dual     │
│  - Carga docs    │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│  FastAPI Routes  │
│  /query          │
│  /query-raw      │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│  SUBOTAI Core    │
│  - RAG           │
│  - Judge AI      │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│  Knowledge Base  │
│  - Server docs   │
│  - User docs     │
└──────┬───────────┘
       │
       ↓
┌──────────────────┐
│  LLM Client      │
│  OpenAI/DeepSeek │
└──────────────────┘
```

---

## 📂 Estructura del Proyecto

```
SUBOTAI/
├── main.py                    # Entry point
├── requirements.txt           # Dependencias Python
├── README.md                  # Este archivo (Español)
├── README_EN.md              # Versión en inglés
│
├── static/
│   └── index.html            # Interfaz web completa
│
├── src/
│   ├── api/
│   │   ├── app.py            # FastAPI application
│   │   ├── routes.py         # Endpoints REST
│   │   ├── auth_routes.py    # Validación de API keys
│   │   └── models.py         # Modelos Pydantic
│   │
│   ├── auth/
│   │   └── api_key_manager.py # Gestión de API keys
│   │
│   ├── core/
│   │   ├── config.py         # Configuración
│   │   └── subotai_core.py   # Orchestrator principal
│   │
│   ├── llm/
│   │   └── llm_client.py     # Cliente unificado LLMs
│   │
│   ├── logic/
│   │   └── reasoning_engine.py # Motor de razonamiento
│   │
│   └── rag/
│       ├── knowledge_base.py     # Gestor de documentos
│       ├── rag_orchestrator.py   # IA Juez
│       └── documents/            # Base de conocimiento
│           └── ciencia.txt
│
└── tests/
    ├── test_api.py           # Tests de API
    └── test_integration.py   # Tests de integración
```

---

## 🔒 Seguridad

### API Keys
- Las API keys se almacenan solo en `localStorage` del navegador
- Nunca se guardan en el servidor
- Se envían en headers `Authorization: Bearer {key}`

### Documentos
- **Servidor**: Permanentes, accesibles para todos
- **Usuario**: Temporales, solo en el navegador del usuario

### CORS
Por defecto, el servidor acepta peticiones desde cualquier origen. Para producción, configura CORS en `src/api/app.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-dominio.com"],  # ← Cambia esto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🛠️ Troubleshooting

### ❌ "API Key inválida"
**Causa**: La API key no es válida o no tiene créditos  
**Solución**: Verifica tu API key en el panel del proveedor

### ❌ "No se encontró el modal"
**Causa**: JavaScript no se cargó correctamente  
**Solución**: Abre F12 → Console y busca errores, luego recarga (F5)

### ❌ Los documentos no se cargan
**Causa**: localStorage lleno o deshabilitado  
**Solución**: Limpia la caché del navegador o habilita localStorage

### ❌ Respuestas sin colores
**Causa**: No hay documentos en la base de conocimiento  
**Solución**: Añade archivos `.txt` en `src/rag/documents/` o carga desde la interfaz

### ❌ Error de conexión al servidor
**Causa**: El servidor no está ejecutándose  
**Solución**: 
```bash
cd SUBOTAI
python main.py
```

---

## 🧪 Testing

Ejecutar todos los tests:
```bash
pytest tests/ -v
```

Ejecutar tests específicos:
```bash
# Tests de API
pytest tests/test_api.py -v

# Tests de integración
pytest tests/test_integration.py -v
```

Coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

---

## 📦 Dependencias Principales

| Paquete | Versión | Uso |
|---------|---------|-----|
| `fastapi` | 0.104.1 | Framework web |
| `uvicorn` | 0.24.0 | Servidor ASGI |
| `httpx` | ≥0.25.0 | Cliente HTTP async |
| `pydantic` | 2.5.0 | Validación de datos |
| `python-dotenv` | 1.0.0 | Variables de entorno |
| `pytest` | ≥7.4.0 | Testing framework |
| `aiofiles` | ≥23.0.0 | Operaciones de archivos async |

Ver `requirements.txt` para la lista completa.

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Añadir nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 🔮 Roadmap

### En desarrollo
- [ ] Persistencia de documentos con Supabase
- [ ] Embeddings vectoriales para búsqueda semántica
- [ ] Soporte para más proveedores (Anthropic Claude, Gemini)
- [ ] Historial de conversaciones

### Futuro
- [ ] Modo multi-agente con debate
- [ ] Exportar conversaciones a PDF/Markdown
- [ ] Dashboard de métricas y analytics
- [ ] Plugin para navegadores

---

## 💬 Soporte

¿Problemas o preguntas?

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/SUBOTAI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tu-usuario/SUBOTAI/discussions)

---

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- OpenAI y DeepSeek por sus APIs
- La comunidad de código abierto

---

**Construido con ❤️ para verificar información con confianza**
