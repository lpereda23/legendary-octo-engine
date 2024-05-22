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
    title: str
    content: str
    created_at: str
    comments: List[Comment]
    username: str
    is_comment_visible: str = 'none'
