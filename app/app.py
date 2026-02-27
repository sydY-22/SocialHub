from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse

app = FastAPI()

text_posts = {1: {"title": "New Post", "content": "cool post test"},
              2: {
                  "title": "New Beginnings",
                  "content": "Every day is a fresh start. Take a deep breath, set your intention, and begin again."
              },
              3: {
                  "title": "Tech Trends 2026",
                  "content": "AI agents, spatial computing, and personalized automation are shaping the future of how we work and live."
              },
              4: {
                  "title": "Healthy Habits",
                  "content": "Small daily improvements—like drinking more water and walking 10 minutes—lead to big long-term results."
              },
              5: {
                  "title": "Productivity Hack",
                  "content": "Try the 50/10 rule: 50 minutes of focused work followed by a 10-minute break to reset your mind."
              },
              6: {
                  "title": "Weekend Vibes",
                  "content": "Slow mornings, good coffee, and zero alarms. That’s the energy we’re keeping."
              },
              7: {
                  "title": "Learning Never Stops",
                  "content": "Read books, take courses, ask questions. Growth begins where comfort ends."
              },
              8: {
                  "title": "Creative Spark",
                  "content": "Ideas often show up when you least expect them. Keep notes—your next big idea might be one thought away."
              },
              9: {
                  "title": "Mindset Matters",
                  "content": "Discipline beats motivation. Show up consistently, even on the days you don’t feel like it."
              },
              10: {
                  "title": "Digital Minimalism",
                  "content": "Unfollow, unsubscribe, declutter. Protect your attention like it’s your most valuable asset—because it is."
              }
              }


@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts


@app.get("/posts/{id}")
def get_post(id: int) -> PostResponse:
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)


@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post
