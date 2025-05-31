from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from . import models

import markdown
import json

# Debo tener 3 vistas definidas:
    # Vista para mostrar el README.md
    # Vista para guardar el README.md
    # Vista para obtener todos los objetos guardados en la base de datos y hacer una preview
    # en la pantalla principal, que no muestre el contenido del README.md, sino que muestre la información
    # del blog(Autor, Título, Fecha de creación) el id se debe guardar para después poder dar click en el blog
    # y que se muestre el contenido del README.md haciendo un llamada a la vista de mostrar el README.md

@method_decorator(csrf_exempt, name='dispatch')
class ReadmeView(View):
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            try:
                blogPost = get_object_or_404(models.Post, id=pk)
                markdown_content = blogPost.content

                # Convertir el contenido Markdown a HTML
                # Utilizando la librería markdown para convertir el contenido Markdown a HTML
                html_content = markdown.markdown(
                    markdown_content,
                    extensions=[
                        'codehilite',      # Resaltado de código
                        'fenced_code',     # Bloques ``` ```
                        'tables',          # Tablas
                        'toc',             # Tabla de contenidos (opcional)
                        'nl2br',           # Saltos de línea automáticos (opcional)
                    ]
                )
                
                return render(request, 'readme.html', {'content': html_content})
            
            except FileNotFoundError:
                return HttpResponse("README no encontrado", status=404)
        
        else:
            # Lógica para obtener todos los objetos guardados y hacer una preview
            blogPosts = models.Post.objects.all()
            return render(request, 'postList.html', {'posts': blogPosts})

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            
            new_post = models.Post.objects.create(
                title=data.get('title'),
                content=data.get('content'),  
                autor=data.get('autor', 'Anónimo')
            )
            
            return JsonResponse({
                "message": "README.md guardado exitosamente",
                "id": new_post.id,
                "title": new_post.title
            })
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
