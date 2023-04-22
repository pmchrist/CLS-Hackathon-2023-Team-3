from everything_else import SocialNorms
import mesa

model = SocialNorms(10)
for i in range(10):
    model.step()