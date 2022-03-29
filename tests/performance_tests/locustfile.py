from locust import HttpUser, task

competition = "Spring Festival"
club = "Simply Lift"


class AppPerformanceTest(HttpUser):
    
    @task
    def index(self):
        self.client.get("/")
    
    @task
    def summary(self):
        self.client.post("/showSummary", {"email":"john@simplylift.co"})


    @task
    def booking(self):
        self.client.get("/book/" + competition + "/" + club )

    @task
    def purchased(self):
        self.client.post("/purchasePlaces", 
        {"club":"Simply Lift", 
        "competition":"Spring Festival", 
        "places":"2"
        })

    @task
    def logout(self):
        self.client.get("/logout")
