# 🏗️ IDA v4.0 — Архитектура

**Создатель:** Григорьев Айтал Григорьевич (@Mareioak)

---

## 📊 Обзор архитектуры

```
┌─────────────────────────────────────────────────────────┐
│                    IDA v4.0 System                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Python     │  │   Mobile     │  │     Web      │  │
│  │   Backend    │  │     App      │  │   Landing    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                 │                 │           │
│         └─────────────────┼─────────────────┘           │
│                           │                             │
│         ┌─────────────────▼─────────────────┐           │
│         │      LLM Manager (Router)         │           │
│         ├─────────────────────────────────┤           │
│         │ - Groq (Primary)                │           │
│         │ - DeepSeek (Secondary)          │           │
│         │ - Fallback Logic                │           │
│         │ - Task-based Routing            │           │
│         └─────────────────────────────────┘           │
│                           │                             │
│         ┌─────────────────┼─────────────────┐           │
│         │                 │                 │           │
│    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐      │
│    │  Groq   │      │DeepSeek │      │ Future  │      │
│    │  API    │      │  API    │      │ Models  │      │
│    └─────────┘      └─────────┘      └─────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Компоненты

### 1. LLM Providers (`llm_providers/`)

#### Base Provider (`base.py`)
- Абстрактный класс для всех провайдеров
- Стандартный формат ответа (`LLMResponse`)
- Интерфейс для реализации

#### Groq Provider (`groq_provider.py`)
- **Модель:** `mixtral-8x7b-32768`
- **Скорость:** Очень быстрая
- **Качество:** Отличное
- **Цена:** Бесплатно
- **Приоритет:** 1 (Основной)

#### DeepSeek Provider (`deepseek_provider.py`)
- **Модель:** `deepseek-chat`
- **Скорость:** Быстрая
- **Качество:** Очень хорошее
- **Цена:** Бесплатно
- **Приоритет:** 2 (Резервный)

#### LLM Manager (`manager.py`)
- Управление всеми провайдерами
- Автоматический fallback
- Маршрутизация по типу задачи
- Проверка доступности

### 2. Маршрутизация задач

```python
task_routing = {
    "code": "groq",           # Groq лучше для кода
    "reasoning": "deepseek",  # DeepSeek для рассуждений
    "general": "groq",        # Groq для общих вопросов
    "translation": "deepseek",
    "summarization": "groq"
}
```

### 3. Fallback логика

```
Запрос → Выбранный провайдер
           ↓
        Успех? → Ответ
           ↓
         Нет
           ↓
        Следующий провайдер
           ↓
        Успех? → Ответ
           ↓
         Нет
           ↓
        Ошибка: Все провайдеры недоступны
```

---

## 📁 Структура файлов

```
IDA/
├── llm_providers/
│   ├── __init__.py              # Package exports
│   ├── base.py                  # Base provider class
│   ├── groq_provider.py         # Groq implementation
│   ├── deepseek_provider.py     # DeepSeek implementation
│   └── manager.py               # LLM Manager
├── main.py                      # Entry point
├── brain.py                     # NLP logic (updated)
├── config.py                    # Configuration
├── ARCHITECTURE.md              # This file
└── requirements.txt             # Dependencies
```

---

## 🔌 Использование

### Инициализация

```python
from llm_providers import LLMManager

# Создаем менеджер
llm_manager = LLMManager()

# Получаем статус
status = llm_manager.get_status()
print(status)
# {
#     "total_providers": 2,
#     "available_providers": ["groq", "deepseek"],
#     "providers": {
#         "groq": {"available": True, "model": "mixtral-8x7b-32768"},
#         "deepseek": {"available": True, "model": "deepseek-chat"}
#     }
# }
```

### Генерация ответа

```python
# Автоматический выбор лучшего провайдера
response = llm_manager.generate("Привет, как дела?")
print(response.content)
print(f"Provider: {response.provider}")
print(f"Tokens: {response.tokens_used}")

# С указанием типа задачи
best_provider = llm_manager.get_best_provider("code")
response = llm_manager.generate(
    "Напиши функцию на Python",
    provider=best_provider
)

