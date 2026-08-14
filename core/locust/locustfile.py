from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post(
            "/accounts/api/v1/jwt/create/",
            json={
                "email": "farimahtizghadam@gmail.com",
                "password": "nimrimah",
            },
        )

        print("LOGIN STATUS:", response.status_code)
        print("LOGIN BODY:", response.text)

        if response.status_code == 200:
            access_token = response.json().get("access")

            if access_token:
                self.client.headers.update({"Authorization": f"Bearer {access_token}"})
        else:
            print(
                "Login failed:",
                response.status_code,
                response.text,
            )

    @task
    def post_list(self):
        self.client.get("/blog/api/v1/post/")

    @task
    def post_category(self):
        self.client.get("/blog/api/v1/category/")
