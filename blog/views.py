from django.shortcuts import render, redirect
from blog.models import PostModel

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

cloud_config = {
    'secure_connect_bundle': 'C:/Users/larat/Documents/Tomi Files/projects/tech_blog/techblog/secure-connect-techblog.zip'
}
auth_provider = PlainTextAuthProvider('WSbuLmzAbweUSKaTUZhPufjZ', 'Ha8Wb,hn2aGLa3g9QU0.3W_p0wM.gcOn84dAS_j7yjIodlIZZa-lFTqY4Hhaoyy2KfSY40u_2Dc_KuG2,rH0r3F6dmmPL97jJ0HoIiIZcOFj3c_kL0ihtX+HEPEfyINz')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('tech_blog')


# Create your views here.
def home(request):
    posts_list = []
    rows = session.execute('SELECT title, body, created_at, id FROM post_model')
    for row in rows:
        lists = row.title, row.body, row.created_at, row.id
        posts_list.append(lists)
    return render(request, 'index.html', {'posts': posts_list})

def newpost(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']

        new_post = PostModel.objects.create(title=title, body=body)
        new_post.save
        return redirect('/')
    else:
        return render(request, 'newpost.html')

def posts(request, pk):
    post = PostModel.objects.get(id=pk)
    return render(request, 'post.html', {'post': post})