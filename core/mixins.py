from django.db import models

class VoteMixin(models.Model):
    up_votes = models.IntegerField(default = 0)
    down_votes = models.IntegerField(default = 0)
    net_votes = models.IntegerField(default = 0)

    def up_vote(self, user):
        if user not in self.up_voted_by.all():
            self.up_voted_by.add(user)

            if user in self.down_voted_by.all():
                self.down_voted_by.remove(user)

            self.save()

    def down_vote(self, user):
        if user not in self.down_voted_by.all():
            self.down_voted_by.add(user)

            if user in self.up_voted_by.all():
                self.up_voted_by.remove(user)

            self.save()

    def get_net_votes(self):
        return self.up_voted_by.all().count() - self.down_voted_by.all().count()

    def total_votes(self):
        return self.up_votes + self.down_votes

    def up_vote_pct(self):
        if self.total_votes() == 0:
            return "N/A"
        return self.up_votes/self.total_votes()*100

    def save(self, *args, **kwargs):
        self.net_votes = self.get_net_votes()
        super().save()

    class Meta:
        abstract = True
