# Atalho da Pizza

## Visão Geral do Projeto

O "Atalho da Pizza" é uma aplicação desktop intuitiva e eficiente, desenvolvida em Python com a biblioteca `customtkinter`, projetada para simplificar a organização e execução de atalhos. Ele permite aos usuários criar e gerenciar atalhos para uma variedade de elementos, incluindo arquivos locais, pastas do sistema, URLs da web e comandos de terminal. Com uma interface gráfica amigável e funcionalidades robustas, o aplicativo visa otimizar o fluxo de trabalho e o acesso rápido a recursos frequentemente utilizados.

### Funcionalidades Principais

- **Criação Versátil de Atalhos**: Adicione facilmente novos atalhos, especificando um nome descritivo, o caminho ou URL de destino e, opcionalmente, um ícone personalizado.
- **Interface de Usuário Intuitiva**: Os atalhos são apresentados em um formato de "cards" visuais, proporcionando uma experiência de usuário organizada e de fácil navegação.
- **Personalização de Ícones**: Atribua ícones de imagem específicos para cada atalho, permitindo uma identificação visual rápida e personalizada.
- **Geração Automática de Ícones Genéricos**: Para atalhos sem um ícone personalizado, o aplicativo gera ícones genéricos dinamicamente, baseados no tipo do atalho (link, arquivo, pasta, comando), garantindo uma representação visual consistente.
- **Execução Simplificada**: Abra arquivos, acesse pastas, navegue para URLs ou execute comandos diretamente da interface com um único clique, eliminando a necessidade de navegação manual.
- **Persistência de Dados Confiável**: Todos os atalhos criados são automaticamente salvos em um arquivo JSON (`atalhos.json`), garantindo que suas configurações e atalhos sejam preservados entre as sessões do aplicativo.
- **Gerenciamento Eficiente de Atalhos**: Remova atalhos indesejados de forma rápida e descomplicada, mantendo sua lista de atalhos sempre atualizada e relevante.

## Estrutura do Projeto

O projeto "Atalho da Pizza" é organizado de forma modular para facilitar o desenvolvimento, a manutenção e a compreensão. Abaixo, detalhamos os principais arquivos e diretórios:

- `main.py`: Este é o coração da aplicação. Contém a lógica principal da interface gráfica (GUI) construída com `customtkinter`, gerencia a criação, edição e exclusão de atalhos, e coordena a interação com os arquivos de dados e ícones. É o ponto de entrada para a execução do aplicativo.
- `pizza_window.py`: (Assumindo que este arquivo contém a classe da janela principal ou elementos específicos da GUI). Este arquivo provavelmente encapsula a definição da janela principal do aplicativo ou componentes visuais específicos, promovendo a modularidade do código da interface.
- `atalho_pizza.py`: (Assumindo que este arquivo contém a lógica para a criação e gerenciamento de atalhos individuais). Este módulo deve ser responsável pela representação de um atalho (como uma classe ou estrutura de dados) e pelas operações relacionadas a ele, como a execução do atalho.
- `icon_generator.py`: Este script é responsável por gerar os ícones genéricos para os atalhos que não possuem um ícone personalizado. Ele garante que todos os atalhos tenham uma representação visual, mesmo que padrão, e otimiza o desempenho armazenando esses ícones em cache.
- `atalhos.json`: Um arquivo JSON crucial que atua como o banco de dados persistente da aplicação. Todos os dados dos atalhos criados pelos usuários (nome, caminho/URL, tipo, caminho do ícone) são serializados e armazenados neste arquivo. Ele é carregado na inicialização do aplicativo e salvo automaticamente a cada alteração.
- `icon_cache/`: Este diretório é utilizado para armazenar os ícones genéricos gerados pelo `icon_generator.py`. O cache de ícones melhora significativamente o desempenho da aplicação, evitando a regeneração de ícones a cada inicialização ou exibição.
- `assets/`: (Se houver) Este diretório é destinado a armazenar recursos estáticos da aplicação, como imagens padrão, fontes ou outros arquivos multimídia utilizados pela interface.
- `dist/`: Este diretório é criado pelo PyInstaller (ou ferramenta similar) e contém o executável final da aplicação, pronto para distribuição. É o resultado do processo de empacotamento.
- `build/`: Este diretório também é gerado pelo PyInstaller e contém arquivos temporários e intermediários criados durante o processo de construção do executável.
- `venv/`: (Se houver) Este diretório representa o ambiente virtual Python do projeto. É uma prática recomendada para isolar as dependências do projeto do ambiente global do Python, garantindo que as bibliotecas corretas sejam usadas e evitando conflitos.
- `main.spec`: Este arquivo é gerado pelo PyInstaller e contém as especificações de como o executável deve ser construído, incluindo quais arquivos e módulos devem ser incluídos.
- `__pycache__/`: Diretórios criados automaticamente pelo Python para armazenar arquivos bytecode (`.pyc`), que são versões compiladas dos módulos Python para acelerar o tempo de carregamento.

