from django.db import models
import uuid
from users.models import Profile

class Project(models.Model):
    '''
    :title:<str> title of the project
    :description:<str> description of the project
    :demo link, source code:<str> url to live demo, source code respectively
    :tags:<str> many-to-many relation to tags Model 
    :vote_ratio:<int> to show what % of the votes were +ve vs -ve
    '''
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, 
                          editable=False, unique=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, 
                              null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    project_image = models.ImageField(null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=1000, null=True, blank=True)
    source_code = models.CharField(max_length=1000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True) #in quotes since Tag is defined below
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title

    # to calculate vote total and vote ratio
    @property
    def get_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value='up').count()
        total_votes = reviews.count()
        ratio = (up_votes/total_votes)*100
        
        self.vote_total = total_votes
        self.vote_ratio = ratio
        self.save()

    # get all list of reviewers ID, flat will turn obj into true list
    @property
    def reviewers(self):
        reviewers = self.review_set.all().values_list('owner__id', flat=True)
        print(reviewers)
        return reviewers

    class Meta:
        # ordering = ['created_date_time'] #can add -ve sign to order by asc
        ordering = ['-vote_ratio','-vote_total', 'title']

class Review(models.Model):
    # one-to-one with project table
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, 
                          editable=False, unique=True)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=100, choices=VOTE_TYPE)
    date_time = models.DateTimeField(auto_now_add=True)
    
    # to ensure one user can only leave one review per project
    

    def __str__(self) -> str:
        return self.value
    
    class Meta:
        ordering = ['date_time']
        unique_together = [['owner', 'project']]
        # upgrate it to newer viewsion using unique constraints
        
class Tag(models.Model):
    # many-many with project table

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, 
                          editable=False, unique=True)
    name = models.CharField(max_length=200)
    date_time = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name


