# projectus/management/commands/atualizar_posts.py
#
# Atualiza os posts do blog com títulos, textos e capas novas,
# e cria posts que ainda não existem.
#
# Como usar (na pasta do projeto, com o ambiente virtual ativado):
#     python manage.py atualizar_posts
#
# Pode rodar quantas vezes quiser: ele nunca duplica posts.
# Ele procura cada post pelo título antigo OU pelo título novo.

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.templatetags.static import static

from projectus.models import Post


# Cada item da lista é um post.
#   'titulos_antigos': títulos usados para encontrar o post no banco
#   'capa': nome do arquivo em projectus/static/projectus/img/posts/
POSTS = [
    {
        'titulos_antigos': ['Introdução ao Django'],
        'title': 'Django: crie sites completos com Python',
        'summary': 'Conheça o framework que já vem com login, painel administrativo e banco de dados prontos para usar.',
        'capa': 'django.jpg',
        'textbody': """Django é um framework web escrito em Python que segue uma ideia simples: você não precisa reinventar a roda. Os recursos que todo site precisa já vêm prontos, e você foca no que torna o seu projeto único.

É a mesma ferramenta usada por plataformas como o Instagram, que atendem milhões de pessoas todos os dias.

O que já vem pronto no Django
• Sistema de usuários, com cadastro, login e recuperação de senha
• Painel administrativo gerado automaticamente
• ORM, que permite trabalhar com o banco de dados usando Python, sem escrever SQL
• Proteção contra ataques comuns, como CSRF e SQL Injection

A estrutura segue o padrão MTV: o Model cuida dos dados, o Template cuida da aparência e a View faz a ligação entre os dois.

Para começar, bastam dois comandos: django-admin startproject cria a estrutura do projeto e python manage.py runserver coloca o site no ar no seu computador. Este blog, aliás, foi construído com Django.""",
    },
    {
        'titulos_antigos': ['Aprendendo Python'],
        'title': 'Python do zero: por onde começar',
        'summary': 'Os primeiros passos na linguagem mais versátil do momento, do primeiro print até os seus próprios projetos.',
        'capa': 'python.jpg',
        'textbody': """Python é hoje uma das linguagens de programação mais usadas no mundo. E não é por acaso: a sintaxe é limpa, parecida com o inglês, e permite escrever programas úteis já nas primeiras semanas de estudo.

Ela está por trás de sites, automações, análise de dados, inteligência artificial e ferramentas que facilitam o trabalho no escritório.

Por onde começar
• Variáveis e tipos de dados: textos, números e listas
• Condicionais (if, elif e else) para tomar decisões no código
• Laços de repetição (for e while) para automatizar tarefas
• Funções, para organizar e reaproveitar o que você escreveu

Uma dica que faz diferença: pratique todos os dias, nem que seja por 20 minutos. Reescreva os exemplos, mude os valores, quebre o código de propósito e veja o que acontece. É errando que a lógica de programação começa a fazer sentido.

Depois do básico, escolha um caminho: desenvolvimento web com Django, análise de dados com Pandas ou automação de tarefas. O importante é colocar a mão no código e construir algo seu.""",
    },
    {
        'titulos_antigos': ['Criando APIs REST'],
        'title': 'APIs REST: como os sistemas conversam entre si',
        'summary': 'Entenda o que acontece quando um aplicativo busca dados em outro sistema e por que isso move a internet.',
        'capa': 'apis-rest.jpg',
        'textbody': """Sempre que você consulta o rastreio de uma encomenda, vê a previsão do tempo no celular ou paga uma compra com Pix, existe uma API trabalhando nos bastidores.

API é a sigla para Interface de Programação de Aplicações. Na prática, é um conjunto de regras que permite que um sistema peça informações a outro e receba uma resposta organizada.

Os principais verbos do REST
• GET: buscar dados, como listar os posts de um blog
• POST: criar algo novo, como publicar um comentário
• PUT ou PATCH: atualizar um registro que já existe
• DELETE: remover um registro

As respostas geralmente chegam em JSON, um formato de texto leve que tanto pessoas quanto programas conseguem ler com facilidade.

Cada resposta também traz um código de status: 200 significa que deu tudo certo, 404 que o recurso não foi encontrado e 500 que houve um erro no servidor.

No mundo Python, o Django REST Framework é uma das formas mais populares de criar APIs. Com ele, os mesmos dados de um site podem alimentar um aplicativo de celular ou um painel de Power BI.""",
    },
    {
        'titulos_antigos': ['Templates no Django'],
        'title': 'Templates no Django: HTML organizado e reutilizável',
        'summary': 'Aprenda a usar a herança de templates para escrever menos código e manter o visual do site consistente.',
        'capa': 'templates.jpg',
        'textbody': """Imagine ter que copiar o mesmo cabeçalho, menu e rodapé em cada página do seu site. Agora imagine precisar mudar um link do menu em vinte arquivos diferentes. É exatamente esse problema que os templates do Django resolvem.

A ideia central é a herança: você cria um arquivo base com a estrutura que se repete e, nas outras páginas, preenche apenas o que muda.

Os recursos mais usados
• {% extends %}: indica de qual template a página herda a estrutura
• {% block %}: define as áreas que cada página pode preencher
• {{ variavel }}: exibe os dados enviados pela view
• {% for %} e {% if %}: repetem e condicionam partes do HTML
• {% url %}: gera links a partir do nome das rotas, sem endereços fixos

Com essa organização, todas as páginas deste blog compartilham um único arquivo base. Foi por isso que bastou ligar uma folha de estilos nele para que o site inteiro ganhasse um visual novo.

Templates bem organizados deixam o projeto mais fácil de manter, de entender e de evoluir.""",
    },
    {
        'titulos_antigos': [],
        'title': 'Site responsivo com CSS: do celular ao computador',
        'summary': 'Como CSS Grid, variáveis e media queries deixam qualquer página bonita em qualquer tamanho de tela.',
        'capa': 'css-responsivo.jpg',
        'textbody': """O celular é o principal aparelho de acesso à internet no Brasil. Um site que só funciona bem no computador perde visitantes logo no primeiro clique.

Site responsivo é aquele que se adapta automaticamente ao tamanho da tela. Os mesmos elementos se reorganizam para continuar legíveis e fáceis de usar em qualquer dispositivo.

As ferramentas que fazem isso acontecer
• Meta tag viewport: avisa ao navegador do celular que a página foi pensada para telas pequenas
• CSS Grid e Flexbox: organizam os elementos em linhas e colunas flexíveis
• Media queries: aplicam regras diferentes a partir de uma largura de tela
• Variáveis CSS: centralizam cores e espaçamentos para manter tudo consistente

Neste blog, por exemplo, os posts aparecem em três colunas no computador, duas no tablet e uma no celular. A regra que faz isso tem poucas linhas de código.

Uma boa prática é pensar primeiro no celular e depois expandir para telas maiores. Assim, o conteúdo mais importante nunca fica escondido.""",
    },
    {
        'titulos_antigos': [],
        'title': 'Senhas fora do código: protegendo seu projeto com .env',
        'summary': 'Um erro comum de quem está começando e uma solução simples para não expor senhas no GitHub.',
        'capa': 'env-seguranca.jpg',
        'textbody': """Um dos erros mais comuns de quem está começando é escrever senhas diretamente no código. Parece inofensivo até o dia em que o projeto vai para o GitHub e qualquer pessoa pode ler a senha do seu e-mail ou do seu banco de dados.

A solução é simples: guardar as informações sensíveis em variáveis de ambiente, dentro de um arquivo chamado .env, que nunca é enviado para o repositório.

Como funciona na prática
• O arquivo .env guarda as senhas e chaves no formato NOME=valor
• O .gitignore impede que o .env seja enviado para o GitHub
• A biblioteca python-dotenv carrega esses valores quando o projeto inicia
• No código, os valores são lidos com os.getenv('NOME')

Também vale criar um arquivo .env.example, com os nomes das variáveis e sem os valores reais. Assim, quem baixar o projeto sabe exatamente o que precisa configurar.

E se uma senha já foi exposta, o caminho é revogá-la e gerar uma nova. Apagar do código não basta, porque ela continua guardada no histórico do Git.""",
    },
]