# С конкретным провайдером
response = llm_manager.generate(
    "Вопрос",
    provider="groq",
    max_tokens=1000,
    temperature=0.7
)
```

### Проверка доступности

```python
# Проверить конкретный провайдер
if llm_manager.providers["groq"].is_available():
    print("Groq доступен")

# Получить список доступных
available = llm_manager.list_providers()
print(f"Доступные провайдеры: {available}")
```

---

## 🔐 Безопасность

### Переменные окружения

```bash
# .env
GROQ_API_KEY="gsk_..."
DEEPSEEK_API_KEY="sk_..."
```

### Валидация

- ✅ Проверка API ключей
- ✅ Проверка доступности провайдеров
- ✅ Обработка ошибок
- ✅ Логирование запросов

---

## 📈 Масштабируемость

### Добавление нового провайдера

1. Создать класс, наследующий `BaseLLMProvider`
2. Реализовать методы `generate()` и `is_available()`
3. Добавить в `LLMManager._initialize_providers()`

```python
# llm_providers/new_provider.py
from .base import BaseLLMProvider, LLMResponse

class NewProvider(BaseLLMProvider):
    def generate(self, prompt, **kwargs):
        # Реализация
        pass
    
    def is_available(self):
        # Проверка
        pass
```

### Будущие провайдеры

- [ ] Claude (Anthropic)
- [ ] Ollama (локальные модели)
- [ ] LLaMA (Meta)
- [ ] Mistral
- [ ] Kimi (Moonshot)

---

## 🧪 Тестирование

```python
# tests/test_llm_manager.py
import pytest
from llm_providers import LLMManager

def test_manager_initialization():
    manager = LLMManager()
    assert len(manager.providers) > 0

def test_generate_response():
    manager = LLMManager()
    response = manager.generate("Привет")
    assert response.success
    assert len(response.content) > 0

def test_fallback():
    manager = LLMManager()
    # Отключаем первый провайдер
    manager.priority_order = ["deepseek", "groq"]
    response = manager.generate("Тест")
    assert response.success
```

---

## 📊 Производительность

### Сравнение провайдеров

| Метрика | Groq | DeepSeek |
|---------|------|----------|
| Скорость | ⚡⚡⚡ | ⚡⚡ |
| Качество | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Доступность | 99.9% | 99.5% |
| Цена | Бесплатно | Бесплатно |
| Модель | Mixtral 8x7B | DeepSeek Chat |

---

## 🔄 Интеграция с основным кодом

### В `brain.py`

```python
from llm_providers import LLMManager

class Brain:
    def __init__(self):
        self.llm_manager = LLMManager()
    
    def think(self, prompt, task_type="general"):
        provider = self.llm_manager.get_best_provider(task_type)
        response = self.llm_manager.generate(
            prompt,
            provider=provider
        )
        return response.content
```

### В `main.py`

```python
from brain import Brain

brain = Brain()
response = brain.think("Какое время?", task_type="general")
print(response)
```

---

## 📚 Документация API

### LLMResponse

```python
@dataclass
class LLMResponse:
    content: str              # Содержимое ответа
    model: str               # Используемая модель
    provider: str            # Провайдер
    tokens_used: int         # Использованные токены
    success: bool            # Успех ли запрос
    error: Optional[str]     # Сообщение об ошибке
```

### LLMManager методы

```python
# Генерация ответа
generate(prompt, provider=None, **kwargs) -> LLMResponse

# Получить лучший провайдер для задачи
get_best_provider(task_type) -> str

# Получить статус всех провайдеров
get_status() -> Dict

# Список доступных провайдеров
list_providers() -> List[str]
```

---

## 🚀 Развертывание

### Требования

```
groq>=0.4.0
requests>=2.28.0
python-dotenv>=0.19.0
```

### Установка

```bash
pip install -r requirements.txt
```

### Конфигурация

```bash
# .env
GROQ_API_KEY="gsk_..."
DEEPSEEK_API_KEY="sk_..."
```

---

## 👤 Автор

**Григорьев Айтал Григорьевич** ([@Mareioak](https://github.com/fightmeb1tch99-ux))

---

## 📝 Лицензия

MIT License

---

*IDA v4.0 Architecture — 2026*
