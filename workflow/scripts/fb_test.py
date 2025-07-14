# scripts/fb_test.py

from facebook_scraper import get_posts
import time

# A known public page
pages = ["BBCNews"]

for page in pages:
    print(f"\n=== FIRST POSTS FROM {page} ===")
    # Fetch ~50 posts (pages=5)
    for i, post in enumerate(get_posts(page, pages=5, extra_info=True)):
        text = post.get("post_text") or ""
        print(f"\nPOST #{i+1} @ {post.get('time')}\n{text[:200]}…")
        if i >= 2:
            break
    # pause between pages
    time.sleep(2)
