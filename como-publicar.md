# Como publicar o Nossos Drinks

Guia do zero, sem pressupor nada. Reserve uns 30 minutos na primeira vez.

São duas partes:

- **Parte A — Supabase:** o banco de dados, onde ficam guardadas as avaliações de vocês três.
- **Parte B — GitHub Pages:** a hospedagem, que transforma o arquivo num link que qualquer um abre.

Faça na ordem. A parte A gera duas chaves que você vai colar no arquivo antes de subir na parte B.

---

## Parte A — Criar o banco de dados (Supabase)

### A1. Criar a conta

1. Acesse `supabase.com`
2. Clique em **Start your project**
3. Entre com sua conta do GitHub ou com e-mail e senha (se ainda não tem GitHub, escolha e-mail — você criará o GitHub na parte B)

### A2. Criar o projeto

1. Clique em **New project**
2. **Name:** `nossos-drinks`
3. **Database Password:** clique em *Generate a password* e guarde num lugar seguro. Você provavelmente não vai precisar dela, mas não dá pra recuperar depois.
4. **Region:** escolha a mais perto de vocês — `East US` ou `South America (São Paulo)`
5. Clique em **Create new project**
6. Espere uns 2 minutos enquanto ele monta o projeto

### A3. Criar a tabela

1. No menu da esquerda, clique no ícone **SQL Editor** (parece uma folha com `>_`)
2. Clique em **New query**
3. Apague o que estiver lá e cole exatamente isto:

```sql
create table entries (
  id text primary key,
  venue_name text not null,
  venue_link text,
  venue_address text,
  venue_photo text,
  drink_name text not null,
  drink_photo text,
  author text not null,
  ratings jsonb default '{}'::jsonb,
  notes text,
  reactions jsonb default '{}'::jsonb,
  comments jsonb default '[]'::jsonb,
  ts bigint not null
);

alter table entries enable row level security;

create policy "todos podem ler"
  on entries for select using (true);

create policy "todos podem inserir"
  on entries for insert with check (true);

create policy "todos podem atualizar"
  on entries for update using (true);
```

4. Clique em **Run** (ou Ctrl+Enter)
5. Deve aparecer *Success. No rows returned* — é isso mesmo, a tabela foi criada vazia

### A4. Pegar as duas chaves

1. No menu da esquerda, vá em **Project Settings** (a engrenagem, bem embaixo)
2. Clique em **API**
3. Você vai ver dois valores que precisa copiar:
   - **Project URL** — algo como `https://abcdefgh.supabase.co`
   - **Project API keys → anon public** — um texto bem longo começando com `eyJ...`
4. Deixe essa aba aberta, você usa os dois no próximo passo

### A5. Colar as chaves no arquivo

1. Baixe o arquivo `index.html` que eu te mandei
2. Abra ele num editor de texto:
   - **Mac:** clique com o botão direito → Abrir com → TextEdit
   - **Windows:** clique com o botão direito → Abrir com → Bloco de Notas
3. Logo no começo do arquivo você vai encontrar estas duas linhas:

```javascript
const SUPABASE_URL  = "COLE_A_PROJECT_URL_AQUI";
const SUPABASE_KEY  = "COLE_A_ANON_PUBLIC_KEY_AQUI";
```

4. Substitua o texto entre aspas pelos valores do passo A4. Fica assim:

```javascript
const SUPABASE_URL  = "https://abcdefgh.supabase.co";
const SUPABASE_KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6...";
```

5. **Mantenha as aspas e o ponto e vírgula.** É o erro mais comum.
6. Salve o arquivo (Ctrl+S ou Cmd+S)

Se quiser testar antes de publicar, dê dois cliques no arquivo para abrir no navegador. O aviso vermelho no topo deve ter sumido. Adicione um drink de teste e recarregue a página — se ele continuar lá, o banco está funcionando.

---

## Parte B — Publicar (GitHub Pages)

### B1. Criar a conta

1. Acesse `github.com`
2. Clique em **Sign up**
3. Escolha um nome de usuário — ele vai aparecer no endereço final, então vale escolher algo apresentável, tipo `joaobrilhante`
4. Confirme o e-mail que eles enviarem

### B2. Criar o repositório

Repositório é só o nome que o GitHub dá para uma pasta de projeto.

1. No canto superior direito, clique no **+** → **New repository**
2. **Repository name:** `nossos-drinks`
3. Marque **Public** (o Pages gratuito exige público)
4. **Não** marque nenhuma das caixas de inicialização
5. Clique em **Create repository**

### B3. Subir o arquivo

1. Na tela que aparecer, clique no link **uploading an existing file**
2. Arraste o `index.html` já editado para a área indicada
3. Lá embaixo, clique em **Commit changes**

### B4. Ligar o Pages

1. No topo do repositório, clique em **Settings**
2. No menu da esquerda, clique em **Pages**
3. Em **Source**, escolha **Deploy from a branch**
4. Em **Branch**, selecione **main** e a pasta **/ (root)**
5. Clique em **Save**
6. Espere 1 a 2 minutos e recarregue a página

No topo vai aparecer o seu endereço:

```
https://SEUUSUARIO.github.io/nossos-drinks/
```

Esse é o link para mandar pro Renê e pro Luiz.

---

## Como atualizar depois

Sempre que quiser mudar alguma coisa:

1. Entre no repositório
2. Clique no arquivo `index.html`
3. Clique no ícone de lápis (canto superior direito)
4. Edite e clique em **Commit changes**
5. Em um minuto o site já está atualizado

---

## Problemas comuns

**O aviso vermelho continua aparecendo.** As chaves não foram coladas corretamente. Confira se as aspas continuam lá e se não sobrou nenhum pedaço de `COLE_`.

**Salvo um drink e ele some.** Provavelmente a tabela não foi criada ou as políticas do passo A3 não rodaram. Volte no SQL Editor e rode o bloco de novo — se a tabela já existir, ele vai reclamar, e aí rode só a parte a partir do `alter table`.

**O link dá erro 404.** O arquivo precisa se chamar exatamente `index.html`, tudo minúsculo. E o Pages demora até uns 2 minutos na primeira publicação.

**A busca de endereço não retorna nada.** Ela usa o OpenStreetMap, que é gratuito mas limita consultas muito seguidas. Espere alguns segundos e tente de novo, ou escreva o nome à mão — nada quebra por causa disso.

**Os amigos não veem o que eu avaliei.** Confirme que todos estão abrindo o mesmo link publicado, e não um arquivo baixado no celular.

---

## Uma coisa importante sobre segurança

A chave `anon public` fica visível para quem abrir o site — isso é normal e é para isso que ela existe. Mas, do jeito que configuramos, qualquer pessoa com o link pode adicionar e editar avaliações. Para um app entre amigos isso é aceitável, e é o que mantém tudo simples: ninguém precisa criar login.

Se um dia o link vazar e alguém bagunçar, me chame que a gente coloca uma senha ou um login de verdade.
