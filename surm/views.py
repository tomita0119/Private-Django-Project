from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from surm.models import Group, JoinGroup, Resource, CreateGroupForm, AddResourceForm

def index(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            g = Group(name=form.cleaned_data['name'])
            g.save()
            jg = JoinGroup(user=request.user, group=g)
            jg.save()
        else:
            pass
            return HttpResponseRedirect('/surm/cre_group/')
    
    try:
        mygroups = Group.objects.filter(joingroup__user__exact=request.user)
        print mygroups
        context = {
            'title': 'index',
            'mygroups': mygroups,
        }
    except:
        context = {
            'title': 'index'
        }
    return render(request, 'surm/index.html', context)
    
    
def cre_group(request):
    form = CreateGroupForm()
    context = {
        'title': 'Create Group',
        'form': form
    }
    return render(request, 'surm/cre_group.html', context)
    
    
def group_index(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    join_users = User.objects.filter(joingroup__group__exact=group)
    
    if request.method == 'POST':
        form = AddResourceForm(request.POST)
        if form.is_valid():
            new_resource = Resource(name=form.cleaned_data['name'], url=form.cleaned_data['url'], creater=request.user, group=group)
            new_resource.save()
    else:
        form = AddResourceForm()
    
#     if request.method == 'POST':
#         new_resource = Resource(name=request.POST['resource_title'], url=request.POST['resource_url'], creater=request.user, group=group)
#         new_resource.save()
#     except:
#         pass
    resources = Resource.objects.filter(group=group)
    print resources
    context = {
        'title': group.name,
        'group': group,
        'resources': resources,
        'join_users': join_users,
        'form': form
    }
    return render(request, 'surm/group_index.html', context)

