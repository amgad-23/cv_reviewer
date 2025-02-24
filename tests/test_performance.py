from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def test_upload_cv(self):
        self.client.get("/api/upload-cv")

    @task
    def test_query(self):
        self.client.get("/api/candidates-with-skill?skill=Python")