class Command(BaseCommand):
    help = 'Atualiza os posts do blog com textos e capas novas e cria os que faltam'

    def handle(self, *args, **options):
        User = get_user_model()

        # Autor dos posts novos: o mesmo autor dos posts existentes
        # (ou o primeiro usuário cadastrado, se não houver posts)
        primeiro_post = Post.objects.order_by('id').first()
        autor = primeiro_post.user if primeiro_post else User.objects.order_by('id').first()

        if not autor:
            self.stdout.write(self.style.ERROR(
                'Crie pelo menos um usuário antes de rodar este comando.'
            ))
            return

        atualizados = 0
        criados = 0

        for dados in POSTS:
            titulos = dados['titulos_antigos'] + [dados['title']]

            # Procura o post pelo título antigo ou pelo novo
            post = Post.objects.filter(title__in=titulos).order_by('id').first()

            campos = {
                'title': dados['title'],
                'summary': dados['summary'],
                'textbody': dados['textbody'],
                'thumbnail': static(f"projectus/img/posts/{dados['capa']}"),
            }

            if post:
                for campo, valor in campos.items():
                    setattr(post, campo, valor)
                post.save()
                atualizados += 1
                self.stdout.write(f'  Atualizado: {post.title}')
            else:
                post = Post.objects.create(user=autor, **campos)
                criados += 1
                self.stdout.write(f'  Criado:     {post.title}')

        self.stdout.write(self.style.SUCCESS(
            f'Pronto! {atualizados} post(s) atualizado(s) e {criados} criado(s).'
        ))
