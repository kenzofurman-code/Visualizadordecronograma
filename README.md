# GanttFlow Viewer 📊

O **GanttFlow Viewer** é um visualizador web moderno e interativo para cronogramas de projetos exportados em formato PDF (como MS Project, Primavera, etc.). 

A aplicação utiliza um backend inteligente que segmenta o PDF em alta resolução (300 DPI) em quatro quadrantes (lista de tarefas, régua de datas, cabeçalho e corpo do gráfico de Gantt) para permitir uma rolagem sincronizada (estilo planilha/Excel), onde o cabeçalho de datas e a lista de tarefas permanecem travados na tela enquanto você rola o gráfico.

Este projeto foi otimizado para rodar de forma **100% stateless (sem estado)** na memória, tornando-o totalmente compatível com a hospedagem gratuita na **Vercel**.

---

## 🚀 Como Rodar Localmente

### 1. Pré-requisitos
Certifique-se de ter o **Python 3.10+** instalado na sua máquina.

### 2. Ativar o Ambiente Virtual e Instalar Dependências
Abra o terminal na raiz do projeto e execute:

**No Windows (PowerShell):**
```powershell
# Ativar o ambiente virtual (.venv já criado)
.venv\Scripts\activate

# Instalar as dependências (caso não tenham sido instaladas)
pip install -r requirements.txt
```

**No Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Iniciar o Servidor Local
Execute o seguinte comando para rodar o backend e o frontend juntos:
```bash
python -m uvicorn api.index:app --reload
```

Acesse **`http://localhost:8000`** no seu navegador. O frontend será carregado e você poderá arrastar e soltar um arquivo PDF para visualizar.

---

## ☁️ Como Publicar no GitHub e Hospedar no Vercel (Passo a Passo)

### Passo 1: Inicializar o Repositório Git Local
Abra o terminal na raiz do projeto e execute os seguintes comandos:
```bash
# Inicializar o repositório git
git init

# Adicionar todos os arquivos (o .gitignore já está configurado para ocultar a pasta .venv e caches)
git add .

# Criar o primeiro commit
git commit -m "feat: estrutura unificada para deploy no Vercel"
```

### Passo 2: Publicar no GitHub
1. Vá até o [GitHub](https://github.com) e crie um novo repositório vazio (não adicione README, .gitignore ou licença).
2. Copie a URL do repositório gerada (ex: `https://github.com/seu-usuario/seu-repositorio.git`).
3. Volte ao seu terminal e rode os comandos:
   ```bash
   # Renomear a branch principal para main
   git branch -M main

   # Associar o repositório remoto
   git remote add origin URL_DO_SEU_REPOSITORIO_COPIADA

   # Enviar o código para o GitHub
   git push -u origin main
   ```

### Passo 3: Criar o Projeto e Publicar no Vercel
1. Acesse o painel do [Vercel](https://vercel.com) e faça login com a sua conta do GitHub.
2. Clique em **"Add New..."** e depois em **"Project"**.
3. Na lista de repositórios do seu GitHub, clique em **"Import"** ao lado do repositório deste projeto.
4. Na tela de configurações do projeto Vercel:
   - **Framework Preset:** Deixe como **Other** (a Vercel detectará o arquivo `vercel.json` e configurará automaticamente).
   - **Root Directory:** Deixe como raiz `./`.
5. Clique em **"Deploy"**.

A Vercel criará automaticamente os arquivos estáticos do frontend e hospedará o backend em Python dentro de uma Serverless Function. Em poucos minutos, você terá um link seguro e público (ex: `https://seu-projeto.vercel.app`) para usar e compartilhar!

---

## 🛠️ Tecnologias Utilizadas
- **Frontend:** HTML5, CSS3 (Modern Vanilla com Custom Properties e Animações), Vanilla JS.
- **Backend:** FastAPI, PyMuPDF (fitz), Pillow (PIL), Uvicorn.
- **Deployment:** Vercel (Serverless Functions para Python).
