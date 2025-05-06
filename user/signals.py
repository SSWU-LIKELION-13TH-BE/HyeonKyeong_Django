from .models import Stack

def create_default_stacks(sender, **kwargs):
    default_stacks = ["Python", "Django", "JavaScript", "React", "Java"]
    for name in default_stacks:
        Stack.objects.get_or_create(name=name)