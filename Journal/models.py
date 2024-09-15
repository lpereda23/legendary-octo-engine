# Our models classes => aligns with the way our tables in Supabase are structured...

from typing import List
import reflex as rx

class Comment(rx.Base):
    id: str
    user_id: str
    post_id: str
    content: str
    created_at: str
    username: str

class CustomPost(rx.Base):
    id: str # THE KEYS MUST MATCH THE KEYS INSIDE SUPABASE TABLES
    user_id: str
    intention: str
    success: str
    lesson: str
    grateful: str
    lesson_score: int
    success_score: int
    created_at: str
    comments: List[Comment]
    username: str
    is_comment_visible: str = 'none'

class StatsMetrics(rx.Base):
    post_id: str
    user_id: str
    lesson_score: int
    success_score: int
    created_at: str


# class Profile(rx.Base):
#     email: str
#     password: str
#     # notifications: bool = False
