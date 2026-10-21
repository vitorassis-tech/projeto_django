from django.shortcuts import get_object_or_404, render
from projectus.models import Post
from django.conf import settings


def post_view(request, id):

    # Obtém o post solicitado pelo ID
    post = get_object_or_404(Post, id=id)

    # Trata nome do autor
    if post.user.first_name and post.user.last_name:
        author_name = f'{post.user.first_name} {post.user.last_name}'
    elif post.user.first_name:
        author_name = post.user.first_name
    else:
        author_name = post.user.username

    # Obtém os posts do mesmo autor aleatóriamente
    posts = Post.objects.filter(
        user=post.user,
        is_active=True,
        is_deleted=False
    ).exclude(
        # Excluindo o post atual
        id=post.id
    ).order_by('?')[:3]  # Fatia somente 3 posts

    return render(
        request,
        'projectus/post_view.html',
        {
            'tag_title': f'{settings.SITENAME} - {post.title}',
            'post': post,  # Post original
            'posts': posts,  # Posts do autor
            'author_name': author_name, # Nome do autor do post, ajustado
        }
    )
