from django.shortcuts import render
from django.http import HttpResponse

projects_list = [
    {'id': 1,
    'name':'Multi vendor ecommerce',
    'description':'many vendors selling many things online for everyone to see and buy!'
    },
    {'id': 2,
    'name':'Uber eats',
    'description':'many restaurants selling many food online for everyone to order and eat!'
    },
    {'id': 3,
    'name':'Online arcade',
    'description':'many games online for everyone to see and play and have fun!'
    },
    {'id': 4,
    'name':'Accountability post it notes',
    'description':'many people posting notes for their goals and daily activities to work and grow with others!'
    },
]


def projects(request):
    number = 10
    context = {'msg':'General Kenobi', 'number':number, 'projects':projects_list}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    
    for project in projects_list:
        if str(project['id']) == pk:
            break
        else:
            project=None

    return render(request, 'projects/single_project.html', {'project':project})