## Como Usar

Para utilizar o "Atalho da Pizza", siga as instruções abaixo, que cobrem desde a configuração do ambiente até a execução da aplicação e a geração de executáveis.

### Requisitos do Sistema

Certifique-se de ter os seguintes requisitos instalados em seu sistema:

- **Python 3.x**: Recomenda-se a versão 3.8 ou superior para garantir compatibilidade com todas as bibliotecas.
- **Bibliotecas Python**: `customtkinter` e `Pillow` são essenciais para a interface gráfica e manipulação de imagens, respectivamente.

### Configuração do Ambiente e Instalação das Dependências

É altamente recomendável criar um ambiente virtual para isolar as dependências do projeto e evitar conflitos com outras instalações Python em seu sistema. Siga os passos:

1. **Navegue até o diretório do projeto** no seu terminal:
   ```bash
   cd /caminho/para/AtalhoDaPizza
   ```

2. **Crie um ambiente virtual** (se ainda não tiver um):
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**:
   - **Windows (Prompt de Comando)**:
     ```bash
     venv\Scripts\activate
     ```
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências** necessárias. Com o ambiente virtual ativado, execute:
   ```bash
   pip install customtkinter Pillow
   ```

### Executando a Aplicação (a partir do Código Fonte)

Após instalar as dependências, você pode executar a aplicação diretamente do código fonte:

1. **Certifique-se de que o ambiente virtual está ativado**.
2. **Execute o script principal**:
   ```bash
   python main.py
   ```
   A janela do "Atalho da Pizza" será exibida, pronta para uso.

### Gerando o Executável (para Distribuição)

Para criar um executável autônomo da aplicação, que pode ser distribuído e executado sem a necessidade de ter o Python instalado, utilize o PyInstaller. Este processo é ideal para criar uma versão do aplicativo para usuários finais.

1. **Instale o PyInstaller** (se ainda não tiver) dentro do seu ambiente virtual:
   ```bash
   pip install pyinstaller
   ```

2. **Navegue até o diretório raiz do projeto** (`AtalhoDaPizza`) no seu terminal.

