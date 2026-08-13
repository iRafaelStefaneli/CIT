# Sistema Acadêmico CIT

Sistema Acadêmico desenvolvido em Python (com CustomTkinter para a interface gráfica e JSON para persistência de dados), criado como projeto acadêmico. Simula uma plataforma de gestão escolar para uma instituição fictícia, com portais distintos para Administrador, Professor e Aluno, permitindo controle de notas, faltas e atividades.

## Funcionalidades

- **Login por perfil**: acesso diferenciado para Administrador, Professor e Aluno.
- **Portal do Administrador**: cadastro de alunos, professores e turmas.
- **Portal do Professor**: lançamento de notas e faltas, criação de atividades para as turmas.
- **Portal do Aluno**: visualização de notas, faltas, resultados de atividades e conteúdos disponíveis.
- **Persistência de dados** em arquivos JSON (sem necessidade de banco de dados externo).

## Tecnologias utilizadas

- **Python 3**
- **CustomTkinter** (interface gráfica)
- **JSON** (armazenamento de dados)

## Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/SEU-USUARIO/sistema-academico-cit.git
   cd sistema-academico-cit
   ```

2. Instale as dependências:
   ```bash
   pip install customtkinter pillow requests
   ```

3. Execute o sistema:
   ```bash
   python "Projeto CIT.py"
   ```

## Estrutura do projeto

```
├── Projeto CIT.py     # Código principal do sistema
├── dados.json          # Base de dados (turmas, notas, faltas, atividades)
├── users.json           # Base de usuários do sistema
└── README.md
```

## Observação

Este é um projeto acadêmico desenvolvido para fins de aprendizado, unindo conceitos de lógica de programação, estruturas de dados, engenharia de software ágil e modelagem UML.
