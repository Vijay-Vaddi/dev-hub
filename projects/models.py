from django.db import models
import uuid

class Project(models.Model):
    
    '''
    :title:<str> title of the project
    :description:<str> title of the project
    :demo link, source code:<str> url to live demo, source code respectively
    :tags:<str> many-many relation to tags Model 
    :vote_ratio:<int> to show what % of the votes were +ve vs -ve
    '''
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, 
                          editable=False, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=1000, null=True, blank=True)
    source_code = models.CharField(max_length=1000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True) #in quotes since Tag is defined below
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    # one-one with project table
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )

    # owner of review
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, 
                          editable=False, unique=True)
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=100, choices=VOTE_TYPE)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.value
    
    class Meta:
        ordering = ['date_time']

class Tag(models.Model):
    # many-many with project table

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, 
                          editable=False, unique=True)
    name = models.CharField(max_length=200)
    date_time = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name


