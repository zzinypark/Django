from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from todo.forms import CommentForm
from todo.models import Todo, Comment


class TodoListView(LoginRequiredMixin,ListView):
    queryset = Todo.objects.all()
    template_name = 'todo_list.html'
    context_object_name = 'todo_list'
    paginate_by = 10
    ordering = ('-created_at',)

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')

        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )
        return queryset

class TodoDetailView(LoginRequiredMixin,DetailView):
    model = Todo
    queryset = Todo.objects.all().prefetch_related('comments', 'comments__user')
    template_name = 'todo_info.html'
    context_object_name = 'todo'

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not (self.request.user.is_superuser or obj.user == self.request.user):
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo = self.object
        comments = todo.comments.order_by("-created_at")
        paginator = Paginator(comments, 10)
        context.update({
            "todo": todo.__dict__,
            "comment_form": CommentForm(),
            "page_obj": paginator.get_page(self.request.GET.get("page")),
        })
        return context

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo_create.html'
    fields = ('title', 'description', 'start_date', 'end_date')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.pk})

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    template_name = 'todo_update.html'
    fields = ('title', 'description', 'start_date', 'end_date' ,'is_completed')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (self.request.user.is_superuser or obj.user == self.request.user):
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.pk})

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (self.request.user.is_superuser or obj.user == self.request.user):
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['message']
    pk_url_kwarg = 'todo_id'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.todo = Todo.objects.get(pk=self.kwargs['todo_id'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.kwargs['todo_id']})

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['message']

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not (self.request.user.is_superuser or obj.user == self.request.user):
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.todo.id})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (self.request.user.is_superuser or obj.user == self.request.user):
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={"pk": self.object.todo.id})