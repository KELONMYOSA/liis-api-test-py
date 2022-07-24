import requests
from requests.auth import HTTPBasicAuth


# Testing requests for posts
def test_posts():
    base_url = "https://hr.recruit.liis.su/qa0/v1/api/79825223592@yandex.ru/"
    basic_auth = HTTPBasicAuth("admin", "123")

    # PostsBefore
    response = requests.get(base_url + "posts")
    assert response.status_code == 200
    posts_before = response.text

    # PostPost
    body_data = "{ \"title\": \"Title\", \"content\": \"Content\" }"
    response = requests.post(base_url + "posts",
                             auth=basic_auth,
                             data=body_data,
                             headers={"content-type": "application/json"}
                             )
    assert response.status_code == 201
    post_id = response.json()["id"]

    response = requests.get(base_url + "post/" + str(post_id))
    assert response.status_code == 200
    post_title = response.json()["title"]
    post_content = response.json()["content"]
    assert post_title == "Title"
    assert post_content == "Content"

    # PutPost
    body_data = "{ \"title\": \"NewTitle\", \"content\": \"NewContent\" }"
    response = requests.put(base_url + "post/" + str(post_id),
                            auth=basic_auth,
                            data=body_data,
                            headers={"content-type": "application/json"}
                            )
    assert response.status_code == 200

    response = requests.get(base_url + "post/" + str(post_id))
    assert response.status_code == 200
    post_title = response.json()["title"]
    post_content = response.json()["content"]
    assert post_title == "NewTitle"
    assert post_content == "NewContent"

    # DeletePost
    response = requests.delete(base_url + "post/" + str(post_id),
                               auth=basic_auth
                               )
    assert response.status_code == 204

    # PostsAfter
    response = requests.get(base_url + "posts")
    assert response.status_code == 200
    posts_after = response.text

    assert posts_before == posts_after


# Testing requests for comments
def test_comments():
    base_url = "https://hr.recruit.liis.su/qa0/v1/api/79825223592@yandex.ru/"
    basic_auth = HTTPBasicAuth("admin", "123")

    # CommentsBefore
    response = requests.get(base_url + "comments")
    assert response.status_code == 200
    comments_before = response.text

    # PostPost
    body_data = "{ \"title\": \"Title\", \"content\": \"Content\" }"
    response = requests.post(base_url + "posts",
                             auth=basic_auth,
                             data=body_data,
                             headers={"content-type": "application/json"}
                             )
    assert response.status_code == 201
    post_id = response.json()["id"]

    # PostComment
    body_data = "{ \"title\": \"Title\", \"content\": \"Content\", \"post\": \"" + str(post_id) + "\" }"
    response = requests.post(base_url + "comments",
                             auth=basic_auth,
                             data=body_data,
                             headers={"content-type": "application/json"}
                             )
    assert response.status_code == 201
    comment_id = response.json()["id"]

    response = requests.get(base_url + "comment/" + str(comment_id))
    assert response.status_code == 200
    comment_title = response.json()["title"]
    comment_content = response.json()["content"]
    assert comment_title == "Title"
    assert comment_content == "Content"

    # PutComment
    body_data = "{ \"title\": \"NewTitle\", \"content\": \"NewContent\" }"
    response = requests.put(base_url + "comment/" + str(comment_id),
                            auth=basic_auth,
                            data=body_data,
                            headers={"content-type": "application/json"}
                            )
    assert response.status_code == 200

    response = requests.get(base_url + "comment/" + str(comment_id))
    assert response.status_code == 200
    comment_title = response.json()["title"]
    comment_content = response.json()["content"]
    assert comment_title == "NewTitle"
    assert comment_content == "NewContent"

    # DeleteComment
    response = requests.delete(base_url + "comment/" + str(comment_id),
                               auth=basic_auth
                               )
    assert response.status_code == 204

    # DeletePost
    response = requests.delete(base_url + "post/" + str(post_id),
                               auth=basic_auth
                               )
    assert response.status_code == 204

    # CommentsAfter
    response = requests.get(base_url + "comments")
    assert response.status_code == 200
    comments_after = response.text

    assert comments_before == comments_after


# Sign-in test
def test_sign_in():
    base_url = "https://hr.recruit.liis.su/qa0/v1/api/79825223592@yandex.ru/"

    body_data = "{ \"username\": \"ruby\", \"email\": \"youremadsil\", \"password\": \"123\" }"
    response = requests.post(base_url + "sign-in",
                             data=body_data,
                             headers={"content-type": "application/json"}
                             )
    resp = str(response.status_code)
    if resp != "200":
        resp = response.json()["message"]
    assert (resp == "200" or resp == "User with this username or email already exists")
