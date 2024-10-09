# main API page
from datetime import datetime
import os
import pandas as pd
import jwt
import httpx
from dotenv import load_dotenv

from Journal.models import Comment, CustomPost, StatsMetrics

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
    #print(f"This is the 'headers' {headers}",end='\n')
    # send request...
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, headers=headers, json=data
        )
        print(f"This is response ----- {response.status_code}", end='\n')
        data = response.json()
        print(f"This is data print ----- {data}", end='\n')
        # get the data we need
        access_token = data["access_token"]
        expires_in = data["expires_in"]
        user_id = data["user"]["id"]
        user_email = data["user"]["email"]

        return access_token, expires_in, user_id, user_email

# API endpoint to log out user
async def user_logout_endpoint(access_token: str):

    url = "https://mddgckpnxesyhhwpaydc.supabase.co/auth/v1/logout"

    headers = {
        "apikey": PUBLIC_KEY,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url=url, headers=headers)
        # print(response.status_code)
        # print(response)
        return response.status_code

# second API endpoint: user registration
async def username_registration_endpoint(user_id: str, username: str, access_token: str):
    url = "https://mddgckpnxesyhhwpaydc.supabase.co/rest/v1/users"

    headers = {
        "apikey": PUBLIC_KEY,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "id": user_id,
        "username": username
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        # print(f"This is the response {response}", end='\n')

        # 201, NOT 200
        return response.status_code


async def is_username_taken(username: str, access_token: str):
    url = "https://mddgckpnxesyhhwpaydc.supabase.co/rest/v1/users?select=*"

    headers = {
        "apikey": PUBLIC_KEY,
        "Authorization": f"Bearer {access_token}",
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
    data_post = {
        "email": email,
        "password": password
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data_post)
        # print(f"This is the reponse from the post client email password: {response}", end='\n')
        data = response.json()
        if response.status_code == 400:
            msg = "Email Already Taken!"
            return msg
        else:
            # check if username is taken
            if await is_username_taken(username, data['access_token']) is False:
                # data = response.json()
                # print(f"Data submitted to username_registration_endpoint -> {data}", end='\n')
                await username_registration_endpoint(
                    data["user"]["id"],
                    username,
                    data['access_token']
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

# endpoint to get username
async def get_user_name(access_token: str, user_id: str):
    url = f"https://mddgckpnxesyhhwpaydc.supabase.co/rest/v1/users?id=eq.{user_id}&select=*"

    headers = {
        "apikey": PUBLIC_KEY,
        "Authorization": f"Bearer {access_token}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        # print(response.json())
        if response.status_code == 200:
            response = response.json()[0]['username']
            # print(response)
            return response
        return None

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
        "Authorization": f"Bearer {access_token}"
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

                intention=post["intention"],
                success=post["success"],
                lesson=post["lesson"],
                grateful=post["grateful"],
                lesson_score=post["lesson_score"],
                success_score=post["success_score"],

                created_at=pd.to_datetime(post["created_at"]).strftime('%B %d, %Y'),
                username=next(
                    (
                        user['username']
                        for user in username_list
                        if user["id"] == post["user_id"]
                    ),
                    "none"
                ),
                comments=[]
            )
            for post in response
        ]
        return custom_posts

async def get_comments_for_post(
    access_token: str, post_id: str, username_list: list[dict]
):
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
                created_at=pd.to_datetime(comment["created_at"]).strftime('%B %d, %Y'),
                username=next(
                    (
                        user['username']
                        for user in username_list
                        if user["id"] == comment["user_id"]
                    ),
                    "none",
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
    # print(f"Return of posts--> {posts}")
    return posts


# Method to update posts on filtered dates selected
async def get_posts_with_comments_filtered(
    access_token: str, username_list: list[dict],
    start_date: str, end_date: str
):
    posts: list[CustomPost] = await get_posts_endpoint(
        access_token=access_token, username_list=username_list
    )

    # loop over posts and filter on specific dates and update posts list
    posts = [
        post for post in posts if (pd.to_datetime(post.created_at) <= pd.to_datetime(end_date)) and (
            pd.to_datetime(post.created_at) >= pd.to_datetime(start_date))
    ]

    #loop over the list of custom posts and match the ORIGINAL post id
    # with its counterpart in the COMMENT object
    for post in posts:
        comments: list[Comment] = await get_comments_for_post(
            access_token=access_token, post_id=post.id, username_list=username_list
        )
        # set the post comments list to the newly updated list
        post.comments = comments
    # print(f"Return of posts--> {posts}")
    return posts

# API endpoint to push the post to supabase
async def insert_post_to_database(
    access_token: str, user_id: str,
    post_intention: str, post_success: str,
    post_lesson: str, post_grateful: str,
    post_lesson_score: int, post_success_score: int
):
    url = "https://mddgckpnxesyhhwpaydc.supabase.co/rest/v1/posts"

    headers = {
        "apikey": PUBLIC_KEY,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    data = {
            "user_id": user_id,
            "intention": post_intention,
            "success": post_success,
            "lesson": post_lesson,
            "grateful": post_grateful,
            "lesson_score": post_lesson_score,
            "success_score": post_success_score,
    }

    # print(data, end='\n')
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        # print(response)
        return response.status_code

# API endpoint to insert COMMENT to database
async def insert_comment_to_database(access_token: str, comment: dict):
    url = "https://mddgckpnxesyhhwpaydc.supabase.co/rest/v1/comments"

    # print(comment)

    headers = {
        "apikey": PUBLIC_KEY,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url=url,headers=headers, json=comment)
        # print(response)
        return response.status_code

# API endpoints for STATS Page -------------------------------------------------

async def get_post_stats_endpoint(access_token: str, user_id: str):
    url = f'https://mddgckpnxesyhhwpaydc.supabase.co/rest/v1/posts?&select=*&user_id=eq.{user_id}'

    headers = {
        "apikey": PUBLIC_KEY,
        "Authorization": f"Bearer {access_token}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response = response.json()

        stats_metrics: list[StatsMetrics] = [
            StatsMetrics(
                post_id=post["post_id"],
                user_id=post["user_id"],
                lesson_score=post["lesson_score"],
                success_score=post["success_score"],
                created_at=pd.to_datetime(post["created_at"]).strftime('%B %d, %Y')
            )
            for post in response
        ]
        print(f"STATS_METRICS---->{stats_metrics}", end='\n')
        return stats_metrics

# async def get_x_df(access_token: str, posts: str):
