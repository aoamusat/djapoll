from polls.models import Question, Choice
from django_seed import Seed

seeder = Seed.seeder()

seeder.add_entity(Question, 2)

inserted = seeder.execute()