3. **Execute o comando PyInstaller** com as opções apropriadas. O comando abaixo é configurado para criar um único arquivo executável para Windows, sem console e incluindo os arquivos de dados necessários:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --add-data "atalhos.json:." --add-data "icon_cache:icon_cache" main.py
   ```
   - `--noconfirm`: Sobrescreve arquivos existentes sem pedir confirmação, útil para automação.
   - `--onefile`: Empacota todo o aplicativo em um único arquivo executável, facilitando a distribuição.
   - `--windowed`: Cria uma aplicação sem a janela de console (terminal) visível, ideal para GUIs.
   - `--add-data "atalhos.json:."`: Inclui o arquivo `atalhos.json` no executável. O `.` indica que ele será colocado na raiz do diretório temporário de execução do executável.
   - `--add-data "icon_cache:icon_cache"`: Inclui o diretório `icon_cache` e todo o seu conteúdo no executável, mantendo a estrutura de diretórios relativa.

Após a execução bem-sucedida do PyInstaller, o executável (`main.exe` ou `AtalhoDaPizza.exe`, dependendo do nome do seu script principal) será encontrado na pasta `dist` dentro do diretório do seu projeto. Você pode renomeá-lo para "AtalhoDaPizza.exe" para maior clareza.

**Observação Importante**: A geração de executáveis para um sistema operacional específico (e.g., Windows) deve ser realizada no próprio sistema operacional de destino para garantir a compatibilidade e evitar problemas com bibliotecas e dependências específicas da plataforma. Se você estiver em Linux ou macOS e deseja um executável para Windows, considere usar uma máquina virtual ou um ambiente de CI/CD configurado para Windows.

## Capturas de Tela

Abaixo estão algumas capturas de tela da aplicação "Atalho da Pizza", demonstrando suas principais interfaces e funcionalidades:

### Interface Principal
![Interface Principal](prints/Interface_Principal.png)

### Criar Atalho
![Criar Atalho](prints/Criar_Atalho.png)

### Janela Pizza
![Janela Pizza](prints/Janela_Pizza.png)



## Como Contribuir

Contribuições são sempre bem-vindas! Se você tem ideias para melhorias, novas funcionalidades ou encontrou algum bug, sinta-se à vontade para:

1.  **Abrir uma Issue**: Descreva detalhadamente o problema ou a sugestão na seção de Issues do repositório.
2.  **Criar um Pull Request (PR)**: Se você implementou uma correção ou uma nova funcionalidade, siga os passos abaixo para enviar seu código:
    a.  Faça um fork do repositório.
    b.  Crie uma nova branch (`git checkout -b feature/sua-feature` ou `bugfix/seu-bug`).
    c.  Faça suas alterações e commit (`git commit -m 'feat: adiciona nova funcionalidade'`).
    d.  Envie para o seu fork (`git push origin feature/sua-feature`).
    e.  Abra um Pull Request para a branch `main` deste repositório, descrevendo suas alterações.

Por favor, certifique-se de que seu código siga as boas práticas de programação Python e que todos os testes (se houver) passem.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE). Isso significa que você é livre para usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do software, desde que inclua a notificação de direitos autorais e esta permissão em todas as cópias ou partes substanciais do software.

## Roadmap e Próximos Passos

O "Atalho da Pizza" é um projeto em constante evolução. Abaixo estão algumas ideias e funcionalidades que podem ser implementadas no futuro:

-   **Suporte Multiplataforma Aprimorado**: Melhorar a compatibilidade e a experiência do usuário em sistemas operacionais Linux e macOS.
-   **Interface de Edição de Atalhos**: Adicionar uma funcionalidade para editar atalhos existentes diretamente na interface, sem a necessidade de removê-los e recriá-los.
-   **Categorização de Atalhos**: Implementar um sistema de tags ou categorias para organizar um grande número de atalhos.
-   **Pesquisa e Filtragem**: Adicionar uma barra de pesquisa e opções de filtro para encontrar atalhos rapidamente.
-   **Importação/Exportação de Atalhos**: Funcionalidade para importar e exportar atalhos, facilitando a migração entre dispositivos ou o compartilhamento.
-   **Integração com o Sistema Operacional**: Opções para iniciar o aplicativo com o sistema, adicionar atalhos ao menu de contexto, etc.
-   **Notificações**: Implementar notificações para feedback ao usuário sobre a execução de atalhos ou erros.
-   **Personalização de Temas**: Permitir que o usuário escolha entre diferentes temas visuais para a aplicação.

Sua contribuição é fundamental para o desenvolvimento dessas e de outras funcionalidades!

## Créditos e Agradecimentos

-   Desenvolvido por [Bernardo Sarmento Martins Costa](https://github.com/JovemBernardo).
-   Agradecimentos especiais à comunidade `customtkinter` e `Pillow` pelo excelente trabalho nas bibliotecas.