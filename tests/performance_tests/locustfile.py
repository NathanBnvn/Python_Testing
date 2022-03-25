from locust import HttpUser, task

class AppPerformanceTest(HttpUser):
    
    @task
    def index(self):
        self.client.get("/")
    
    @task
    def summary(self):
        self.client.post("/showSummary", {"email":"john@simplylift.co"})

    @task
    def forbidden(self):
        self.client.get("/unauthorized")

    @task
    def booking(self):
        self.client.get("/book/<competition>/<club>")

    @task
    def purchased(self):
        self.client.post("/purchasePlaces", 
        {"club":"Simply Lift", 
        "competition":"Spring Festival", 
        "places":"6"
        })

    @task
    def index(self):
        self.client.get("/logout")
