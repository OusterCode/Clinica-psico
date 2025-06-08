# Sistema de Gestão de Clínica Psicológica

## Visão Geral

O Sistema de Gestão é uma aplicação web desenvolvida para facilitar o gerenciamento de uma clínica de psicologia. O sistema permite que psicólogos cadastrem pacientes, registrem consultas, gerenciem tarefas e armazenem dados relevantes de forma eficiente.

## Funcionalidades

- **Gestão de Pacientes:** Adicione, atualize e visualize detalhes dos pacientes, incluindo informações de contato, queixas e status de pagamento.
- **Registro de Consultas:** Registre consultas com detalhes como avaliação de humor, anotações gerais e vídeos.
- **Gestão de Tarefas:** Atribua tarefas específicas aos pacientes com opções de frequência pré-definidas.
- **Visualização de Dados:** Gere gráficos de tendência de humor com base nas consultas anteriores.
- **Acesso Seguro:** As consultas só ficam acessíveis para pacientes com pagamento em dia.

## Tecnologias Utilizadas

- **Backend:** Django (Python)
- **Banco de Dados:** SQLite (padrão, mas pode ser configurado para PostgreSQL/MySQL)
- **Frontend:** HTML, CSS (templates Django, Tailwind)
- **Processamento de Imagens:** Pillow
- **Outras Bibliotecas:** Django Messages Framework

## Instalação

### Clone o Repositório

```sh
git clone https://github.com/yourusername/management-system.git
cd management-system
```

### Inicie o Servidor

```sh
python manage.py runserver
```

## Como Usar

- Acesse `http://127.0.0.1:8000/` para utilizar a interface de gestão de pacientes.
- Cadastre novos pacientes informando seus dados e foto de perfil.
- Registre consultas com avaliação de humor e vídeo.
- Atribua e gerencie tarefas para cada paciente.

## Endpoints da Aplicação

| Endpoint                        | Método | Descrição                                                        |
| ------------------------------- | ------ | ---------------------------------------------------------------- |
| `/`                             | GET    | Visualizar todos os pacientes                                    |
| `/<int:id>`                     | GET    | Visualizar detalhes de um paciente específico                    |
| `/update_patient/<int:id>`      | POST   | Atualizar status de pagamento do paciente                        |
| `/delete_consultation/<int:id>` | POST   | Excluir um registro de consulta                                  |
| `/public_consultation/<int:id>` | GET    | Visualizar consulta pública se o paciente estiver em dia         |

## Observações

- IDE utilizada: Visual Studio Code ([baixar Visual Studio Code](https://code.visualstudio.com/download))
- Visualizador de banco de dados: SQLite Viewer para VS Code ([acessar SQLite Viewer para VS Code](https://github.com/qwtel/sqlite-viewer-vscode))
- Livremente baseado em https://github.com/JustAnotherBitt/Management-System

