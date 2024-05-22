# main API page
from datetime import datetime
import os
import jwt
import httpx
from dotenv import load_dotenv

from Journal.models import Comment, CustomPost

load_dotenv()
PUBLIC_KEY = os.environ["SUPABASE_KEY"]

# first API endpoint: user login...
async def user_login_endpoint(email: str, password: str) -> None:
    url = "https://mddgckpnxesyhhwpaydc.supabase.co/auth/v1/token?grant_type=password"

    #headers
    headers = {
        "apikey": PUBLIC_KEY,
        "Content-Type": "application/json"
    }

    #data
    data = {
        "email": email,
        "password": password
    }

    # send request...
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, headers=headers, json=data
        )

        data = response.json()
        #print(data)
        # get the data we need
        access_token = data["access_token"]
        expires_in = data["expires_in"]
        user_id = data["user"]["id"]
        user_email = data["user"]["email"]

        return access_token, expires_in, user_id, user_email

# second API endpoint: user registration
async def username_registration_endpoint(user_id: str, username: str):
    url = "https://mddgckpnxesyhhwpaydc.supabase.co/rest/v1/users"

    headers = {
        "apikey": PUBLIC_KEY,
        "Authorization": f"Bearer {PUBLIC_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "id": user_id,
        "username": username
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)

        # 201, NOT 200
        return response.status_code


async def is_username_taken(username: str):
    url = "https://mddgckpnxesyhhwpaydc.supabase.co/rest/v1/users?select=*"

    headers = {
        "apikey": PUBLIC_KEY,
        "Authorization": f"Bearer {PUBLIC_KEY}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url=url,
                                    headers=headers)

        # This will return True if the username is within the Json Object
        return any(username==user.get("username") for user in response.json())


async def user_registration_endpoint(username: str, email: str, password: str):
    url = "https://mddgckpnxesyhhwpaydc.supabase.co/auth/v1/signup"

    #headers and data
    headers = {
        "apikey": PUBLIC_KEY ,
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)

        if response.status_code == 400:
            msg = "Email Already Taken!"
            return msg
        else:
            # check if username is taken
            if await is_username_taken(username) is False:
                data = response.json()
                print(data)
                await username_registration_endpoint(
                    data["user"]["id"],
                    username
                )

                return True
            else:
                msg = "Username Already taken"
                return msg

# endpoint to check validity of JWT
async def is_user_authenticated(access_token: str):
    if access_token:
        result: dict = jwt.decode(jwt=access_token,
                                  options={
                                      "verify_signature":False
                                      })
        #perform simple validation based on expiration...
        # can be changed to somthing more complex
        result = result["exp"]

        #check if the exp. session time has passed...
        if datetime.now() > datetime.fromtimestamp(result):
            return False
        else:
            return True
    else:
        return False

# username endpoint
async def get_usernames():
    url = "https://mddgckpnxesyhhwpaydc.supabase.co/rest/v1/users?select=*"

    headers = {
        "apikey": PUBLIC_KEY,
        "Authorization": f"Bearer {PUBLIC_KEY}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

        return response.json()


# next api, getting our posts from supabase
async def get_posts_endpoint(access_token: str, username_list: str):
    url = "https://mddgckpnxesyhhwpaydc.supabase.co/rest/v1/posts?select=*"

    headers = {
        "apikey": PUBLIC_KEY,
        "Authorization": f"Bearer {PUBLIC_KEY}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response = response.json()
        # print(response)
        # we now create a list of CustomPost data type...
        # Recall this is defined in our data models file
        custom_posts: list[CustomPost] = [
            CustomPost(
                id=post["post_id"],
                user_id=post["user_id"],
                title=post["title"],
                content=post["content"],
                created_at=post["created_at"],
                username=next(
                    (
                        user['username']
                        for user in username_list
                        if user["id"] == post["user_id"]
                    )
                ),
                comments=[]
            )
            for post in response
        ]
        return custom_posts


async def get_comments_for_post(
    access_token: str, post_id: str, username_list: list[dict]
):
    #TODO:Change to correct url for comments table
    url = f"https://mddgckpnxesyhhwpaydc.supabase.co/rest/v1/comments?&select=*&post_id=eq.{post_id}"

    headers = {
        "apikey": PUBLIC_KEY,
        "Authorization": f"Bearer {access_token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

        data = response.json()

        # we now create a comments object from the JSON object
        comments: list[Comment] = [
            Comment(
                id=comment["id"],
                user_id=comment["user_id"],
                post_id=comment["post_id"],
                content=comment["content"],
                created_at=comment["created_at"],
                username=next(
                    (
                        user['username']
                        for user in username_list
                        if user["id"] == comment["user_id"]
                    ),
                    None,
                ),
            )
            for comment in data
        ]
        return comments

# finally, combine the two methods above to generate our POSTS list
async def get_posts_with_comments_api(
    access_token: str, username_list: list[dict]
):
    posts: list[CustomPost] = await get_posts_endpoint(
        access_token=access_token, username_list=username_list
    )

    #loop over the list of custom posts and match the ORIGINAL post id
    # with its counterpart in the COMMENT object
    for post in posts:
        comments: list[Comment] = await get_comments_for_post(
            access_token=access_token, post_id=post.id, username_list=username_list
        )
        # set the post comments list to the newly updated list
        post.comments = comments
    print(f"Return of posts--> {posts}")
    return posts
